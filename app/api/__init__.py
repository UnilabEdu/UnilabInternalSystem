from flask_restful import Api
from app.api.authentication import RegistrationApi, AuthorizationApi, AccessTokenRefreshApi
from app.api.mailconfirmation import SendConfirmEmailApi, ReceiveConfirmEmailApi
from app.api.registration_activities import RegistrationActivitiesApi
from app.api.userprofile import UserProfileApi
from app.api.roles import RolesApi
from app.api.announcement import AnnouncementApi, AnnouncementFormApi
from app.api.questions import QuestionApi, FormApi, UserAnswerApi, QuestionFormApi
from app.api.certificate import CertificateApi
from app.api.subjects import SubjectApi
from app.api.projects import ProjectApi
from app.api.portfolio import PortfolioApi


api = Api()
api.add_resource(RegistrationApi, "/api/registration")
api.add_resource(AuthorizationApi, "/api/authorization")
api.add_resource(AccessTokenRefreshApi, "/api/refresh_access_token")
api.add_resource(SendConfirmEmailApi, "/api/send_confirm_email")
api.add_resource(ReceiveConfirmEmailApi, "/api/receive_confirm_email")
api.add_resource(UserProfileApi, "/api/user_profile")
api.add_resource(RolesApi, "/api/roles")
api.add_resource(AnnouncementApi, "/api/announcement", "/api/announcement/<int:id>")
api.add_resource(AnnouncementFormApi, "/api/announcement_form")
api.add_resource(QuestionApi, "/api/question")
api.add_resource(QuestionFormApi, "/api/question_form")
api.add_resource(RegistrationActivitiesApi, "/api/registration_activities")
api.add_resource(FormApi, "/api/form")
api.add_resource(UserAnswerApi, "/api/user_answer")
api.add_resource(CertificateApi, "/api/certificate")
api.add_resource(ProjectApi, "/api/project")
api.add_resource(SubjectApi, "/api/subject")
api.add_resource(PortfolioApi, "/api/portfolio", "/api/portfolio/<string:uuid>")