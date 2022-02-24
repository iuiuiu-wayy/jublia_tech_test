from dash import Dash
from dash import html
import dash_bootstrap_components as dbc

def init_app(app):
    dash_app = Dash(
        server = app,
        suppress_callback_exceptions=True,
        external_stylesheets=[dbc.themes.SANDSTONE],
        url_base_pathname='/management/'
    )
    with dash_app.server.app_context():
        from .home import home_view
    dash_app.layout = home_view