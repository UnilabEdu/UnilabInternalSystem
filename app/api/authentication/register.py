from flask_restx import Resource, fields, reqparse, inputs
from flask import render_template

from app.models import User, UserRole
from app.api.validators import check_validators
from app.utils.mail import create_key, send_email
from app.api.authentication import auth_ns

registration_model = auth_ns.model('Registration', {
    'firstname': fields.String(required=True, description='First name', example='გიორგი'),
    'surname': fields.String(required=True, description='Last name', example='გვარაძე'),
    'email': fields.String(required=True, description='Email address', example='giorgi.gvaradze@gmail.com'),
    'number': fields.String(required=True, description='Phone number', example='598123456'),
    'personal_id': fields.String(required=True, description='Personal ID', example='01234567891'),
    'date': fields.DateTime(required=True, description='Date of birth', dt_format='iso8601',example='2024-06-25T15:22:57.338Z'),
    'gender': fields.String(required=True, description='Gender', example='მამრობითი',enum =["მდედრობითი","მამრობითი",]),
    'password': fields.String(required=True, description='Password', example='password'),
    'region_id': fields.Integer(required=True, description='Region ID', example=11),
    'city_id': fields.Integer(required=True, description='City ID', example=2),
    'address': fields.String(required=True, description='Address', example='მისამართი..'),
    'status': fields.String(required=True, description='Status', example='student', enum=['pupil', 'student', 'graduate', 'other']),
    'terms_agreed': fields.Boolean(required=True, description='Agree to terms and conditions', example=True),
    'role_id': fields.Integer(required=True, description='Role ID', example=2),

    # Pupil fields
    'school_id': fields.Integer(required=False, example=1),
    'grade': fields.String(required=False, example="10"),
    'parent_name': fields.String(required=False, example="დავითი"),
    'parent_lastname': fields.String(required=False, example="გვარაძე"),
    'parent_number': fields.String(required=False, example="599243115"),

    # Student/Graduate fields
    'university_id': fields.Integer(required=False, example=1),
    'faculty': fields.String(required=False, example="კომპიუტერული მეცნიერება"),
    'program': fields.String(required=False, example="Ml modeling"),
    'semester': fields.String(required=False, example="ზაფხული 2024"),
    'degree_level': fields.String(required=False, example="მაგისტრი"),
    'completion_date': fields.DateTime(required=False, dt_format='iso8601', example='2025-07-01T00:00:00.000Z'),
})

parser = reqparse.RequestParser()
parser.add_argument("firstname", required=True, type=str, help="Name example: Giorgi (1-50 characters)", location ='json')
parser.add_argument("surname", required=True, type=str, help="Last name example: Saldadze ", location ='json')
parser.add_argument("email", required=True, type=str, help="Email example: example@example.com ", location ='json')
parser.add_argument("number", required=True, type=str, help="Phone number example: 123456789", location ='json')
parser.add_argument("personal_id", required=True, type=str, help="Personal ID example: 12345678901 (11 characters)", location ='json')
parser.add_argument("date", required=True, type=inputs.datetime_from_iso8601, help="Date of birth example: YYYY-MM-DD", location ='json')
parser.add_argument("gender", required=True, type=str, help="Gender example: Male/Female", location ='json')
parser.add_argument("password", required=True, type=str, help="Password example: password", location ='json')

parser.add_argument("region_id", required=True, type=int, help="Region ID example: 11 (cities and regions should be a match)", location ='json')
parser.add_argument("city_id", required=True, type=int, help="City ID example: 2 (cities and regions should be a match)", location ='json')
parser.add_argument("address", required=True, type=str, help="Address example: 123 Main St", location ='json')
parser.add_argument("status", required=True, type=str, help="User status. Determines which additional fields are required. Choose one of: 'pupil', 'student', 'graduate', 'other'.", choices=('pupil', 'student', 'graduate', 'other'), location='json')
parser.add_argument("terms_agreed", required=True, type=inputs.boolean, help="You must agree to the terms and conditions by checking the box", location='json')

parser.add_argument("role_id", required=True, type=int, help="Role ID example: 2  (1- is for admin)", location ='json')

parser.add_argument("school_id", required=False, nullable=True, type=int, help="School example: High School", location ='json')
parser.add_argument("grade", required=False, nullable=True, type=str, help="Grade example: 10th Grade ", location ='json')
parser.add_argument("parent_name", required=False, nullable=True, type=str, help="Parent's name example: John ", location ='json')
parser.add_argument("parent_lastname", required=False, nullable=True, type=str, help="Parent's last name example: Doe ", location ='json')
parser.add_argument("parent_number", required=False, nullable=True, type=str, help="Parent's phone number example: 123456789 ", location ='json')

parser.add_argument("university_id", required=False, nullable=True, type=int, help="University ID example: 1", location ='json')
parser.add_argument("faculty", required=False, nullable=True, type=str, help="Faculty example: Engineering ", location ='json')
parser.add_argument("program", required=False, nullable=True, type=str, help="Program example: Computer Science", location ='json')
parser.add_argument("semester", required=False, nullable=True, type=str, help="Semester example: 1st Semester ", location ='json')
parser.add_argument("degree_level", required=False, nullable=True, type=str, help="Degree level example: Bachelor", location ='json')
parser.add_argument("completion_date", required=False, type=inputs.datetime_from_iso8601, help="Completion date example: 2024-06-25T15:22:57.338Z (visible only for Graduates)", location='json')

@auth_ns.route('/register')
@auth_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
@auth_ns.expect(registration_model)
class RegistrationApi(Resource):
    @auth_ns.doc(parser=parser)
    def post(self):
        args = parser.parse_args()

        if not args["terms_agreed"]:
            return "უნდა დაეთანხმოთ წესებს და პირობებს", 400

        # Validate conditional fields
        status = args["status"]
        if status == "pupil":
            required_fields = ["school_id", "grade", "parent_name", "parent_lastname", "parent_number"]
        elif status == "student":
            required_fields = ["university_id", "faculty", "program", "semester", "degree_level"]
        else:
            required_fields = []

        for field in required_fields:
            if not args.get(field):
                return f"{field} ველი სავალდებულოა ამ სტატუსისთვის", 400

        validation = check_validators(args)
        if validation:
            return validation

        new_user = User(
            name=args["firstname"],
            lastname=args["surname"],
            email=args["email"],
            password=args["password"],
            personal_id=args["personal_id"],
            number=args["number"],
            date=args["date"],
            gender=args["gender"],
            region_id=args["region_id"],
            city_id=args["city_id"],
            address=args["address"],
            school_id=args["school_id"],
            grade=args["grade"],
            parent_name=args["parent_name"],
            parent_lastname=args["parent_lastname"],
            parent_number=args["parent_number"],
            university_id=args["university_id"],
            faculty=args["faculty"],
            program=args["program"],
            semester=args["semester"],
            degree_level=args["degree_level"],
            completion_date=args["completion_date"]
        )

        new_user.create()
        new_user.save()

        # Default role for self-registration
        new_user_role = UserRole(user_id=new_user.id, role_id=args["role_id"])
        new_user_role.create()
        new_user_role.save()

        key = create_key(args["email"])
        html = render_template('_activation_massage.html', key=key)
        send_email(subject="Confirm your account", html=html, recipients=args["email"])

        return f"/confirm_account/{key}", 200 # TODO: Remove token once we move to production


# {
#   "firstname": "გიორგი",
#   "surname": "გვარაძე",
#   "email": "giorgi.gvaradze@gmail.com",
#   "number": "598123456",
#   "personal_id": "01234567891",
#   "date": "2024-06-25T15:22:57.338Z",
#   "gender": "მამრობითი",
#   "password": "password",
#   "region_id": 11,
#   "city_id": 2,
#   "address": "მისამართი..",
#   "status": "student",
#   "terms_agreed": true,
#   "role_id": 2,
#   "school_id": 1,
#   "grade": "10",
#   "parent_name": "დავითი",
#   "parent_lastname": "გვარაძე",
#   "parent_number": "599243115",
#   "university_id": 1,
#   "faculty": "კომპიუტერული მეცნიერება",
#   "program": "Ml modeling",
#   "semester": "ზაფხული 2024",
#   "degree_level": "მაგისტრი",
#   "completion_date": "2025-07-01T00:00:00.000Z"
# }