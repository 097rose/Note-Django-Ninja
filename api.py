from ninja_extra import NinjaExtraAPI
from notes.controllers import NoteController

api = NinjaExtraAPI(
    title="Note System with Audit Log",
    description="A clean architecture example using Ninja-Extra"
)

# 註冊 Controller
api.register_controllers(NoteController)