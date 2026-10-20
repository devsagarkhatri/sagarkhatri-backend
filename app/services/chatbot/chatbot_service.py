
from sqlalchemy.orm import Session

from app.services.experience_service import get_experiences
from app.services.profile_service import get_profile
from app.services.project_service import get_projects
from app.services.technology_service import get_technologies


def get_chatbot_profile(db: Session) -> dict | None:
    """Return selected public profile information for the chatbot."""
    profile = get_profile(db)

    if profile is None:
        return None

    return {
        "name": profile.name,
        "headline": profile.headline,
        "hero_description": profile.hero_description,
        "about_title": profile.about_title,
        "about_description": profile.about_description,
        "location": profile.location,
        "email": profile.email,
        "resume_url": profile.resume_url,
    }


def get_chatbot_projects(db: Session) -> list[dict]:
    """Return visible projects with selected public fields."""
    projects = get_projects(db)

    return [
        {
            "name": project.name,
            "slug": project.slug,
            "description": project.description,
            "long_description": project.long_description,
            "github_url": project.github_url,
            "live_url": project.live_url,
            "featured": project.featured,
            "technologies": [
                tag.name for tag in project.tags
            ],
        }
        for project in projects
    ]


def get_chatbot_experience(db: Session) -> list[dict]:
    """Return visible work experience and its public highlights."""
    experiences = get_experiences(db)

    return [
        {
            "job_title": experience.job_title,
            "company_name": experience.company_name,
            "company_url": experience.company_url,
            "location": experience.location,
            "start_date": (
                experience.start_date.isoformat()
                if experience.start_date
                else None
            ),
            "end_date": (
                experience.end_date.isoformat()
                if experience.end_date
                else None
            ),
            "is_current": experience.is_current,
            "display_date": experience.display_date,
            "highlights": [
                point.content for point in experience.points
            ],
        }
        for experience in experiences
    ]


def get_chatbot_technologies(db: Session) -> list[dict]:
    """Return visible technologies and their categories."""
    technologies = get_technologies(db)

    return [
        {
            "name": technology.name,
            "category": technology.category,
        }
        for technology in technologies
    ]
