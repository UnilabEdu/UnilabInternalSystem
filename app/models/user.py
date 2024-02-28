import uuid

from app.extensions import db
from app.models.base import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.questions import QuestionOption

class User(BaseModel):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)  #
    uuid = db.Column(db.String, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String)  #
    lastname = db.Column(db.String)  #
    email = db.Column(db.String)  #
    _password = db.Column("password", db.String)
    personal_id = db.Column(db.String)  #
    number = db.Column(db.String)  #
    date = db.Column(db.Date)  #
    gender = db.Column(db.String)  #
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"))  #
    region_id = db.Column(db.Integer, db.ForeignKey("regions.id"))  #
    city_id = db.Column(db.Integer, db.ForeignKey("cities.id"))  #
    address = db.Column(db.String)  #
    confirmed = db.Column(db.Boolean, default=False)
    reset_password = db.Column(db.Integer, default=False)

    about_me = db.Column(db.String)

    role = db.relationship("Role", secondary="user_roles", backref="roles")  #
    announcements = db.relationship("Announcement", secondary="announcement_user", backref="announcements")
    question = db.relationship("Question", backref="user")
    projects = db.relationship("Project", secondary="project_user", back_populates="user")
    certificates = db.relationship("Certificate", back_populates="user")
    subjects = db.relationship("Subject", secondary="subject_lecturer", back_populates="lecturers")

    # Pupil #
    school = db.Column(db.String)
    grade = db.Column(db.String)
    parent_name = db.Column(db.String)
    parent_lastname = db.Column(db.String)
    parent_number = db.Column(db.String)

    # student #
    university_id = db.Column(db.Integer, db.ForeignKey("universities.id"))
    faculty = db.Column(db.String)
    program = db.Column(db.String)
    semester = db.Column(db.String)
    degree_level = db.Column(db.String)

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
            "country_id": self.country_id,
            "region_id": self.region_id,
            "city_id": self.city_id,
            "address": self.address,
            "role": [role.name for role in self.role],
            "school": self.school,
            "grade": self.grade,
            "parent_name": self.parent_name,
            "parent_lastname": self.parent_lastname,
            "parent_number": self.parent_number,
            "university_id": self.university_id,
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


class Country(BaseModel):
    __tablename__ = "countries"

    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String)

    user = db.relationship("User", backref="country")


class Region(BaseModel):
    __tablename__ = "regions"

    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"))
    region_name = db.Column(db.String)

    user = db.relationship("User", backref="region")
    country = db.relationship("Country", backref="region")


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
