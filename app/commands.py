from flask.cli import with_appcontext
from app.extensions import db
from app.models import User, Country, Region, City, University
from app.models import Role, UserRole
from app.models import ActivityType, Subject, Announcement, AnnouncementUser
from app.models import Question, QuestionOption
from data import user_data
from datetime import datetime
import click


@click.command("init_db")
@with_appcontext
def init_db():
    click.echo("Database Creation in Progress...")
    db.drop_all()
    db.create_all()
    click.echo("Database Created!")


@click.command("populate_db")
@with_appcontext
def populate_db():
    click.echo("Creating Initial Entries...")

    # populating country table
    countries = [
        "საქართველო", "საფრანგეთი",
        "გერმანია", "ავსტრია", "დიდი ბრიტანეთი"
    ]
    for country in countries:
        country_ = Country(country_name=country)
        country_.create()
    country_.save()

    # populating region table
    regions = [
        "გურია", "იმერეთი", "კახეთი", 
        "მცხეთა-მთიანეთი", "რაჭა-ლეჩხუმისა და ქვემო სვანეთი", 
        "სამეგრელო-ზემო სვანეთი", "სამცხე-ჯავახეთი",
        "ქვემო ქართლი", "შიდა ქართლი", "აჭარა", "თბილისი"
    ]
    for region in regions:
        region_ = Region(region_name=region, country_id=1)
        region_.create()
    region_.save()

    # populating city table
    cities = [
        {"name": "ქუთაისი", "region_id": 2},
        {"name": "თბილისი", "region_id": 11},
        {"name": "ზუგდიდი", "region_id": 6},
        {"name": "ბათუმი", "region_id": 10},
        {"name": "გორი", "region_id": 9},
    ]
    for city in cities:
        city_ = City(
            city_name=city["name"], 
            region_id=city["region_id"]
        )
        city_.create()
    city_.save()

    # populating university table
    universities = [
        {"name": "ილიაუნი", "city_id": 2},
        {"name": "თსუ", "city_id": 2},
        {"name": "თსსუ", "city_id": 2},
        {"name": "გტუ", "city_id": 2},
        {"name": "სამხატვრო", "city_id": 2},
    ]
    for university in universities:
        university_ = University(
            university_name=university["name"], 
            city_id=university["city_id"]
        )
        university_.create()
    university_.save()

    # populating roles table
    role_ = Role(name="ადმინი", can_create_activity=True,
                 can_create_subject=True, can_create_roles=True, can_edit_users=True,
                 can_create_questions=True, can_view_questions=True, 
                 can_create_forms=True, can_create_certificates=True)
    role_.create()
    role_ = Role(name="სტუდენტი")
    role_.create()
    role_ = Role(name="ლექტორი", can_create_activity=True,
                 can_create_subject=True, can_create_roles=False,can_create_questions=True, 
                 can_view_questions=True, can_create_certificates=True, can_create_forms=True)
    role_.create()
    role_ = Role(name="მოდერატორი", can_create_activity=True,
                 can_create_subject=True, can_edit_users=True)
    role_.create()
    role_ = Role(name="მოსწავლე")
    role_.create()
    role_.save()

    # populating subjects
    subjects = ["პითონი", "HTML/CSS", "ჯავასკრიპტი", "C++"]
    for subject in subjects:
        subject_ = Subject(name=subject)
        subject_.create()
    subject_.save()

    # populating type
    types = ["კურსი", "სტაჟირება", "სასკოლო კურსი"]
    for type in types:
        type_ = ActivityType(name=type)
        type_.create()
    type_.save()

    for user in user_data:
        user_ = User(
            name=user["name"],
            lastname=user["lastname"],
            email=user["email"],
            number=user["number"],
            personal_id=user["personal_id"],
            date=datetime.now(),
            gender=user["gender"],
            password=user["password"],
            country_id=user["country_id"],
            region_id=user["region_id"],
            city_id=user["city_id"],
            address=user["address"],
            school=user["school"],
            grade=user["grade"],
            parent_name=user["parent_name"],
            parent_lastname=user["parent_lastname"],
            parent_number=user["parent_number"],
            university_id=user["university_id"],
            faculty=user["faculty"],
            program=user["program"],
            semester=user["semester"],
            degree_level=user["degree_level"],
        )
        user_.create()
        user_.save()

        user_role = UserRole(
            user_id=user_.id,
            role_id=user["role"],
        )
        user_role.create()

        user_role = UserRole(
            user_id=user_.id,
            role_id=4,
        )
        user_role.create()

        user_role.save()

    click.echo("Entries Created!")
