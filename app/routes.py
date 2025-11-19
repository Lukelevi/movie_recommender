from flask import Blueprint, render_template, request
from app.recommender.engine import get_recommendations

#Blueprint: A way to group routes/views and register them on the main app
#request: the current incoming HTTP request object(used to access form data, query patrams, headers, etc.)
main = Blueprint('main', __name__) #Creates a blueprint instance called main. 'main' is the blueprint's identifier
#__name__ tells Flask where Blueprint code lives(used for finding templates/ static files)
#The 'main' object wil hold rlated routes that you later register with your flask app
#Therefore, we prefix each route with 'main'(our blueprint)
@main.route('/')
def index():
    '''UI With search bar and movie images dsplayed with flex-box grid. 
    Top searched movies can populate the home page(until we implement authentication)'''
    return render_template('index.html')

@main.route('/results', methods=['POST']) #Handles post request and returns movie_data as the response
def results():
    '''Create an HTTP request call to get movies from 'recommended movies(recommender)
    And render the results.html with your recommended movies'''
    #So GET requests would 405 unless another route handles them
    movie_title = request.form.get('movie')
    if movie_title == None:
        return "No such movies" #Later incorperate a route to handle that error
    result = get_recommendations(movie_title) #Accepts a movie title and return List of recommended movies(recommended data)

    return render_template(
        'results.html',
        movie=movie_title,
        recommendations = result
    )


#request.form is a dict-like object containing form fields(from multipart/form-data)
#render_template renders an HTML TEMPLATE(jinja2) and returns an HTTPS response


#All your flask routes; example
#Blueprints lets you split into LOGICAL modules instead of keeping everything in one big file.
#Configuration: Arrangement of software components, which can be a result of a process or the final setup itself
            #Includes stting options that define how an application operates, allowing users to customize it to their needs
#Example: Adjusting settings in an application, such as changing the theme to "dark mode" or setting a software to start automatically on a computer.

#Flask often uses an instance folder for things that change(database, config)