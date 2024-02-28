from app.extensions import db
from app.models.base import BaseModel

from app.utils.utils import get_project_image_cover_data


class Project(BaseModel):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    url = db.Column(db.String)
    date = db.Column(db.Date)
    type = db.Column(db.String)

    user = db.relationship("User", secondary="project_user", back_populates="projects")

    announcement_id = db.Column(db.Integer, db.ForeignKey("announcements.id"), nullable=True)
    announcement = db.relationship("Announcement", back_populates="projects")

    def to_json(self, user_id):
        project_user = ProjectUser.query.filter_by(user_id=user_id, project_id=self.id).first()
        project_cover_data = get_project_image_cover_data(self.id)

        data = {
            "id": self.id,
            "name": self.name,
            "user_role": project_user.user_role,
            "description": self.description,
            "image": str(project_cover_data),
            "date": str(self.date),
            "type": self.type
        }
        
        return data


class ProjectUser(BaseModel):
    __tablename__ = "project_user"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user_role = db.Column(db.String)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))