from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True)

# app = Dash(__name__)
server = app.server



sliders = [
	dbc.Row([
		dbc.Col(dbc.FormText('Gas-oil (€/unit)', style={'color':'black'}), width=3),
		dbc.Col(dcc.Slider(0, 2, .01, value=.5, marks=None, tooltip={"placement": "bottom", "always_visible": True}),width=9)
	]),
	dbc.Row([
		dbc.Col(dbc.FormText('Heptane (€/unit)', style={'color':'black'}), width=3),
		dbc.Col(dcc.Slider(0, 2, .01, value=.5, marks=None, tooltip={"placement": "bottom", "always_visible": True}),width=9)
	]),
	dbc.Row([
		dbc.Col(dbc.FormText('Electricity (€/unit)', style={'color':'black'}), width=3),
		dbc.Col(dcc.Slider(0, 2, .01, value=.5, marks=None, tooltip={"placement": "bottom", "always_visible": True}),width=9)
	]),
	dbc.Row([
		dbc.Col(dbc.FormText('Treatments + Staff (€/unit)', style={'color':'black'}), width=3),
		dbc.Col(dcc.Slider(0, 2, .01, value=.5, marks=None, tooltip={"placement": "bottom", "always_visible": True}),width=9)
	])
]


# Contenedor de la aplicacion
container = dbc.Container([
    dbc.Row(html.H3('Remoin'), style={'text-align':'center'}),
	html.Div(sliders)
    
	], style={'margin-top':'20px', 'margin-bottom':'40px'})

app.layout = html.Div([container])




if __name__ == '__main__':
    app.run_server(debug=False)
    # app.run_server(host='0.0.0.0', debug=False, port=8050)