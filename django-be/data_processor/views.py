# data_processor/views.py
from ninja import NinjaAPI
from .api.routes import router as data_router

# Initialize NinjaAPI instance and add router
api = NinjaAPI()
api.add_router("/", data_router)
