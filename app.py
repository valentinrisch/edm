import dash
import dash_core_components as dcc
import dash_html_components as html

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_dotenv import DotEnv
from flask_migrate import Migrate
import pandas as pd

# flask instance, will be responsible for all the routing, input, and db connection stuff.
server = Flask(__name__)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# dash app, flask is injected via argument
app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)

env = DotEnv(server)
#server.config.from_object(os.environ['APP_SETTINGS'])
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/valentin/Downloads/million_post_corpus/corpus.sqlite3'
db = SQLAlchemy(server)
migrate = Migrate(server, db)

engine = db.create_engine('sqlite:////Users/valentin/Downloads/million_post_corpus/corpus.sqlite3')


# query dataset
# watch uppercase
df = pd.read_sql_table(table_name="Posts", con=engine, columns=['Status', 'ID_Post'])
# count_deleted = df.groupby('Status').count()
df.set_index("ID_Post", drop=False)

print(df.groupby('Status').size().reset_index(name='ID_Post').iloc[0]['ID_Post'])

# @TODO: import from another file, to keep project structured
# @TODO: do first graph accessing pandas.
app.layout = html.Div(children=[
    html.H1(children='Status of Posts'),

    html.Div(children='''
        Shows the distribution of deleted and online posts.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [0], 'y': [df.groupby('Status').size().reset_index(name='ID_Post').iloc[0]['ID_Post'],0], 'type': 'bar', 'name': u'deleted'},
                {'x': [1], 'y': [0, df.groupby('Status').size().reset_index(name='ID_Post').iloc[1]['ID_Post']], 'type': 'bar', 'name': u'online'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server()
