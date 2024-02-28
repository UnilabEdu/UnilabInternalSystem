from app.extensions import db
from app.models.base import BaseModel


class Announcement(BaseModel):
    __tablename__ = "announcements"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"))
    activity_type_id = db.Column(db.Integer, db.ForeignKey("activity_type.id"))
    registration_start = db.Column(db.Date)  # ?
    registration_end = db.Column(db.Date)  # ?
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    description = db.Column(db.Text)

    projects = db.relationship("Project", back_populates="announcement")
    certificates = db.relationship("Certificate", back_populates="announcement")
    lecturers = db.relationship("AnnouncementLecturer", backref="announcement_lecturers")


    @classmethod
    def get_all_announcements(cls):
        announcements = cls.query.all()

        all_announcements = [
            {
                "id": announcement.id,
                "name": announcement.name,
                "subject_id": announcement.subject_id,
                "activity_type_id": announcement.activity_type_id,
                "registration_start": str(announcement.registration_start),
                "registration_end": str(announcement.registration_end),
                "start_date": str(announcement.start_date),
                "end_date": str(announcement.end_date),
                "description": announcement.description,
                "lecturer_ids": [lecturer.id for lecturer in announcement.lecturers],
                "projects": [
                    {
                        "id": project.id,
                        "name": project.name,
                        "description": project.description,
                        "url": project.url,
                        "date": str(project.date),
                        "type": project.type
                    }
                    for project in announcement.projects
                ]
            }
            for announcement in announcements
        ]

        return all_announcements


class AnnouncementUser(BaseModel):
    __tablename__ = "announcement_user"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    announcement_id = db.Column(db.Integer, db.ForeignKey("announcements.id"))
    passed = db.Column(db.Boolean, default=False)


class AnnouncementLecturer(BaseModel):
    __tablename__ = "announcement_lecturers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    announcement_id = db.Column(db.Integer, db.ForeignKey("announcements.id"))


class AnnouncementForm(BaseModel):
    __tablename__ = "announcements_form"

    id = db.Column(db.Integer, primary_key=True)
    announcement_id = db.Column(db.Integer, db.ForeignKey("announcements.id"))
    form_id = db.Column(db.Integer, db.ForeignKey("forms.id"))

    def to_json(self):
        return {
            "id": self.id,
            "announcement_id": self.announcement_id,
            "form_id": self.form_id
        }


class ActivityType(BaseModel):
    __tablename__ = "activity_type"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
