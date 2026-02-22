from datetime import date

from flask_jwt_extended import jwt_required, current_user
from flask_restx import Resource

from app.api.announcements import announcement_ns, announcement_model, parser
from app.models import User, Announcement, AnnouncementLecturer

@announcement_ns.route('/announcement')
@announcement_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class AnnouncementApi(Resource):
    @jwt_required()
    @announcement_ns.doc(security='JsonWebToken')
    def get(self):
        current_date = date.today()

        active_contests = Announcement.query.filter(
            Announcement.registration_start < current_date,
            Announcement.registration_end >= current_date
        ).all()

        ongoing_activities = Announcement.query.filter(
            Announcement.start_date < current_date,
            Announcement.end_date >= current_date
        ).all()

        active_contests_data = [
            {"id": contest.id, "name": contest.name} for contest in active_contests
        ]
        ongoing_activities_data = [
            {"id": activity.id, "name": activity.name} for activity in ongoing_activities
        ]

        registration_activities = {
            "active_contests": active_contests_data,
            "ongoing_activities": ongoing_activities_data
        }

        return registration_activities, 200

    @jwt_required()
    @announcement_ns.doc(security='JsonWebToken')
    @announcement_ns.expect(announcement_model)
    def post(self):
        args = parser.parse_args()

        if not current_user.check_permission("can_create_activity"):
            return "თქვენ არ გაქვთ აქთივობის შექმნის უფლება", 403

        new_announcement = Announcement(
            name=args["name"],
            subject_id=args["subject_id"],
            activity_type_id=args["activity_type_id"],
            registration_start=args["registration_start"],
            registration_end=args["registration_end"],
            start_date=args["start_date"],
            end_date=args["end_date"]
        )
        new_announcement.create()
        new_announcement.save()

        lecturer_ids = args["lecturer_ids"]
        for lecturer_id in lecturer_ids:
            lecturer = User.query.filter_by(id=lecturer_id).first()
            if not lecturer:
                print(f"User with ID {lecturer_id} does not exist")
                return f"მომხმარებელი აიდით {lecturer_id} არ არსებობს", 400

            if not lecturer.has_role("ლექტორი"):
                print(f"User with ID {lecturer_id} is not a lecturer")
                return f"მომხარებელი აიდით {lecturer_id} არ არის ლექტორი", 400

            announcement_user = AnnouncementLecturer(
                user_id=lecturer_id,
                announcement_id=new_announcement.id
            )
            announcement_user.create()
            announcement_user.save()

        return 200

@announcement_ns.route('/announcement/<int:id>')
@announcement_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class AnnouncementApi(Resource):
    @jwt_required()
    @announcement_ns.doc(security='JsonWebToken')
    @announcement_ns.expect(announcement_model)
    def put(self, id):

        if not current_user.check_permission("can_create_activity"):
            return "You can't create Announcements", 403

        args = parser.parse_args()

        result = Announcement.query.get(id)

        if not result:
            return "აქტივობა ვერ მოიძებნა", 404

        result.name = args["name"]
        result.subject_id = args["subject_id"]
        result.activity_type_id = args["activity_type_id"]
        result.registration_start = args["registration_start"]
        result.registration_end = args["registration_end"]
        result.start_date = args["start_date"]
        result.end_date = args["end_date"]

        result.save()

        lecturer_ids = args["lecturer_ids"]
        for lecturer_id in lecturer_ids:
            lecturer = User.query.filter_by(id=lecturer_id).first()
            if not lecturer:
                print(f"User with ID {lecturer_id} does not exist")
                return f"მომხმარებელი აიდით {lecturer_id} არ არსებობს", 400

            # print(f"Checking roles for User ID {lecturer_id}")
            # print(f"User roles: {[role.name for role in lecturer.role]}")

            if not lecturer.has_role("ლექტორი"):
                print(f"User with ID {lecturer_id} is not a lecturer")
                return f"მომხარებელი აიდით {lecturer_id} არ არის ლექტორი", 400

            announcement_user = AnnouncementLecturer(
                user_id=lecturer_id,
                announcement_id=result.id
            )
            announcement_user.create()
            announcement_user.save()

        return 200

    @jwt_required()
    @announcement_ns.doc(security='JsonWebToken')
    def delete(self, id):
        announcement = Announcement.query.get(id)
        if not announcement:
            return "აქტივობა ვერ მოიძებნა", 404

        if not current_user.check_permission("can_create_activity"):
            return "თქვენ არ გაქვთ აქტივობის წაშლის უფლება", 403

        announcement.delete()
        announcement.save()
        return 200


# announcement details API
@announcement_ns.route('/announcement/<int:id>/details')
@announcement_ns.doc(responses={200: 'OK', 404: 'Not Found'})
class AnnouncementDetailsApi(Resource):
    @jwt_required()
    @announcement_ns.doc(security='JsonWebToken')
    def get(self, id):

        announcement = Announcement.query.get(id)
        if not announcement:
            return {"message": "კურსი ვერ მოიძებნა"}, 404

        lecturer_data = []
        for lecturer_list in announcement.lecturers:
            lecturer = User.query.get(lecturer_list.user_id)
            if lecturer:
                lecturer_data.append({
                    "id": lecturer.id,
                    "full_name": f"{lecturer.name} {lecturer.lastname}",
                    "description": lecturer.about_me,
                    "image": lecturer.profile_image
                })

        return {
            "id": announcement.id,
            "name": announcement.name,
            "description": announcement.description,
            "lecturers": lecturer_data,
            "syllabus_pdf": announcement.syllabus_pdf
        }, 200