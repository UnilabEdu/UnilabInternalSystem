from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, current_user

from app.extensions import db
from app.models import User, Project


class PortfolioApi(Resource):

    @jwt_required()
    def get(self, uuid):
        user: User = User.query.filter_by(uuid=uuid).first()

        if user:
            project = Project.query.join(Project.user).filter(User.uuid == uuid).first()

            data = {
                "fullname": user.name + user.lastname,
                "email": user.email,
                "role": project.announcement.name,
                "about_me": user.about_me,
                "projects": [project.to_json(user.id) for project in user.projects]
            }

            return data, 200
        
        return "Invalid user", 400
    