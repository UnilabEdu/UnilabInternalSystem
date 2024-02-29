from flask_restful import Resource, reqparse, inputs
from flask_jwt_extended import jwt_required, current_user
from app.models.user import User
from app.models import Announcement, AnnouncementForm, AnnouncementLecturer


class AnnouncementApi(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("name", required=True, type=str)
    parser.add_argument("subject_id", required=True, type=int)
    parser.add_argument("activity_type_id", required=True, type=int)
    parser.add_argument("lecturer_ids", required=True, action="append", type=dict)
    # parser.add_argument("registration_start", required=True, type=inputs.datetime_from_iso8601)
    # parser.add_argument("registration_end", required=True, type=inputs.datetime_from_iso8601)
    parser.add_argument("start_date", required=True, type=inputs.datetime_from_iso8601)
    parser.add_argument("end_date", required=True, type=inputs.datetime_from_iso8601)
    parser.add_argument("description", required=False, type=str)

    @jwt_required()
    def get(self):
        if not current_user.check_permission("can_create_activity"):
            return "You can't create or view announcements", 403

        announcements = Announcement.get_all_announcements()

        return announcements, 200

    @jwt_required()
    def post(self):
        request_parser = self.parser.parse_args()

        if not current_user.check_permission("can_create_activity"):
            return "You can't create Announcements", 403

        new_announcement = Announcement(
            name=request_parser["name"],
            subject_id=request_parser["subject_id"],
            activity_type_id=request_parser["activity_type_id"],
            # registration_start=request_parser["registration_start"],
            # registration_end=request_parser["registration_end"],
            start_date=request_parser["start_date"],
            end_date=request_parser["end_date"],
            description=request_parser["description"]
        )
        new_announcement.create()
        new_announcement.save()

        for lecturer in request_parser["lecturer_ids"]:
            announcement_user = AnnouncementLecturer(
                user_id=lecturer["id"],
                announcement_id=new_announcement.id
            )
            announcement_user.create()
        announcement_user.save()


        return "Successfully created an Announcement", 200

    @jwt_required()
    def put(self, id):
        result = Announcement.query.get(id)

        request_parser = self.parser.parse_args()

        if not current_user.check_permission("can_create_activity"):
            return "You can't create Announcements", 403


        if not result:
            return "Announcement not found", 404

        result.name = request_parser["name"]
        result.subject_id = request_parser["subject_id"]
        result.activity_type_id = request_parser["activity_type_id"]
        result.lecturer_id = request_parser["lecturer_id"]
        result.registration_start = request_parser["registration_start"]
        result.registration_end = request_parser["registration_end"]
        result.start_date = request_parser["start_date"]
        result.end_date = request_parser["end_date"]
        result.save()

        return "Successfully updated an Announcement", 200

    @jwt_required()
    def delete(self, id):
        result = Announcement.query.get(id)

        if not current_user.check_permission("can_create_activity"):
            return "You can't create or delete Announcements", 403


        if not result:
            return "Announcement not found", 404

        result.delete()
        result.save()

        return "Successfully deleted an Announcement", 200


class AnnouncementFormApi(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("announcement_id", required=True, type=int)
    parser.add_argument("form_id", required=True, type=int)

    @jwt_required()
    def get(self):
        if not current_user.check_permission("can_create_activity"):
            return "You can't create Announcement Forms", 403

        announcements = Announcement.get_all_announcements()

        return announcements, 200
    
    @jwt_required()
    def post(self):
        request_parser = self.parser.parse_args()

        if not current_user.check_permission("can_create_activity"):
            return "You can't create Announcement forms", 403

        new_announcement_form = AnnouncementForm(
            announcement_id=request_parser["announcement_id"],
            form_id=request_parser["form_id"],
        )
        new_announcement_form.create()
        new_announcement_form.save()

        return "Successfully created an Announcement form", 200