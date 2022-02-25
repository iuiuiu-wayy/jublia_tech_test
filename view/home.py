from sqlite3 import Timestamp
from turtle import width
from dash import html
from dash.dependencies import Input, Output, State, MATCH, ALL
import datetime 
import dash_bootstrap_components as dbc
from dash import dcc
from flask import request, url_for
import requests
import pytz


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
                        dbc.Row([
                            dbc.Col(
                                dbc.Button("add", outline=True, color="primary", className="mr-1", id='email_add'),
                            width=6)
                        ]),
                    ])),
                    dbc.CardBody([
                        dbc.Row([
                            html.Label('Add recipient email below'),
                        ]),
                        dbc.Row([
                            dbc.Col(
                                dbc.Input(id='new_recipient_email', placeholder='example@jublia.com', type='text'),
                                width=9,
                            ),
                        ]),
                        dbc.Row([
                            dbc.Col(
                                dbc.Button('add email address',  outline=True, color="primary", className="mr-1", id='new_email_button'),
                                width=6
                            ),
                        ])
                    ])
                ])
            ],width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(
                                dbc.Button('Refresh', outline=True, color="primary", className="mr-1", id='list_refresh'),
                                width=4
                            ),
                        ]),
                        dbc.Row([
                            html.Label('List of recipient email addresses:')
                        ]),
                        dbc.Row([
                            html.Div(id='list_email_address'),
                        ]),
                        dbc.Row([
                            html.Br()
                        ]),
                        dbc.Row([
                            html.Label('Last submitted task:')
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

def home_callback(dash_app):
    @dash_app.callback(
        [Output('list_email_address', 'children'),
        Output('list_recent_task', 'children')],
        [Input('list_refresh','n_clicks' )]
    )
    def refresh_button(n_clicks):
        with dash_app.server.app_context():
            from models.operations import get_recent_task, get_recipient_emails

        LOCAL_TIMEZONE = pytz.timezone(dash_app.server.config['TIMEZONE'])
        tasks= get_recent_task()
        email_address = get_recipient_emails()
        task_header = [html.Thead(html.Tr([html.Th("Subject"), html.Th("Status"), html.Th("Timestamp")]))]
        task_tr = []
        for i in range(len(tasks)):
            timestamp = tasks[i][2].astimezone(LOCAL_TIMEZONE)
            timestamp_str = "{}-{}-{} {}:{}:00".format(timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute)
            task_tr.append( html.Tr([html.Td(tasks[i][0]),html.Td(tasks[i][1]),html.Td( timestamp_str )]) )
        task_body = [html.Tbody(task_tr)]
        task_table = dbc.Table(task_header + task_body)
        email_rows = [html.Tr([html.Td(email)]) for email in email_address]
        email_table = html.Tbody(email_rows)
        return email_table, task_table
    
    @dash_app.callback(
        Output('new_recipient_email', 'value'),
        Input('new_email_button', 'n_clicks'),
        State('new_recipient_email', 'value')
    )
    def add_new_email_button(n_clicks, new_email_address):
        if n_clicks is None:
            return ''
        if new_email_address == '' or new_email_address is None:
            return ''
        endpoint = '/'.join(request.base_url.split('/')[:3] + ['add_recipient_email'])
        data_to_send = {'email_address':new_email_address}
        res = requests.post(endpoint, data=data_to_send)
        return ''
    
    @dash_app.callback(
        [Output('subject_textarea', 'value'),
        Output('content_textarea', 'value'),
        Output('datepicker', 'date'),
        Output('timepicker', 'value')],
        Input('email_add', 'n_clicks'),
        [State('subject_textarea', 'value'),
        State('content_textarea', 'value'),
        State('datepicker', 'date'),
        State('timepicker', 'value')] 
    )
    def save_email_callback(n_clicks, subject, content, date_input, time_input):
        if None in [n_clicks, subject, content, date_input, time_input] :
            return subject, content, date_input, time_input
        endpoint = '/'.join(request.base_url.split('/')[:3] + ['save_emails'])
        data_to_send = {
            'email_subject':subject,
            'email_content':content,
            'timestamp':'{} {}:00'.format(date_input, time_input)
            }
        res = requests.post(endpoint, data=data_to_send)
        return (None, None, None, None)