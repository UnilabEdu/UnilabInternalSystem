from flask_restful import Resource, reqparse, inputs
from app.models.user import User, Country
from app.models.roles import UserRole, Role
from app.api.validators.authentication import check_validators
from app.api.validators.mail import create_key, send_email
from flask import render_template
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity


class RegistrationApi(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("name", required=True, type=str)
    parser.add_argument("lastname", required=True, type=str)
    parser.add_argument("email", required=True, type=str)
    parser.add_argument("number", required=True, type=str)
    parser.add_argument("personal_id", required=True, type=str)
    parser.add_argument("date", required=True,
                        type=inputs.datetime_from_iso8601)
    parser.add_argument("gender", required=True, type=str)

    parser.add_argument("password", required=True, type=str)
    parser.add_argument("conf_password", required=True, type=str)

    parser.add_argument("country_id", required=True, type=int)
    parser.add_argument("region_id", required=True, type=int)
    parser.add_argument("city_id", required=True, type=int)
    parser.add_argument("address", required=True, type=str)

    parser.add_argument("role_id", required=True, type=int)

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

    parser.add_argument("terms", required=True, type=bool)

    def post(self):

        parser = self.parser.parse_args()
        validation = check_validators(parser)

        if validation:
            return validation
    
        new_user = User(
            name=parser["name"],
            lastname=parser["lastname"],
            email=parser["email"],
            password=parser["password"],
            personal_id=parser["personal_id"],
            number=parser["number"],
            date=parser["date"],
            gender=parser["gender"],
            country_id=parser["country_id"],
            region_id=parser["region_id"],
            city_id=parser["city_id"],
            address=parser["address"],
            school=parser["school"],
            grade=parser["grade"],
            parent_name=parser["parent_name"],
            parent_lastname=parser["parent_lastname"],
            parent_number=parser["parent_number"],
            university_id=parser["university_id"],
            faculty=parser["faculty"],
            program=parser["program"],
            semester=parser["semester"],
            degree_level=parser["degree_level"]
        )

        new_user.create()
        new_user.save()

        
        new_user_role = UserRole(user_id=new_user.id, role_id=parser["role_id"])

        new_user_role.create()
        new_user_role.save()

        key = create_key(parser["email"])
        html = render_template('_activation_massage.html', key=key)

        send_email(subject="Confirm your account",
                html=html, recipients=parser["email"])

        return "Successfully registered a User", 200
        

    def get(self):

        locations = Country.get_locations()
        roles = Role.get_roles()

        data = {
            "locations": locations,
            "roles": roles
        }

        return data, 200


class AuthorizationApi(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument("email", required=True, type=str)
    parser.add_argument("password", required=True, type=str)

    def post(self):

        parser = self.parser.parse_args()

        user = User.query.filter_by(email=parser["email"]).first()

        if user and user.check_password(parser["password"]):
            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)
            responce = {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
            return responce
        else:
            return "Password or mail is incorrect", 400


class AccessTokenRefreshApi(Resource):

    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        response = {
            "access_token": access_token
        }

        return response
