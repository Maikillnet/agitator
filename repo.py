from __future__ import annotations
from typing import Optional, Iterable
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from .models import Agent, Visit, Contact, RepeatTouch, TalkStatus, FlyerMethod
from hashlib import sha256
from datetime import datetime, timedelta

def phone_hash(phone_e164: str) -> str:
    return sha256(phone_e164.encode()).hexdigest()

async def get_or_create_agent(session: AsyncSession, tg_user_id: int, *, name: str | None = None, username: str | None = None) -> Agent:
    res = await session.execute(select(Agent).where(Agent.tg_user_id == tg_user_id))
    agent = res.scalars().first()
    if agent:
        updated = False
        if name and agent.name != name:
            agent.name = name; updated = True
        if username and agent.username != username:
            agent.username = username; updated = True
        if updated:
            await session.flush()
        return agent
    agent = Agent(tg_user_id=tg_user_id, name=name, username=username)
    session.add(agent)
    try:
        await session.flush()
        return agent
    except IntegrityError:
        await session.rollback()
        res = await session.execute(select(Agent).where(Agent.tg_user_id == tg_user_id))
        agent2 = res.scalars().first()
        if agent2:
            changed = False
            if name and agent2.name != name:
                agent2.name = name; changed = True
            if username and agent2.username != username:
                agent2.username = username; changed = True
            if changed:
                await session.flush()
            return agent2
        session.add(Agent(tg_user_id=tg_user_id, name=name, username=username))
        await session.flush()
        res = await session.execute(select(Agent).where(Agent.tg_user_id == tg_user_id))
        return res.scalars().first()

async def create_visit(session: AsyncSession, agent_id: int, address: str | None = None) -> Visit:
    visit = Visit(agent_id=agent_id, address=address)
    session.add(visit)
    await session.flush()
    return visit

async def close_visit(session: AsyncSession, visit_id: int):
    res = await session.execute(select(Visit).where(Visit.id == visit_id))
    visit = res.scalars().first()
    if visit and not visit.closed_at:
        visit.closed_at = datetime.utcnow()
        await session.flush()

async def create_contact(session: AsyncSession, *, visit_id: int, agent_id: int, full_name: str, phone_e164: str) -> Contact:
    c = Contact(visit_id=visit_id, agent_id=agent_id, full_name=full_name, phone_e164=phone_e164, phone_hash=phone_hash(phone_e164))
    session.add(c)
    await session.flush()
    return c

async def update_contact_fields(session: AsyncSession, contact_id: int, **fields):
    await session.execute(update(Contact).where(Contact.id == contact_id).values(**fields))
    res = await session.execute(select(Contact).where(Contact.id == contact_id))
    return res.scalars().first()

async def close_contact(session: AsyncSession, contact_id: int):
    res = await session.execute(select(Contact).where(Contact.id == contact_id))
    c = res.scalars().first()
    if c and not c.closed_at:
        c.closed_at = datetime.utcnow()
        await session.flush()

async def list_contacts_for_period(session: AsyncSession, *, days: int | None):
    q = select(Contact, Agent).join(Agent, Contact.agent_id == Agent.id, isouter=True)
    if days is not None:
        since = datetime.utcnow() - timedelta(days=days)
        q = q.where(Contact.created_at >= since)
    q = q.order_by(Contact.created_at.desc())
    res = await session.execute(q)
    return res.all()

async def flyer_exists(session: AsyncSession, flyer_number: str) -> bool:
    if not flyer_number:
        return False
    res = await session.execute(select(func.count()).select_from(Contact).where(Contact.flyer_number == flyer_number))
    return (res.scalar() or 0) > 0

async def agent_stats_last24h(session: AsyncSession, agent_id: int) -> dict:
    since = datetime.utcnow() - timedelta(hours=24)
    q = select(Contact).where(Contact.agent_id == agent_id, Contact.created_at >= since)
    res = await session.execute(q)
    rows = res.scalars().all()

    total = len(rows)
    status = {"CONSENT":0, "REFUSAL":0, "NO_ONE":0}
    flyer = {"HAND":0, "MAILBOX":0, "NONE":0}
    home_yes = 0
    for c in rows:
        if c.talk_status:
            status[c.talk_status.value] = status.get(c.talk_status.value, 0) + 1
        if c.flyer_method:
            flyer[c.flyer_method.value] = flyer.get(c.flyer_method.value, 0) + 1
        if c.home_voting:
            home_yes += 1
    return {"total": total, "status": status, "flyer": flyer, "home_yes": home_yes}

# NEW: stats for all agents over period
async def agents_stats_for_period(session: AsyncSession, days: int | None):
    # Prepare agents map
    res = await session.execute(select(Agent))
    agents = res.scalars().all()
    stats = {
        a.id: {
            "agent_id": a.id,
            "agent_tg": a.tg_user_id,
            "agent_username": (f"@{a.username}" if getattr(a, "username", None) else ""),
            "agent_name": a.name or "",
            "total": 0,
            "consent": 0,
            "refusal": 0,
            "no_one": 0,
            "hand": 0,
            "mailbox": 0,
            "none": 0,
            "home_yes": 0,
        } for a in agents
    }
    # Get contacts
    q = select(Contact)
    if days is not None:
        since = datetime.utcnow() - timedelta(days=days)
        q = q.where(Contact.created_at >= since)
    res = await session.execute(q)
    rows = res.scalars().all()
    for c in rows:
        aid = c.agent_id
        if aid not in stats:
            stats[aid] = {
                "agent_id": aid, "agent_tg": None, "agent_username": "", "agent_name": "",
                "total": 0,"consent":0,"refusal":0,"no_one":0,"hand":0,"mailbox":0,"none":0,"home_yes":0
            }
        s = stats[aid]
        s["total"] += 1
        if c.talk_status:
            if c.talk_status.value == "CONSENT":
                s["consent"] += 1
            elif c.talk_status.value == "REFUSAL":
                s["refusal"] += 1
            elif c.talk_status.value == "NO_ONE":
                s["no_one"] += 1
        if c.flyer_method:
            if c.flyer_method.value == "HAND":
                s["hand"] += 1
            elif c.flyer_method.value == "MAILBOX":
                s["mailbox"] += 1
            elif c.flyer_method.value == "NONE":
                s["none"] += 1
        if c.home_voting:
            s["home_yes"] += 1
    # Return list sorted by total desc
    return sorted(stats.values(), key=lambda x: x["total"], reverse=True)
