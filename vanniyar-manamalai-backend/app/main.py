from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.profile import Profile
from models.address import Address
from models.astrology import AstrologyDetails
from models.education import EducationDetails
from models.family import FamilyDetails
from models.partner_preferences import PartnerPreferences
from models.professional import ProfessionalDetails
from models.profile_photo import ProfilePhoto
from models.property import PropertyDetails
import database
from routers import profile, address, astrology, education, family, partner_preferences, professional, profile_photo, property, user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Update if Angular runs on a different host
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
database.Base.metadata.create_all(bind=database.engine)

# Include routers
app.include_router(profile.router)
app.include_router(address.router)
app.include_router(astrology.router)
app.include_router(education.router)
app.include_router(family.router)
app.include_router(partner_preferences.router)
app.include_router(professional.router)
app.include_router(property.router)
app.include_router(profile_photo.router)
app.include_router(user.router)