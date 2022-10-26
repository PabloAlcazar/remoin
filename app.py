from turtle import width
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True)

server = app.server



sliders = [
	dbc.Row([
		dbc.Col(dbc.FormText('Gas-oil (€/unit)', style={'color':'black'}), width=3),
		dbc.Col(dcc.Input(id='gas_input', value=1.281, style={'width':'100%'}), width=2),
		dbc.Col(dcc.Slider(0, 2, .01, value=1.281, id='gas', marks=None, tooltip={"placement": "bottom", "always_visible": True}),width=7)
	]),
	dbc.Row([
		dbc.Col(dbc.FormText('Heptane (€/unit)', style={'color':'black'}), width=3),
		dbc.Col(dcc.Input(id='heptane_input', value=.4341, style={'width':'100%'}), width=2),
		dbc.Col(dcc.Slider(0, 2, .01, value=.4341, id='heptane', marks=None, tooltip={"placement": "bottom", "always_visible": True}),width=7)
	]),
	dbc.Row([
		dbc.Col(dbc.FormText('Electricity (€/unit)', style={'color':'black'}), width=3),
		dbc.Col(dcc.Input(id='electricity_input', value=.179, style={'width':'100%'}), width=2),
		dbc.Col(dcc.Slider(0, 1, .01, value=.179, id='electricity', marks=None, tooltip={"placement": "bottom", "always_visible": True}),width=7)
	]),
	dbc.Row([
		dbc.Col(dbc.FormText('Treatments + Staff (€/unit)', style={'color':'black'}), width=3),
		dbc.Col(dcc.Input(id='treat_staff_input', value=2.90697, style={'width':'100%'}), width=2),
		dbc.Col(dcc.Slider(0, 5, .01, value=2.90697, id='treat_staff', marks=None, tooltip={"placement": "bottom", "always_visible": True}),width=7)
	]),
	dbc.Row([
		dbc.Col(dbc.FormText('Amortization (€/unit)*', style={'color':'black'}), width=3),
		dbc.Col(dcc.Input(id='amort_input', value=.2, style={'width':'100%'}), width=2),
		dbc.Col(dcc.Slider(0, 2, .01, value=.2, id='amort', marks=None, tooltip={"placement": "bottom", "always_visible": True}),width=7)
	]),dbc.FormText('* The smaller the amortization, the longer the contract needs to go on in order to obtain ROI', style={'color':'black'})
]


# Contenedor de la aplicacion
container = dbc.Container([
    dbc.Row(html.H3('Remoin Ingeniería'), style={'text-align':'center'}),
	dbc.Row(dcc.Graph(id="graph")),
	html.Div(sliders),
    
	], style={'margin-top':'20px', 'margin-bottom':'40px'})

app.layout = html.Div([container])

# Actualiza los sliders
@callback(
    Output("gas", "value"),
	Output("heptane", "value"),
	Output("electricity", "value"),
	Output("treat_staff", "value"),
	Output("amort", "value"),
	
	Input("gas_input", "value"),
	Input("heptane_input", "value"),
	Input("electricity_input", "value"),
	Input("treat_staff_input", "value"),
	Input("amort_input", "value"))
def update_inputs(gas, heptane, electricity, treat_staff, amort):
	return float(gas), float(heptane), float(electricity), float(treat_staff), float(amort)


# Actualiza los inputs
@callback(
    Output("gas_input", "value"),
	Output("heptane_input", "value"),
	Output("electricity_input", "value"),
	Output("treat_staff_input", "value"),
	Output("amort_input", "value"),
	
	Input("gas", "value"),
	Input("heptane", "value"),
	Input("electricity", "value"),
	Input("treat_staff", "value"),
	Input("amort", "value"))
def update_inputs(gas, heptane, electricity, treat_staff, amort):
	return float(gas), float(heptane), float(electricity), float(treat_staff), float(amort)


# Actualiza la figura
@callback(
    Output("graph", "figure"), 
    Input("gas", "value"),
	Input("heptane", "value"),
	Input("electricity", "value"),
	Input("treat_staff", "value"),
	Input("amort", "value"))
def update_bar_chart(gas, heptane, electricity, treat_staff, amort):


	heptane_20 = 0.24
	gas_20 = 0.72
	stuff_20 = 2.68
	amo_20 = 0.72
	ele_20 = 0.104
	price_20 = 4.9104
	earn_20 = 0.4464

	heptane_22 = 0.4341
	gas_22 = 1.281
	stuff_22 = 2.8739
	amo_22 = 0.2
	ele_22 = 0.179
	price_22 = 5.501177
	earn_22 = 0.500107 

	costeSimulado = gas+heptane+electricity+treat_staff+amort

	df = {
		'year': ['2020']*3 + ['2022']*3 + ['Simulator']*3,
		'category':['Price\n(paid by Bridgestone)','Cost\n(to Remoin)','Earning\n(to Remoin)']*3,
		'money': [
			# precio, coste, ganancias (1 fila*año)
			price_20, heptane_20+gas_20+amo_20+stuff_20+ele_20,earn_20,
			price_22, heptane_22+gas_22+amo_22+stuff_22+ele_22,earn_22,
			costeSimulado+earn_22*.1/.9,costeSimulado,costeSimulado*.1/.9
		]
	}
	df = pd.DataFrame(df)


	fig = px.bar(df, x="year", y="money", 
				color="category", barmode="group", text_auto=True)
	fig.update_traces(textfont_size=12, texttemplate='%{y:.2f}', textangle=0, textposition="outside", cliponaxis=False)
	fig.update_layout(
		yaxis_title="€ per unit",
		legend_title_text='',
		title_text='Evolution of costs',
		title_font_color="black",
		title_x=0.5,
		template='simple_white'
		)
	return fig






if __name__ == '__main__':
    app.run_server(debug=False)
