from flask_restful import Resource, reqparse, inputs
from app.api.validators.authentication import check_validators
from flask_jwt_extended import jwt_required, current_user


class UserProfileApi(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument("name", required=True, type=str)
    parser.add_argument("lastname", required=True, type=str)
    parser.add_argument("email", required=True, type=str)
    parser.add_argument("number", required=True, type=str)
    parser.add_argument("personal_id", required=True, type=str)
    parser.add_argument("date", required=True,type=inputs.datetime_from_iso8601)
    parser.add_argument("gender", required=True, type=str)

    parser.add_argument("password", required=True, type=str)
    parser.add_argument("password_new", required=True, type=str)

    parser.add_argument("country_id", required=True, type=int)
    parser.add_argument("region_id", required=True, type=int)
    parser.add_argument("city_id", required=True, type=int)
    parser.add_argument("address", required=True, type=str)

    parser.add_argument("school", required=True, type=str)
    parser.add_argument("grade", required=True, type=str)
    parser.add_argument("parent_name", required=True, type=str)
    parser.add_argument("parent_lastname", required=True, type=str)
    parser.add_argument("parent_number", required=True, type=str)

    parser.add_argument("university_id", required=True, type=int)
    parser.add_argument("faculty", required=True, type=str)
    parser.add_argument("program", required=True, type=str)
    parser.add_argument("semester", required=True, type=str)
    parser.add_argument("degree_level", required=True, type=str)

    parser.add_argument("about_me", required=True, type=str)

    parser.add_argument("terms", required=False, type=str, default=True)

    @jwt_required()
    def get(self):
        if current_user:
            user_data = current_user.to_json()
            return user_data, 200

        return "User not found", 404

    @jwt_required()
    def put(self):

        parser = self.parser.parse_args()
        validation = check_validators(parser, user_check=False, role_check = False)

        if validation:
            return validation

        if current_user and current_user.check_password(parser["password"]):

            current_user.name = parser["name"]
            current_user.lastname = parser["lastname"]
            current_user.email = parser["email"]
            current_user.number = parser["number"]
            current_user.personal_id = parser["personal_id"]
            current_user.date = parser["date"]
            current_user.gender = parser["gender"]
            current_user.password = parser["password_new"]
            current_user.country_id = parser["country_id"]
            current_user.region_id = parser["region_id"]
            current_user.city_id = parser["city_id"]
            current_user.address = parser["address"]
            current_user.school = parser["school"]
            current_user.grade = parser["grade"]
            current_user.parent_name = parser["parent_name"]
            current_user.parent_lastname = parser["parent_lastname"]
            current_user.parent_number = parser["parent_number"]
            current_user.university_id = parser["university_id"]
            current_user.faculty = parser["faculty"]
            current_user.program = parser["program"]
            current_user.semester = parser["semester"]
            current_user.degree_level = parser["degree_level"]
            current_user.about_me = parser["about_me"]

            current_user.save()

            return "Successfully updated User's profile", 200

        return "Bad request", 400
