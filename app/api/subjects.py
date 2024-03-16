from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, current_user
from flask import request
from uuid import uuid4
from os import path

from app.models import Subject, SubjectLecturer
from app import Config

SYLLABUS_NAMES = ["course_syllabus", "internship_syllabus", "tlt_syllabus", "school_syllabus"]


class SubjectApi(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", required=True, location="form")
    parser.add_argument("lecturers_id", required=True, type=int, action="append", location="form")
    parser.add_argument("course_syllabus", type=str, location="files")
    parser.add_argument("internship_syllabus", type=str, location="files")
    parser.add_argument("tlt_syllabus", type=str, location="files")
    parser.add_argument("school_syllabus", type=str, location="files")
    # Additional Links

    @jwt_required()
    def post(self):
        request_parser = self.parser.parse_args()
        syllabus_list = [
            request_parser["course_syllabus"],
            request_parser["internship_syllabus"],
            request_parser["tlt_syllabus"],
            request_parser["school_syllabus"],
        ]

        print(syllabus_list)

        if not current_user.check_permission("can_create_subject"):
            return "You can't create Subjects", 403

        if not any(syllabus_list):
            return "At least one syllabus must be sent", 400

        syllabus_names = []
        for syllabus in SYLLABUS_NAMES:
            file = request.files[syllabus]

            if file.filename == "":
                syllabus_names.append(None)
                continue

            if file.filename.lower().endswith(".pdf"):
                name = str(uuid4())
                file.save(path.join(Config.BASE_DIR, "app", "files", f"{name}.pdf"))
                syllabus_names.append(name)
            else:
                return "Only PDF format is allowed!", 400

        print(syllabus_names)

        new_subject = Subject(
            name=request_parser["name"],
            course_syllabus=syllabus_names[0],
            internship_syllabus=syllabus_names[1],
            tlt_syllabus=syllabus_names[2],
            school_syllabus=syllabus_names[3],
            # Additional Links
        )
        new_subject.create()
        new_subject.save()

        for lecturer_id in request_parser["lecturers_id"]:
            subject_lecturer = SubjectLecturer(
                user_id=lecturer_id,
                subject_id=new_subject.id,
            )
            subject_lecturer.create()
        subject_lecturer.save()

        return "Successfully created a Subject", 200