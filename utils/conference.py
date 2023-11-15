import requests
import json
from statistics import mode
from flask import current_app
from sqlalchemy import desc

from werkzeug.security import generate_password_hash, check_password_hash

from database import Conference

def getConferences():
    return Conference.query.all()