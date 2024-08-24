import re
from datetime import datetime

def generate_slug(text):
    """
    Generates a URL-friendly slug from the provided text.
    """
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^\w\-]', '', text)
    return text.lower()

def calculate_age(birthdate):
    """
    Calculates the age based on the provided birthdate.
    """
    today = datetime.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

def format_response(message, status_code=200):
    return {'message': message}, status_code

