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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']#['https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css']#['my_style.css']#["https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"] #

my_style ={
	'text-align': 'center',
	'border-radius': '8px',
	'border': '2px solid #0B0B61',
	'margin': '5px',
	'background-color': 'white',
	#'margin': '0',
    #'padding': '0'
}

my_style2 ={
	#'text-align': 'center',
	'border-radius': '8px',
	'border': '2px solid #0B0B61',
	'margin': '5px',
	'background-color': 'white',
	#'margin': '0',
    #'padding': '0'
}


app_colors = {
    'background': "white", #'#b4daff',
	"background_div": "white",
	"deleted_data": "#FF8000",#"#FF0000",
	"online_data": "#1F77B4",#"#60BC70",
	"missing": "#FF8000",
	"not_missing": "#1F77B4",
	"total" : "#60BC70"

}


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

filePath =  "./assets/dataset/smallPosts.csv" #'PostsExtended.csv'#'smallPosts.csv' #PostsMid.csv #'smallPosts.csv'
df = pd.read_csv(filePath)#('smallPosts.csv')
df['CreatedAt'] = df['CreatedAt'].apply(parser.parse)

timeSeries = pd.DataFrame(index=df.groupby(df.CreatedAt.dt.date).count().index, columns=['num_total','num_online','num_del'])
timeSeries.num_total = df.ID_Post.groupby(df.CreatedAt.dt.date).count()
timeSeries.num_del = df[df.Status == 'deleted'].ID_Post.groupby(df.CreatedAt.dt.date).count()
timeSeries.num_online = df[df.Status == 'online'].ID_Post.groupby(df.CreatedAt.dt.date).count()
timeSeries = timeSeries.fillna(0)

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

file_Size = convert_size(os.stat(filePath).st_size)


#available_indicators = df['Indicator Name'].unique()
columns = list(df)
categorical_columns = ['ID_Post','ID_Parent_Post','ID_Article','ID_User','Status','Headline','Body','Is_Staff']
numerical_columns = ['PositiveVotes','NegativeVotes','count_sent','count_word','count_unique_word','count_letters','count_punctuations','count_words_upper','count_words_title','count_stopwords','mean_word_len']

app.layout = html.Div([
    
	
	html.Div([
		html.Div([
			html.H1("Toxic Comments Analysis"),
			html.P("This dashboard is intended to be used by Data Scientists"),
		],className = "col-md-12"
		)
	], className = "row",
	style = my_style
	),
	
	
	html.Div([	
		html.Div([
			html.H2("Basic Overview")
		], className = "three columns"#,style = my_style
		),
	
		html.Div([
			html.H3("File Size"),
			html.H3(str(file_Size))
		], className = "three columns"#,style = my_style
		),
		
		html.Div([
			html.H3("Number of Columns"),
			html.H3(str(df.shape[0]))
		], className = "three columns"#,style = my_style
		),
		
		html.Div([
			html.H3("Number of Rows"),
			html.H3(str(df.shape[1]))
		], className = "three columns"#,style = my_style
		),
		
	], className = "row",
	style = my_style
	),
	
	html.Div([
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
			], className = "six columns" , style={'width': '45%', 'float': 'right', 'display': 'inline-block'}
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
								values=[df.shape[0]-df.isnull().any(axis=1).sum(),df.isnull().any(axis=1).sum()],
								marker=dict(colors=[app_colors['not_missing'], app_colors['missing']])
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
		)
	],style = my_style2
	),
	
	
	html.Div([
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
								marker=dict(colors=[app_colors['deleted_data'], app_colors['online_data']])
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

			html.Div(
				dcc.RadioItems(
					id="time_series_button",
					options=[
						{'label': 'Absolute', 'value': 'absolute'},
						{'label': 'Relative', 'value': 'relative'}
					],
					value='absolute'
				), className="two columns"
			),
			
			html.Div([
				dcc.Graph(
					id="time_series",
					config=dict(displayModeBar=False)
				)
			],className="ten  columns",
			#style = {"":"","":""}#{'width': '100%', 'float': 'right', 'display': 'inline-block'}
			),		

		], className = "row"
		),
		
		# html.Div([
				# dcc.Dropdown(
					# id='violin_dropdown',
					# options=[{'label': i, 'value': i} for i in numerical_columns],
					# multi=False,
					# value= 'count_word'
				# ),
			# ],
			# style={'width': '100%', 'float': 'right', 'display': 'inline-block'}
		# ),
		
		# html.Div([
			# #html.P("percentage of missing values"),
			# dcc.Graph(
				# id="violin",
				# style={"height": "90%", "width": "98%"},
				# config=dict(displayModeBar=False),
			# ),
		# ],className="twelve columns chart_div"
		# ),
		
		# html.Div([
			# dcc.Dropdown(
				# id='box_plot_selector',
				# options=[{'label': i, 'value': i} for i in numerical_columns],
				# multi=False,
				# value='count_word'
			# ),
		# ],
		# style={'width': '100%', 'float': 'right', 'display': 'inline-block'}
		# ),
		
		html.Div([
			html.Div([
				dcc.RadioItems(
					id="box_plot_selector",
					options=[{'label': i, 'value': i} for i in numerical_columns],
					#multi=False,
					value='count_word'
				)
			],className="two columns chart_div"
			),
			
			html.Div([
				dcc.Graph(
					id="box_plot",
					style={"height": "90%", "width": "98%"},
					config=dict(displayModeBar=False),
				),
			],className="ten columns chart_div"
			)
		],className="row"
		)
	], style = my_style2
	)
	
], className="container-fluid", style = {'backgroundColor': app_colors['background']}
)


@app.callback(
    Output("bar_null", "figure"),
    [Input("null_dropdown", "value")]#, Input("leads_df", "children")],
)
def bar_null(cols):
	trace1 = go.Bar(
		x=cols,
		y=[df[col].isnull().sum() for col in cols],
		name='null',
		marker=dict(color=app_colors['missing'])
	)
	trace2 = go.Bar(
		x=cols,
		y=[df[col].count() for col in cols],
		name='not null',
		marker=dict(color=app_colors['not_missing'])
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
		values=[df.loc[:,cols].shape[0]-df.loc[:,cols].isnull().any(axis=1).sum(),df.loc[:,cols].isnull().any(axis=1).sum()],
		marker=dict(colors=[app_colors['not_missing'], app_colors['missing']])
	)
	layout = go.Layout(
		#title='Usable Data',
    )
	return dict(data=[trace], layout=layout)
	
# @app.callback(
    # Output("violin", "figure"),
    # [Input("violin_dropdown", "value")]#, Input("leads_df", "children")],
# )
# def violin(col): #cols
	# data = []
	# #for col in cols:
	# Online = {
		# "type": 'violin',
		# "y": col,
		# "x": df[col] [ df['Status'] == 'online' ],
		# "legendgroup": 'Online',
		# "scalegroup": 'Online',
		# "name": col,
		# "side": 'negative',
		# "box": {
			# "visible": True
		# },
		# "meanline": {
			# "visible": True
		# },
		# "line": {
			# "color": 'blue'
		# },
		# "showlegend": False,
		# "orientation" : "h"  
	# }
	# data.append(Online)
	# Deleted= {
		# "type": 'violin',
		# "y": col,
		# "x": df[col] [ df['Status'] == 'deleted' ],
		# "legendgroup": 'Deleted',
		# "scalegroup": 'Deleted',
		# "name": col,
		# "side": 'positive',
		# "box": {
			# "visible": True
		# },
		# "meanline": {
			# "visible": True
		# },
		# "line": {
			# "color": 'green'
		# },
		# "showlegend": False,
		# "orientation" : "h"  
	# }
	# data.append(Deleted)


	# layout = go.Layout(
        # yaxis = {
            # "zeroline": False,
        # },
        # violingap = 0,
        # #"violingroupgap": 0,
        # violinmode = "overlay",
		# #margin=dict(l=10, r=10, t=0, b=0)
	# )
		
	# return dict(data=data, layout=layout)

@app.callback(
    Output("example_comment", "children"),
    [Input("status_selector", "value")]#, Input("leads_df", "children")],
)
def example_comment(status):
	return text_generator(list(df['Body'][df['Status'] == status].dropna().sample(1))[0])
	
def text_generator(text):
	return html.P(text)

	
	
@app.callback(
    Output("time_series", "figure"),
    [Input("time_series_button", "value")]#, Input("leads_df", "children")],
)
def time_series(val):
	if val == 'absolute':
		dummy = 1
	else:
		dummy = timeSeries.num_total

	
	x = timeSeries.index

	trace0 = go.Scatter(
		x = x,
		y = timeSeries.num_total/dummy,
		mode = 'lines',
		name = 'Total',
		line = dict( color = app_colors['total'])
	)

	trace1 = go.Scatter(
		x = x,
		y = timeSeries.num_del/dummy,
		mode = 'lines',
		name = 'Deleted',
		line = dict( color = app_colors['deleted_data'])
	)
	trace2 = go.Scatter(
		x = x,
		y = timeSeries.num_online/dummy,
		mode = 'lines',
		name = 'Online',
		line = dict( color = app_colors['online_data'])
	)

	data = [trace0, trace1, trace2]
	
	layout = dict(
		title = "Daily number of comments",
		# xaxis = dict(
			# range = ['2015-05-31','2016-06-07']
		# )
	)
	
	return dict(data=data, layout=layout)#)

	
	
@app.callback(
    Output("box_plot", "figure"),
    [Input("box_plot_selector", "value")]#, Input("leads_df", "children")],
)
def box_plot(col):
	
	trace0 = go.Box(
		x = df[col][df.Status == 'deleted'],
		name = 'Deleted',
		marker= dict(color = app_colors['deleted_data'])
	)
	trace1 = go.Box(
		x = df[col][df.Status == 'online'],
		name = 'Online',
		marker= dict(color = app_colors['online_data'])
	)
	data = [trace0, trace1]


	layout = go.Layout(
		title=col,
	)

	return dict(data=data, layout=layout)
	
	
if __name__ == '__main__':
	#crete a config for host runnning locally
    app.run_server(debug=True, host='0.0.0.0')