from aiogram.fsm.state import StatesGroup, State

class Survey(StatesGroup):
    waiting_full_name = State()
    waiting_phone = State()
    waiting_repeat_touch = State()
    waiting_photo_door = State()
    waiting_talk_status = State()
    waiting_flyer_method = State()
    waiting_mailbox_photo = State()
    waiting_flyer_number = State()
    waiting_home_voting = State()
    waiting_finish_choice = State()

class AdminExport(StatesGroup):
    waiting_range = State()

class AdminAuth(StatesGroup):
    waiting_login = State()
    waiting_password = State()
