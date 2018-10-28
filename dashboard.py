import dash_core_components as dcc
import dash_html_components as html

#import pandas as pd

# import redpanda
#
# engine = redpanda.create_engine("sqlite://")
# # => Engine(sqlite://)
#
# Session = redpanda.orm.sessionmaker(bind=engine)
# session = Session()
# # => <sqlalchemy.orm.session.Session>

from app import db

# query = db.session
#
# df = pd.read_sql()

dashboard = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montreal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])


