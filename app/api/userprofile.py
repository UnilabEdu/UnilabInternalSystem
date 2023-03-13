from flask_restful import Resource, reqparse, inputs
from app.api.validators.authentication import check_validators
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User


class UserProfileApi(Resource):
    parser = reqparse.RequestParser()


    parser.add_argument("name", required=True, type=str )
    parser.add_argument("lastname", required=True, type=str)
    parser.add_argument("email", required=True, type=str)
    parser.add_argument("number", required=True, type=str)
    parser.add_argument("personal_id", required=True, type=str)
    parser.add_argument("date", required=True, type=inputs.datetime_from_iso8601)
    parser.add_argument("gender", required=True, type=str)
   
    parser.add_argument("password", required=True, type=str )
    parser.add_argument("password_new", required=True, type=str)

    parser.add_argument("country_id", required=True, type=int)
    parser.add_argument("region_id", required=True, type=int)
    parser.add_argument("city_id", required=True, type=int)
    parser.add_argument("address", required=True, type=str)

    parser.add_argument("role", required=True, type=str )

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

    parser.add_argument("terms", required=False, type=str, default=True)


    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()

        user = User.query.filter_by(email=current_user).first()

        user_data = {
            "name" : user.name,
            "lastname" : user.lastname ,
            "email" : user.email ,
            "number" : user.number ,
            "personal_id" : user.personal_id ,
            "date" : str(user.date) ,
            "country_id" : user.country_id ,
            "region_id" : user.region_id ,
            "city_id" : user.city_id ,
            "address" : user.address ,
            "role" : user.role ,
            "school" : user.school ,
            "grade" : user.grade ,
            "parent_name" : user.parent_name ,
            "parent_lastname" : user.parent_lastname ,
            "parent_number" : user.parent_number ,
            "university_id" : user.university_id ,
            "faculty" : user.faculty ,
            "program" : user.program ,
            "semester" : user.semester ,
            "degree_level" : user.degree_level 
           
        }

        return user_data, 200





    @jwt_required()
    def put(self):

        parser = self.parser.parse_args()
        validation = check_validators(parser, User, user_check = False)
        current_user = get_jwt_identity()

        if validation:
            return validation       


        user = User.query.filter_by(email=current_user).first()

        if user and user.check_password(parser["password"]):
        
            user.name = parser["name"]
            user.lastname = parser["lastname"]
            user.email = parser["email"]
            user.number = parser["number"]
            user.personal_id = parser["personal_id"]
            user.date = parser["date"]
            user.gender = parser["gender"]
            user.password = parser["password_new"]
            user.country_id = parser["country_id"]
            user.region_id = parser["region_id"]
            user.city_id = parser["city_id"]
            user.address = parser["address"]
            user.role = parser["role"]
            user.school = parser["school"]
            user.grade = parser["grade"]
            user.parent_name = parser["parent_name"]
            user.parent_lastname = parser["parent_lastname"]
            user.parent_number = parser["parent_number"]
            user.university_id = parser["university_id"]
            user.faculty = parser["faculty"]
            user.program = parser["program"]
            user.semester = parser["semester"]
            user.degree_level = parser["degree_level"]
        
            user.save()

            return "Success", 200

        return "Bad request", 400


