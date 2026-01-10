from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Import model submodules via package-relative imports so SQLAlchemy metadata is populated
# without causing circular import issues when the package is imported by uvicorn.
from app.models import profile as models_profile
from app.models import astrology as models_astrology
from app.models import family as models_family
from app.models import partner_preferences as models_partner_preferences
from app.models import professional as models_professional
from app.models import file as models_file
import app.database as database
from app.routers import (
    profile as profile_router,
    astrology as astrology_router,
    family as family_router,
    partner_preferences as partner_preferences_router,
    professional as professional_router,
    user as user_router,
    file as file_router,
    membership as membership_router,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://89.116.134.253",
                   "http://localhost:4200"],  # Update if Angular runs on a different host
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
database.Base.metadata.create_all(bind=database.engine)

# Include routers (use the package-relative imports)
app.include_router(profile_router.router)
app.include_router(astrology_router.router)
app.include_router(family_router.router)
app.include_router(partner_preferences_router.router)
app.include_router(professional_router.router)
app.include_router(user_router.router)
app.include_router(file_router.router)
app.include_router(membership_router.router)