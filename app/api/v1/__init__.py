from fastapi import APIRouter

from app.api.v1.certifications import router as certifications_router
from app.api.v1.education import router as education_router
from app.api.v1.experience import router as experience_router
from app.api.v1.profile import router as profile_router
from app.api.v1.projects import router as projects_router
from app.api.v1.technologies import router as technologies_router
from app.api.v1.services import router as services_router
from app.api.v1.testimonials import router as testimonials_router
from app.api.v1.social_links import router as social_links_router
from app.api.v1.site_sections import router as site_sections_router
from app.api.v1.me import router as me_router
from app.api.v1 import security_test
from app.api.v1.admin import router as admin_router
from app.api.v1 import chatbot



api_router = APIRouter(
    prefix="/api/v1",
)

api_router.include_router(profile_router)
api_router.include_router(experience_router)
api_router.include_router(projects_router)
api_router.include_router(technologies_router)
api_router.include_router(education_router)
api_router.include_router(certifications_router)
api_router.include_router(services_router)
api_router.include_router(testimonials_router)
api_router.include_router(social_links_router)
api_router.include_router(site_sections_router)
api_router.include_router(me_router)
api_router.include_router(security_test.router, prefix="/api/v1")
api_router.include_router(admin_router)
api_router.include_router(chatbot.router)
