from app import db, app

# Run this inside the Flask app context
with app.app_context():
    db.create_all() 