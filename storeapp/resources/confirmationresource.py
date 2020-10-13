from flask_restful import Resource
from storeapp.models.usermodel import UserModel, ConfirmationModel
from flask import make_response, render_template
from storeapp.mail.emailsender import send_email_confirmation, MailGunException

INVALID_CONFIRMATION_TOKEN = "Invalid confirmation token passed"
TOKEN_EXPIRED = "Token has expired"
INVALID_USER = "Invalid user id passed"
USER_ACTIVATED = "User is already active"
EMAIL_SENT = "Registration email resent successfully"
EMAIL_SEND_FAILED = "Registration email resend failed"

class ConfirmationResource(Resource):

    @classmethod
    def get(cls, token: str):
        confirmation = ConfirmationModel.find_by_id(token)
        if (confirmation):
            if(confirmation.expired()):
                 return {"message":TOKEN_EXPIRED}, 400
            else:
                user = confirmation.user
                user.activated = True
                user.save_to_db()
                confirmation.delete()
                return make_response(render_template('confirmation_page.html', email=user.email), 200,{"Content-Type": "text/html"})
        else:
            return {"message": INVALID_CONFIRMATION_TOKEN}, 400

class ResendConfirmationresource(Resource):

    @classmethod
    def post(cls,email_id: str):
        user = UserModel.find_by_email(email_id)
        if not user:
            return {"message":INVALID_USER},400
        if user.activated:
            return {"message":USER_ACTIVATED},400
        confirmation = user.confirmation
        try:
            send_email(user.id)
            confirmation.delete()
            return {"message":EMAIL_SENT},200
        except MailGunException as e:
            return {"message":EMAIL_SEND_FAILED},500

def send_email(user_id:int):
    confirmation = ConfirmationModel(user_id)
    confirmation.save_to_db()
    link = "http://localhost:5000/confirm/" + confirmation.id
    send_email_confirmation(["dipayan1.das@gmail.com"], "Registration Confirmation",
                                        "Please confirm your mail by clicking on this link, <a href='" + link + "'>" + link + "</a>")



