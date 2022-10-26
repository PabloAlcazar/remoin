from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL, callback_context
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
		dbc.Col(dbc.FormText('Heptane (€/unit)', style={'color':'black'}), width=3),
		dbc.Col(dbc.FormText(id='heptane_unit', children=.4341, style={'width':'100%', 'color':'black'}), width=9),
	]),
	dbc.Row([
		dbc.Col(dbc.FormText('Gas-oil (€/unit)', style={'color':'black'}), width=3),
		dbc.Col(dbc.FormText(id='gas_unit', children=1.281, style={'width':'100%', 'color':'black'}), width=9),
	]),
	dbc.Row([
		dbc.Col(dbc.FormText('Electricity (€/unit)', style={'color':'black'}), width=3),
		dbc.Col(dbc.FormText(id='electricity_unit', children=.179, style={'width':'100%', 'color':'black'}), width=9),
	]),
	dbc.Row([
		dbc.Col(dbc.FormText('Treatments + Staff (€/unit)', style={'color':'black'}), width=3),
		dbc.Col(dcc.Input(id='treat_staff_input', value=2.8739, style={'width':'100%'}), width=2),
		dbc.Col(dcc.Slider(0, 5, .01, value=2.8739, id='treat_staff', marks=None, tooltip={"placement": "bottom", "always_visible": True}),width=7)
	]),
	dbc.Row([
		dbc.Col(dbc.FormText('Amortization (€/unit)*', style={'color':'black'}), width=3),
		dbc.Col(dcc.Input(id='amort_input', value=.2, style={'width':'100%'}), width=2),
		dbc.Col(dcc.Slider(0, 2, .01, value=.2, id='amort', marks=None, tooltip={"placement": "bottom", "always_visible": True}),width=7)
	]),
	dbc.Row(dbc.FormText('* The smaller the amortization, the longer the contract needs to go on in order to obtain ROI', style={'color':'black'})),
	dbc.Row(dbc.FormText(children='4 Years of amortization', id="years_amort", style={'color':'black', 'font-weight':'bold'})),
]


# Contenedor de la aplicacion
container = dbc.Container([
    dbc.Row([
		html.H3('Remoin Ingeniería'),
		], style={'text-align':'center', 'height': '100px'}),
	dbc.Row([
		dbc.Col(dcc.Graph(id="graph"), width=7),
		dbc.Col([
			dbc.Row(html.H5('Market price:')),
			dbc.Row([
				dbc.Col(dbc.FormText('Heptane (€/L)', style={'color':'black', 'width':'100%'}), width=4),
				dbc.Col(dcc.Input(id='heptane_market', value=1.497), width=1)
			]),
			dbc.Row([
				dbc.Col(dbc.FormText('Gas-oil (€/L)', style={'color':'black', 'width':'100%'}), width=4),
				dbc.Col(dcc.Input(id='gas_market', value=1.25), width=1)
			]),
			dbc.Row([
				dbc.Col(dbc.FormText('Electricity (€/kW)', style={'color':'black', 'width':'100%'}), width=4),
				dbc.Col(dcc.Input(id='electricity_market', value=.179), width=1)
			]),
		], width=5, align="center"),
	]),
	html.Div(sliders),
    
	], style={'margin-top':'20px', 'margin-bottom':'40px'})

app.layout = container





# Actualiza la figura
@callback(
    Output("graph", "figure"), 
	Output("years_amort", "children"), 
	Input("heptane_market", "value"),
	Input("gas_market", "value"),
	Input("electricity_market", "value"),
	Input("treat_staff", "value"),
	Input("amort", "value"),

	)
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
	amo_22 = 0.233
	ele_22 = 0.179
	price_22 = 5.501177
	earn_22 = 0.500107 

	costeSimulado = float(gas)*1.34+float(heptane)*.29+float(electricity)*1+treat_staff+amort

	df = {
		'year': ['2020']*3 + ['2022']*3 + ['Simulator']*3,
		'category':['Price\n(paid by Bridgestone)','Cost\n(to Remoin)','Earning\n(to Remoin)']*3,
		'money': [
			# precio, coste, ganancias (1 fila*año)
			price_20, heptane_20+gas_20+amo_20+stuff_20+ele_20,earn_20,
			price_22, heptane_22+gas_22+amo_22+stuff_22+ele_22,earn_22,
			costeSimulado/(1-(10/100)),costeSimulado,(costeSimulado/(1-(10/100)))-costeSimulado
		]
	}
	df = pd.DataFrame(df)


	fig = px.bar(df, x="year", y="money", 
				color="category", barmode="group", text_auto=True)
	fig.update_traces(textfont_size=12, texttemplate='%{y:.3f}', textangle=0, textposition="outside", cliponaxis=False)
	fig.update_layout(
		yaxis_title="€ per unit",
		legend_title_text='',
		# title_pad_t=0,
		title_text='Evolution of costs',
		title_font_color="black",
		title_x=0.5,
		template='simple_white'
		)
	fig.update_layout(legend=dict(
		orientation="h",
		yanchor="bottom",
		y=1.02,
		xanchor="right",
		x=1
	))

	fig.update_layout(
		margin=dict(l=0, r=40, t=120, b=70),
	)

	return fig, f'{round(0.72*7/amort, 2)} Years of amortization'






# Actualiza las unidades por rueda en funcion del precio mercado
@callback(
    Output("heptane_unit", "children"),
	Input("heptane_market", "value"))
def update_heptane_units(heptane_market):
	return round(float(heptane_market)*.29, 4)

# Actualiza las unidades por rueda en funcion del precio mercado
@callback(
    Output("gas_unit", "children"),
	Input("gas_market", "value"))
def update_gas_units(gas_market):
	return round(float(gas_market)*1.34, 4)

# Actualiza las unidades por rueda en funcion del precio mercado
@callback(
    Output("electricity_unit", "children"),
	Input("electricity_market", "value"))
def update_electricity_units(electricity_market):
	return round(float(electricity_market)*1, 4)

# Actualiza los sliders y los input
@callback(
    Output("heptane", "value"),
	Output("heptane_input", "value"),
	Input("heptane", "value"),
	Input("heptane_input", "value"))
def update_inputs(slider_value, input_value):
	ctx = callback_context
	trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
	value = input_value if trigger_id == "heptane_input" else slider_value
	return float(value), float(value)


# Actualiza los sliders y los input
@callback(
    Output("treat_staff", "value"),
	Output("treat_staff_input", "value"),
	Input("treat_staff", "value"),
	Input("treat_staff_input", "value"))
def update_inputs(slider_value, input_value):
	ctx = callback_context
	trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
	value = input_value if trigger_id == "treat_staff_input" else slider_value
	return float(value), float(value)

# Actualiza los sliders y los input
@callback(
    Output("amort", "value"),
	Output("amort_input", "value"),
	Input("amort", "value"),
	Input("amort_input", "value"))
def update_inputs(slider_value, input_value):
	ctx = callback_context
	trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
	value = input_value if trigger_id == "amort_input" else slider_value
	return float(value), float(value)






if __name__ == '__main__':
    app.run_server(debug=False)
