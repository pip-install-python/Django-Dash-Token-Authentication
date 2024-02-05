import dash
from dash import html, dcc
from dash.dependencies import Output, Input, State
import dash_mantine_components as dmc
import pydeck as pdk
import pandas
import dash_deck
import json
import dash_trich_components as dtc
import dash_bootstrap_components as dbc




# import utils

dash.register_page(__name__, path="/")

# dash.register_page(__name__, path='/map')



# initial map view state of debug toolbar



# todo: Tried adding a switch navbar thru utils and utils.navbar, but it didn't work
layout = html.Div(
    children=[
        dmc.Image(
                src=dash.get_asset_url("branding/django-dash-token-authentication.png"),
                height='100vh',
                width='100vw'
            )
    ]
)

