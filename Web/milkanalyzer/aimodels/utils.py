import os
import secrets
from flask import current_app

def store_csv(form_csv):
    rand = secrets.token_hex(10)
    file_name, file_extension = os.path.splitext(form_csv.filename)
    csv_name = rand + file_extension
    csv_path = os.path.join(current_app.root_path, 'static/prediction_files', csv_name)
    form_csv.save(csv_path)
    return csv_name