from sqlalchemy import func, CheckConstraint
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone_number = db.Column(db.String(10), nullable=False)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author must have a name")
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Author phone numbers must be exactly ten digits")
        return phone_number

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(250))
    category = db.Column(db.String(20), nullable=False)

    @validates('title')
    def validate_title(self, key, title):
        if  not  title:
            raise ValueError("Must have a title")
        return title

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Post summary cannot exceed 250 characters")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Invalid post category. Must be either Fiction or Non-Fiction")
        return category

# Create a CheckConstraint for ensuring title is not empty
title_not_empty_constraint = CheckConstraint("length(trim(title)) > 0", name="title_not_empty_constraint")
db.event.listen(Post.__table__, 'after_create', title_not_empty_constraint)
