import uuid

from app.extensions import db
from app.models.base import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.questions import QuestionOption


class User(BaseModel):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String)
    _password = db.Column("password", db.String)
    personal_id = db.Column(db.String)
    number = db.Column(db.String)
    date = db.Column(db.Date)
    gender = db.Column(db.String)
    region_id = db.Column(db.Integer, db.ForeignKey("regions.id"))
    city_id = db.Column(db.Integer, db.ForeignKey("cities.id"))
    address = db.Column(db.String)
    confirmed = db.Column(db.Boolean, default=False)
    reset_password = db.Column(db.Integer, default=False)

    about_me = db.Column(db.String, nullable=True)

    role = db.relationship("Role", secondary="user_roles", backref="roles")
    announcements = db.relationship("Announcement", secondary="announcement_user", backref="announcements")
    question = db.relationship("Question", backref="user")
    projects = db.relationship("Project", secondary="project_user", back_populates="user")
    certificates = db.relationship("Certificate", back_populates="user")
    subjects = db.relationship("Subject", secondary="subject_lecturer", back_populates="lecturers")

    # status #
    status = db.Column(db.String, nullable=True)
    terms_accepted = db.Column(db.Boolean, default=True)

    # Pupil #
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=True)
    grade = db.Column(db.String, nullable=True)
    parent_name = db.Column(db.String, nullable=True)
    parent_lastname = db.Column(db.String, nullable=True)
    parent_number = db.Column(db.String, nullable=True)

    # student #
    university_id = db.Column(db.Integer, db.ForeignKey("universities.id"), nullable=True)
    faculty = db.Column(db.String, nullable=True)
    program = db.Column(db.String, nullable=True)
    semester = db.Column(db.String, nullable=True)
    degree_level = db.Column(db.String, nullable=True)

    # graduated #
    # it is same as in student, but we add completion time
    completion_date = db.Column(db.DateTime, nullable=True)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    password = db.synonym('_password', descriptor=property(
        _get_password, _set_password))

    def check_permission(self, request):
        permisions = [getattr(permision, request) for permision in self.role]
        return any(permisions)

    def is_admin(self):
        return any(role.name == "ადმინი" for role in self.role)

    def has_role(self, role_name):
        return any(role.name == role_name for role in self.role)

    def to_json(self):
        user_data = {
            "id": self.id,
            "uuid": self.uuid,
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email,
            "number": self.number,
            "personal_id": self.personal_id,
            "date": str(self.date),
            "gender": self.gender,

            "region": {
                "id": self.region_id,
                "name": Region.query.get(self.region_id).region_name
            },
            "city": {
                "id": self.city_id,
                "name": City.query.get(self.city_id).city_name
            },
            "university": {
                "id": self.university_id,
                "name": University.query.get(self.university_id).university_name
            },
            "address": self.address,
            "role": [
                {"id": role.id, "name": role.name}
                for role in self.role
            ],
            "school_id": self.school_id,
            "grade": self.grade,
            "parent_name": self.parent_name,
            "parent_lastname": self.parent_lastname,
            "parent_number": self.parent_number,
            "faculty": self.faculty,
            "program": self.program,
            "semester": self.semester,
            "degree_level": self.degree_level,
            "projects": [project for project in self.projects],
            "about_me": self.about_me
        }

        return user_data


class UserAnswer(BaseModel):
    __tablename__ = "user_answers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    form_id = db.Column(db.Integer, db.ForeignKey("forms.id"))
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"))
    answer = db.Column(db.String)
    is_correct = db.Column(db.Boolean, nullable=True)

    @classmethod
    def get_correct_answer(cls, question_id):
        correct_answer = QuestionOption.query.filter_by(question_id=question_id, is_correct=True).first()

        return correct_answer

    def to_json(self):
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "form_id": self.form_id,
            "question_id": self.question_id,
            "answer": self.answer,
            "is_correct": self.is_correct
        }

        return data


class Region(BaseModel):
    __tablename__ = "regions"

    id = db.Column(db.Integer, primary_key=True)
    region_name = db.Column(db.String)

    user = db.relationship("User", backref="region")

    @classmethod
    def get_locations(self):
        regions = Region.query.all()
        locations = []

        for region in regions:
            region_data = {
                "id": region.id,
                "name": region.region_name,
                "cities": [
                    {
                        "id": city.id,
                        "name": city.city_name
                    }
                    for city in City.query.filter_by(region_id=region.id).all()
                ]
            }
            locations.append(region_data)

        return {"locations": locations}, 200


class City(BaseModel):
    __tablename__ = "cities"

    id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, db.ForeignKey("regions.id"))
    city_name = db.Column(db.String)

    user = db.relationship("User", backref="city")
    region = db.relationship("Region", backref="city")


class University(BaseModel):
    __tablename__ = "universities"

    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey("cities.id"))
    university_name = db.Column(db.String)

    user = db.relationship("User", backref="university")
    city = db.relationship("City", backref="university")

    @classmethod
    def get_universities(cls, city_id):
        universities = []
        for university in cls.query.filter_by(city_id=city_id).all():
            universities.append({"id": university.id, "name": university.university_name})
        return universities


class School(BaseModel):
    __tablename__ = "schools"

    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey("cities.id"))
    school_name = db.Column(db.String)

    city = db.relationship("City", backref="school")

    @classmethod
    def get_schools(cls, city_id):
        schools = []
        for school_1 in cls.query.filter_by(city_id=city_id).all():
            schools.append({"id": school_1.id, "name": school_1.school_name})
        return schools

class Certificate(BaseModel):
    __tablename__ = "certificates"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="certificates")

    announcement_id = db.Column(db.Integer, db.ForeignKey("announcements.id"))
    announcement = db.relationship("Announcement", back_populates="certificates")

    def to_json(self):
        certificate_data = {
            "id": self.id,
            "user_id": self.user_id,
            "announcement_id": self.announcement_id,
        }

        return certificate_data



