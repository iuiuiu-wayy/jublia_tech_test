from turtle import width
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
from dash.dependencies import Input, Output, State, MATCH, ALL
import datetime 

home_view = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                    html.H1('Jublia Technical Test Application'),
            ], align='center', width=8),
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
                                'margin': '10px',
                            }
                        ),
                        dbc.Row([
                            dbc.Col(
                                dcc.DatePickerSingle(
                                    id="datepicker",
                                    min_date_allowed = datetime.date.today(),
                                ),width=4,
                            ),
                            dbc.Col(
                                dcc.Input(type='time', id='timepicker'),
                                width=3
                            )
                        ]),
                        # html.Br(),
                        dbc.Row([
                            dbc.Col(
                                dbc.Button("add", outline=True, color="primary", className="mr-1", id='email_add'),
                            width=6)
                        ]),
                    ]))
                ])
            ],width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(
                                dbc.Button('Refresh', outline=True, color="primary", className="mr-1", id='list_email_refresh'),
                                width=4
                            )
                        ]),
                        dbc.Row([
                            html.Label('List of recipient email addresses')
                        ]),
                        dbc.Row([
                            html.Div(id='list_email_address'),
                        ]),
                        dbc.Row([
                            html.Label('Last submitted task')
                        ]),
                        dbc.Row([
                            html.Div(id='list_recent_task')
                        ])
                    ])
                ])
            ], width=6)
        ]),
    ])
])

# def home_callback(app):
#     @app.callback(
#         [Output('')]
#     )
