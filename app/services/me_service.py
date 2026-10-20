from sqlalchemy.orm import Session

from app.services.certification_service import get_certifications
from app.services.education_service import get_education
from app.services.experience_service import get_experiences
from app.services.profile_service import get_profile
from app.services.project_service import get_projects
from app.services.service_service import get_services
from app.services.site_section_service import get_site_sections
from app.services.social_link_service import get_social_links
from app.services.technology_service import get_technologies
from app.services.testimonial_service import get_testimonials


def get_public_portfolio(db: Session) -> dict:
    profile = get_profile(db)
    if profile is None:
        raise ValueError("Profile not found")

    return {
        "profile": profile,
        "experience": get_experiences(db),
        "projects": get_projects(db),
        "technologies": get_technologies(db),
        "education": get_education(db),
        "certifications": get_certifications(db),
        "services": get_services(db),
        "testimonials": get_testimonials(db),
        "social_links": get_social_links(db),
        "site_sections": get_site_sections(db),
    }
