import dash
import dash_core_components as dcc
import dash_html_components as html

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_dotenv import DotEnv
from flask_migrate import Migrate
import dashboard

# flask instance, will be responsible for all the routing, input, and db connection stuff.
server = Flask(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# dash app, flask is injected via argument
app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)

#import from another file, to keep project structured
app.layout = dashboard.dashboard

env = DotEnv(server)
server.config.from_object(os.environ['APP_SETTINGS'])
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(server)
migrate = Migrate(server, db)

if __name__ == '__main__':
    app.run_server()
