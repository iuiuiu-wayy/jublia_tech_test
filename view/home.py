from turtle import width
from dash import html
import dash_bootstrap_components as dbc

home_view = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                  html.H1('Jublia Technical Test Application'),
            ], align='center', width=6),
        ], justify='center'),
        dbc.Row([
            dbc.Col([
            dbc.Card([
                dbc.CardBody(html.Div([
                    html.Label('Add brodcast email'),
                    dbc.Input(id="subject_textarea", placeholder="Subject", type="text"),
                    dbc.Textarea(
                        id = 'content_textarea',
                        placeholder = 'Content here',
                        style={
                          'width': '100%',
                          'height': '200',
                          'lineHeight': '60px',
                          'borderWidth': '1px',
                          # 'borderStyle': 'dashed',
                          'borderRadius': '5px',
                          'margin': '10px'
                      }
                    ),
                    dbc.Button("Submit", outline=True, color="primary", className="mr-1", id='email_submit')
                ]))
            ])
        ],width=6)]),
        dbc.Col([
            dbc.Card([

            ])
        ], width=6)
    ])
])