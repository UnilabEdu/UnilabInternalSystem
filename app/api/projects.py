import os
import uuid
import werkzeug
import mimetypes

from datetime import datetime

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, current_user

from app.models import Project, ProjectUser
from app.config import Config


class ProjectApi(Resource):
    parser = reqparse.RequestParser()   
    parser.add_argument("name", required=True, type=str, location="form")
    parser.add_argument("description", required=True, type=str, location="form")
    parser.add_argument("url", required=False, type=str, location="form")
    parser.add_argument("type", required=True, type=str, location="form")
    parser.add_argument("user_role", required=True, type=str, location="form")
    parser.add_argument("images", required=True, type=werkzeug.datastructures.FileStorage, location="files", action="append")

    @jwt_required()
    def post(self):
        request_parser = self.parser.parse_args()

        image_types = ["image/jpeg", "image/png", "image/jpg"]

        images = [image for image in request_parser["images"] if image.mimetype in image_types]

        if len(images) == len(request_parser["images"]):
            date = datetime.now()

            project = Project(
                name=request_parser["name"],
                description=request_parser["description"],
                url=request_parser["url"],
                date=date,
                type=request_parser["type"],
                # announcement_id=1
            )   
            project.create()
            project.save()

            project_user = ProjectUser(
                user_id=current_user.id,
                user_role=request_parser["user_role"],
                project_id=project.id
            )
            project_user.create()
            project_user.save()

            images_directory = os.path.join(Config.BASE_DIR + '/app', "images", str(project.id))
            os.makedirs(images_directory, exist_ok=True) 

            for image in images:
                extension = mimetypes.guess_extension(image.mimetype) or ".jpg"
                
                file_name = str(uuid.uuid4()) + extension
                image_path = os.path.join(images_directory, file_name)
                image.save(image_path)

            return "Project was created successfully", 200

        return "File was sent which wasn't an image", 400