#Creates the Flask app and loads configuration
from flask import Flask
from app.models import create_tables

def create_app():
    '''Also known as factory function; 
    Creates and configures the app instead of creating it globally.
    This allows better structure, easier testing, and support for multiple instances if needed.'''
    #__name__: Tells Flask where to find resources such as templates aand static files
    #Since we have an instance dir, 'instance_relative..' Tells Flask not to use an instance folder for configuration
    app = Flask(__name__, instance_relative_config=False) #Create an instance of Flask (my_movie_app)

    #Create database tables
    with app.app_context():
        create_tables()
        
    #Load config from config.py
    app.config.from_object('config')

    #Register Blueprint
    from app.routes import main
    app.register_blueprint(main) #We 'attach' the blueprint to your Flask app. This makes all routes in main avalilable to the application
    
    #Returns a fully built and configured Flask app INSTANCE
    return app  

#Three steps for creating app __init__.py
    #1. Define create_app function. Then create app(apply create app syntax)
    #2. Load configurations (.from_object())
    #3. Register the blueprints(grouped routes) in your app. Then return your app