from pydantic import BaseModel

from app.schemas.certification import CertificationResponse
from app.schemas.education import EducationResponse
from app.schemas.experience import ExperienceResponse
from app.schemas.profile import ProfileResponse
from app.schemas.project import ProjectResponse
from app.schemas.service import ServiceResponse
from app.schemas.site_sections import SiteSectionResponse
from app.schemas.social_link import SocialLinkResponse
from app.schemas.technology import TechnologyResponse
from app.schemas.testimonial import TestimonialResponse


class MeResponse(BaseModel):
    profile: ProfileResponse
    experience: list[ExperienceResponse]
    projects: list[ProjectResponse]
    technologies: list[TechnologyResponse]
    education: list[EducationResponse]
    certifications: list[CertificationResponse]
    services: list[ServiceResponse]
    testimonials: list[TestimonialResponse]
    social_links: list[SocialLinkResponse]
    site_sections: list[SiteSectionResponse]
