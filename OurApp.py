import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.plotly as py
import os
import math
from dateutil import parser
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app_colors = {
    'background': '#b4daff',
	"background_div": "white",
    'text': '#FFFFFF',
    'sentiment-plot':'#41EAD4',
    'volume-bar':'#FBFC74',
    'someothercolor':'#FF206E',
}


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('smallPosts.csv')
df['CreatedAt'] = df['CreatedAt'].apply(parser.parse)

#returns top indicator div
def indicator(color, text, id_value):
    return html.Div(
        [
            
            html.P(
                text,
                className="twelve columns indicator_text"
            ),
            html.P(
                id = id_value,
                className="indicator_value"
            ),
        ],
        className="four columns indicator",
        
    )


def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

file_Size = convert_size(os.stat('smallPosts.csv').st_size)


#available_indicators = df['Indicator Name'].unique()
columns = list(df)


app.layout = html.Div([
    
	html.Div([
		html.H1("Toxic Comments Analysis"),
		html.Div([
			html.P("This dashboard is intended to be used by Data Scientists"),
		]),
    ], className = "row"
	),
	
	html.Div([	
		html.Div([
			html.H2("General informations")
		], className = "three columns"
		),
	
		html.Div([
			html.H3("File Size"),
			html.H3(str(file_Size))
		], className = "three columns"
		),
		
		html.Div([
			html.H3("Number of Columns"),
			html.H3(str(df.shape[0]))
		], className = "three columns"
		),
		
		html.Div([
			html.H3("Number of Rows"),
			html.H3(str(df.shape[1]))
		], className = "three columns"
		),
		
	], className = "row"
	),
	
	html.Div([
		html.Div([
			html.H2("Data quality"),
		], className = "three columns"
		),
		
		html.Div([
			html.P("Usable data should at least have:"),			
		], className = "three columns" #style={'width': '20%', 'display': 'inline-block'}
		),
		
		html.Div([
			dcc.Dropdown(
				id='null_dropdown',
				options=[{'label': i, 'value': i} for i in columns],
				multi=True,
				value=[columns[0]]
			)
		], className = "six columns" #style={'width': '80%', 'float': 'right', 'display': 'inline-block'}
		)
		
	], className = "row"
	),
	
	html.Div([
		html.Div([
			dcc.Graph(
				id='total without missing',
				figure={
					'data' : [
						go.Pie(
							labels=['Without missing values', 'With missing values'],
							values=[df.shape[0]-df.isnull().any(axis=1).sum(),df.isnull().any(axis=1).sum()]
						)
					]
					#'layout' : dict(margin=dict(l=15, r=10, t=0, b=65), legend=dict(orientation="h"))
				}
			),
		], className = "four columns"
		),
		
		html.Div([
			#html.P("percentage of missing values"),
			dcc.Graph(
				id="bar_null",
				#style={"height": "60%"},
				config=dict(displayModeBar=False),
			),
		], className = "four columns"
		),
		
		html.Div([
			#html.P("percentage of missing values"),
			dcc.Graph(
				id="usable_data_pie",
				#style={"height": "60%"},
				config=dict(displayModeBar=False),
			),
		], className = "four columns"
		)
		
	], className = "row"
	),
	
	html.Div([		
		html.Div([
			html.H2("Data Analysis"),
		], #className = "three columns"
		),
	], className = "row"
	),
	
	html.Div([
		html.Div([
			dcc.Graph(
				id='pie chart',
				figure={
					'data' : [
						go.Pie(
							labels=['Deleted', 'Online'],
							values=[(df.Status == 'deleted').sum(),(df.Status == 'online').sum()],
							#marker={"colors": ["#264e86", "#0074e4", "#74dbef", "#eff0f4"]}
						)
					],
					#'layout' : dict(margin=dict(l=15, r=10, t=0, b=65), legend=dict(orientation="h"))
				}
			),
		
		], className = "four columns"
		),
		
		html.Div(
			dcc.RadioItems(
				id="status_selector",
				options=[
					{'label': 'Deleted', 'value': 'deleted'},
					{'label': 'Online', 'value': 'online'}
				],
				value='deleted'
			), className='four columns'
		),
	
		html.Div(
			id = "example_comment",
			children = html.P(),
			className="six columns"
			#html.P(df['Body'][10]),className="four columns chart_div"
		),
		
	], className = "row"
	),

	html.Div([
		dcc.Graph(
			id='Not null',
			figure={
				'data': [
					{'x': df.groupby(df.CreatedAt.dt.date).count().index, 'y': df.ID_Post.groupby(df.CreatedAt.dt.date).count(), 'type': 'line', 'name': 'Total'},
					{'x': df[df.Status == 'deleted'].groupby(df.CreatedAt.dt.date).count().index, 'y': df[df.Status == 'deleted'].ID_Post.groupby(df.CreatedAt.dt.date).count(), 'type': 'line', 'name': 'Deleted'},
					{'x': df[df.Status == 'online'].groupby(df.CreatedAt.dt.date).count().index, 'y': df[df.Status == 'online'].ID_Post.groupby(df.CreatedAt.dt.date).count(), 'type': 'line', 'name': 'Online'}
				],
				'layout': {
					#'title': 'Dash Data Visualization'
				}
			}
		)
	],className="twelve columns chart_div"
	),
	
		
	html.Div([
			dcc.Dropdown(
				id='violin_dropdown',
				options=[{'label': i, 'value': i} for i in columns[11:]],
				multi=True,
				value=[columns[12]]
			),
		],
		style={'width': '100%', 'float': 'right', 'display': 'inline-block'}
	),
	
	html.Div([
		#html.P("percentage of missing values"),
		dcc.Graph(
			id="violin",
			style={"height": "90%", "width": "98%"},
			config=dict(displayModeBar=False),
		),
	],className="twelve columns chart_div"
	),
	
], style = {'backgroundColor': app_colors['background']}
)


@app.callback(
    Output("bar_null", "figure"),
    [Input("null_dropdown", "value")]#, Input("leads_df", "children")],
)
def bar_null(cols):
	trace1 = go.Bar(
		x=cols,
		y=[df[col].isnull().sum() for col in cols],
		name='null'
	)
	trace2 = go.Bar(
		x=cols,
		y=[df[col].count() for col in cols],
		name='not null'
	)

	data = [trace1, trace2]
	layout = go.Layout(
		barmode='stack'
	)
	return dict(data=data, layout=layout)


@app.callback(
    Output("usable_data_pie", "figure"),
    [Input("null_dropdown", "value")]#, Input("leads_df", "children")],
)
def usable_data_pie(cols):
	trace = go.Pie(
		labels=['Without missing values', 'With missing values'],
		values=[df.loc[:,cols].shape[0]-df.loc[:,cols].isnull().any(axis=1).sum(),df.loc[:,cols].isnull().any(axis=1).sum()]
	)
	layout = go.Layout(
		#title='Usable Data',
    )
	return dict(data=[trace], layout=layout)
	
@app.callback(
    Output("violin", "figure"),
    [Input("violin_dropdown", "value")]#, Input("leads_df", "children")],
)
def violin(cols):
	data = []
	for col in cols:
		Online = {
			"type": 'violin',
			"x": col,
			"y": df[col] [ df['Status'] == 'online' ],
			"legendgroup": 'Online',
			"scalegroup": 'Online',
			"name": col,
			"side": 'negative',
			"box": {
				"visible": True
			},
			"meanline": {
				"visible": True
			},
			"line": {
				"color": 'blue'
			},
			"showlegend": False
		}
		data.append(Online)
		Deleted= {
			"type": 'violin',
			"x": col,
			"y": df[col] [ df['Status'] == 'deleted' ],
			"legendgroup": 'Deleted',
			"scalegroup": 'Deleted',
			"name": col,
			"side": 'positive',
			"box": {
				"visible": True
			},
			"meanline": {
				"visible": True
			},
			"line": {
				"color": 'green'
			},
			"showlegend": False
		}
		data.append(Deleted)


	layout = go.Layout(
        yaxis = {
            "zeroline": False,
        },
        violingap = 0,
        #"violingroupgap": 0,
        violinmode = "overlay",
		#margin=dict(l=10, r=10, t=0, b=0)
	)
		
	return dict(data=data, layout=layout)

@app.callback(
    Output("example_comment", "children"),
    [Input("status_selector", "value")]#, Input("leads_df", "children")],
)
def example_comment(status):
	return text_generator(list(df['Body'][df['Status'] == status].dropna().sample(1))[0])
	
def text_generator(text):
	return html.P(text)

if __name__ == '__main__':
    app.run_server()