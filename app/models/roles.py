from app.extensions import db
from app.models.base import BaseModel


class UserRole(BaseModel):

    __tablename__ = "user_roles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))



class Role(BaseModel):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    can_create_activity = db.Column(db.Boolean, default=False)
    can_create_subject = db.Column(db.Boolean, default=False)
    can_create_roles = db.Column(db.Boolean, default=False)
    can_edit_users = db.Column(db.Boolean, default=False)
    can_create_questions = db.Column(db.Boolean, default=False)
    can_view_questions = db.Column(db.Boolean, default=False)
    can_create_forms = db.Column(db.Boolean, default=False)
    can_create_certificates = db.Column(db.Boolean, default=False)


    @classmethod
    def get_roles(cls):
        query = cls.query.all()

        data = [
            {
                "id": role.id,
                "name": role.name,
                "can_create_activity": role.can_create_activity,
                "can_create_subject": role.can_create_subject,
                "can_create_roles": role.can_create_roles,
                "can_edit_users": role.can_edit_users,
                "can_create_questions": role.can_create_questions,
                "can_view_questions": role.can_view_questions,
                "can_create_forms": role.can_create_forms,
                "can_create_certificates": role.can_create_certificates
            }
            for role in query
        ]

        return data