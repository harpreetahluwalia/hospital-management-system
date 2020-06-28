from flask import  Flask
from .routes import route1
    






if __name__ == '__main__':
    app.run(debug=True)

app=Flask(__name__)

app.register_blueprint(route1.bp)