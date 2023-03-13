from flask_restful import Resource, reqparse, inputs
from app.models.user import User, Country, Region, City, University
from app.api.validators.authentication import check_validators
from app.api.validators.mail import create_key, send_email
from flask import render_template
from flask_jwt_extended import create_access_token


class RegistrationApi(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("name", required=True, type=str )
    parser.add_argument("lastname", required=True, type=str)
    parser.add_argument("email", required=True, type=str)
    parser.add_argument("number", required=True, type=str)
    parser.add_argument("personal_id", required=True, type=str)
    parser.add_argument("date", required=True, type=inputs.datetime_from_iso8601)
    parser.add_argument("gender", required=True, type=str)
   
    parser.add_argument("password", required=True, type=str )
    parser.add_argument("conf_password", required=True, type=str)

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

    parser.add_argument("terms", required=True, type=bool)

    
    


    def post(self):
        
        parser = self.parser.parse_args()
        validation = check_validators(parser, User)



        if validation:
            return validation
        

        new_user = User(
                        name=parser["name"], 
                        lastname = parser["lastname"], 
                        email = parser["email"],
                        password = parser["password"],
                        personal_id = parser["personal_id"],
                        number = parser["number"],
                        date = parser["date"],
                        gender = parser["gender"],
                        country_id = parser["country_id"],
                        region_id = parser["region_id"],
                        city_id = parser["city_id"],
                        address = parser["address"],
                        role = parser["role"],
                        school = parser["school"],
                        grade = parser["grade"],
                        parent_name = parser["parent_name"],
                        parent_lastname = parser["parent_lastname"],
                        parent_number = parser["parent_number"],  
                        university_id = parser["university_id"],
                        faculty = parser["faculty"],
                        program = parser["program"],
                        semester = parser["semester"],
                        degree_level = parser["degree_level"]
        
                    
                        )


        new_user.create()
        new_user.save()


        key = create_key(parser["email"])
        html = render_template('_activation_massage.html', key=key)
        
        send_email(subject = "Confirm your account", html=html, recipients=parser["email"])
        
        return "Success", 200


      


    def get(self):

        country = [{object.id:object.country_name} for object in Country.query.all()]
        region = [{object.id:object.region_name} for object in Region.query.all()]
        city = [{object.id:object.city_name} for object in City.query.all()]
        university = [{object.id:object.university_name} for object in University.query.all()]

        data = {
            "countries" : country,
            "regions" : region, 
            "cities" : city, 
            "universities" : university
        }

        return data, 200



class AuthorizationApi(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument("email", required=True, type=str )
    parser.add_argument("password", required=True, type=str)



    def post(self):

        parser = self.parser.parse_args()

        user = User.query.filter_by(email = parser["email"]).first()
    

        if user and user.check_password(parser["password"]):           
            access_token = create_access_token(identity = user.email)
            responce = {
                'access token':access_token
            }
            return  responce
        else:
            return "Password or mail is incorrect", 400
        












    




