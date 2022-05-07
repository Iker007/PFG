import os
import secrets
from flask import url_for, current_app
from flask_mail import Message
from getitnow import mail

def store_profile_image(form_image):
    rand = secrets.token_hex(10)
    file_name, file_extension = os.path.splitext(form_image.filename)
    image_name = rand + file_extension
    image_path = os.path.join(current_app.root_path, 'static/profile_images', image_name)
    form_image.save(image_path)
    return image_name

def pass_reset_email(user):
    token = user.get_reset_token()
    message = Message('Password reset', sender='noreply@getitnow.com', recipients=[user.email])
    message.body = f'''To reset your password, click here:
{url_for('users.pass_reset', token=token, _external=True)}
    
In case that you didnt make this request, ignore this email
'''
    mail.send(message)