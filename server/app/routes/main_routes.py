from flask import Blueprint, current_app

main = Blueprint('main', __name__)  

@main.route('/') 
def home():
    return "Hello from the main route!"

@main.route('/app') 
def app_home():
    return "Hello from app!"

@main.route('/testDB')
def test_DB():
    try:
        # creates a pointer to the DB
        cursor = current_app.mysql.connection.cursor()
        # force use database
        cursor.execute("USE budget_app;")
        # asks what database im using
        cursor.execute("SELECT DATABASE();")
        # returns a tuple of the db name
        db_name = cursor.fetchone()
        return f"Connected to database: {db_name[0]}"
    except Exception as e:
         return f"Database connection failed: {str(e)}"


        