import colorama
import dash
import requests
from dash import html, Dash, dcc
from dash.dependencies import Output, Input, State
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import dcc
from dash_iconify import DashIconify
from flask import Flask, render_template, request, make_response
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
import dash_leaflet as dl
from datetime import datetime
# from dash_extensions.enrich import MultiplexerTransform

# only setup Login
from data.ninja_test import (
    login,
    register,
    create_user_token,
    refresh_user_token,
    verify_user_token,
    update_account,
)


server = Flask(__name__)


app = Dash(
    __name__,
    assets_url_path="assets",
    # transforms=[MultiplexerTransform()],
    external_stylesheets=[
        "https://use.fontawesome.com/releases/v6.2.1/css/all.css",
        dbc.themes.SKETCHY,
    ],
    external_scripts=[
    ],
    # plugins=[dash_labs.plugins.pages],
    use_pages=True,
    server=server,
    # prevent_initial_callbacks=True,
    # suppress_callback_exceptions=True,
)


side_bar_u = html.Div(
    [
        dbc.Button(
            dmc.Burger(
                id="burger-button",
                opened=False,
            ),
            style={"height": "80%"},
            color="secondary",
            outline=True,
        ),
        html.Div(id="burger-state"),
    ]
)

navbar = html.Div(
    dmc.Grid(
        [
            dmc.Col(span=1),
            dmc.Col(
                [
                    dmc.Menu(
                        [
                            dmc.MenuTarget(
                                dmc.Button(
                                    dmc.Avatar(
                                        src=dash.get_asset_url("branding/pip_logo.jpeg"),
                                    ),
                                    variant="subtle",
                                    size="lg",
                                )
                            ),
                            dmc.MenuDropdown(
                                children=[
                                    dmc.MenuLabel("Account Logged In"),
                                    # MenuItem is being called to open login modal
                                    dmc.MenuItem(
                                        "Login",
                                        id="login-modal-button",
                                        icon=DashIconify(icon="mdi:user-lock"),
                                    ),
                                    # dmc.MenuItem(
                                    #     "Register",
                                    #     href="/register_user",
                                    #     icon=DashIconify(
                                    #         icon="simple-icons:theregister"
                                    #     ),
                                    # ),
                                    dmc.MenuDivider(),
                                    dmc.MenuItem(href="/about", children=["About"]),
                                    # account-menu-dropdown is being called to change the above to a logged in vs logged out state
                                ],
                                id="render-navbar-based-on-logged-in-status",
                            ),
                        ],
                        trigger="hover",
                    )
                ],
                span=1,
            ),
            dmc.Col(
                html.Center(
                    html.A(
                        href="/",
                        children=[
                            dmc.Space(h=3),
                            html.H2(
                                "Pip Install Python",
                            ),
                        ],
                    )
                ),
                span=8,
            ),
            dmc.Col(
                children=[
                    side_bar_u,
                ],
                ml="auto",
                span=1,
            ),
            dmc.Col(span=1),
        ],
        gutter="sm",
    ),
    id="dynamic-navbar",
    style={"z-index": "26", 'background': 'linear-gradient(to bottom, #ecf0f1 0%, #515960 100%)'},
)

login_form = dbc.Form(
    [
        dbc.Col(
            [
                dmc.Stack(
                    children=[
                        dmc.TextInput(
                            label="Your Username or Email:",
                            style={"width": "100%"},
                            id="login-username",
                        ),
                    ],
                )
            ]
        ),
        dbc.Col(
            [
                dmc.PasswordInput(
                    label="Your password:",
                    style={"width": "100%"},
                    placeholder="Your password",
                    icon=DashIconify(icon="bi:shield-lock"),
                    id="login-password",
                )
            ]
        ),
    ],
    className="mb-5",
)

# Create the layout for the login screen
login_modal = dmc.Card(
    children=[
        dmc.CardSection(
            dmc.Image(
                src=dash.get_asset_url("branding/banner_login.png"),
                height=180,
            )
        ),
        dmc.Group(
            [
                dmc.Text("Access Account", weight=500),
            ],
            position="apart",
            mt="md",
            mb="xs",
        ),
        login_form,
        dmc.Button(
            "Login",
            variant="light",
            color="blue",
            fullWidth=True,
            mt="md",
            radius="md",
            id="login-button",
        ),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={"width": 350},
    id="login-modal-form",
)


login_to_account = dmc.Modal(
    children=[
        # html.Div(id="User-Avatar"),
        login_modal,
    ],
    id="login-account-modal",
    overflow="outside",
    opened=False,
    size="sm",
)


theme_changer = ThemeChangerAIO(
    aio_id="theme", radio_props={"value": dbc.themes.SKETCHY}
)


app.layout = html.Div(
    [
        # Store Data
        dcc.Store(id='auth-store', storage_type='session'),
        # Change theme
        dmc.Affix(theme_changer, position={"bottom": 75, "right": 20}),
        # Modals

        login_to_account,

        navbar,
        # Alerts
        html.Div(id="welcome-back-alert"),
        # Test Setup to look at dcc.Stor(id='auth-store')
        html.Button('Fetch Data', id='fetch-button'),
        html.Div(id='display-data'),  # Placeholder to display the fetched data

        # Page content
        dash.page_container,
        # force change url
        dcc.Location(id="url", refresh=True),
    ],
    style={"height": "100vh"},
)


@app.callback(Output("dynamic-navbar", "children"),
              [Input('auth-store', 'data')])
def dynamic_navbar(data):
    if data:
        return dmc.Grid(
            [
                dmc.Col(span=1),
                dmc.Col(
                    [
                        dmc.Menu(
                            [
                                dmc.MenuTarget(
                                    dmc.Button(
                                        dmc.Avatar(
                                            src=dash.get_asset_url("branding/pip_logo.jpeg"),
                                        ),
                                        variant="subtle",
                                        size="lg",
                                    )
                                ),
                                dmc.MenuDropdown(
                                    children=[
                                        dmc.MenuLabel("Account Logged In"),
                                        # MenuItem is being called to open login modal
                                        # dmc.MenuItem(
                                        #     "Login",
                                        #     id="login-modal-button",
                                        #     icon=DashIconify(icon="mdi:user-lock"),
                                        # ),
                                        dmc.MenuItem(
                                            html.A(
                                                href="/profile",
                                                children=["Profile"],
                                            ),
                                            icon=DashIconify(
                                                icon="icon-park:avatar"
                                            ),
                                        ),
                                        dmc.MenuDivider(),
                                        dmc.MenuItem(
                                            html.A(
                                                href="/about", children=["About"]
                                            )
                                        ),
                                        # account-menu-dropdown is being called to change the above to a logged in vs logged out state
                                    ],
                                    id="render-navbar-based-on-logged-in-status",
                                ),
                            ],
                            trigger="hover",
                        )
                    ],
                    span=1,
                ),
                dmc.Col(
                    html.Center(
                        html.A(
                            href="/",
                            children=[
                                dmc.Space(h=3),
                                html.H2(
                                    "Django-Dash-Token-Authentication",
                                ),
                            ],
                        )
                    ),
                    span=8,
                ),
                dmc.Col(
                    children=[
                        side_bar_u,
                    ],
                    ml="auto",
                    span=1,
                ),
                dmc.Col(span=1),
            ],
            gutter="sm",
        )
    else:
        return dmc.Grid(
            [
                dmc.Col(span=1),
                dmc.Col(
                    [
                        dmc.Menu(
                            [
                                dmc.MenuTarget(
                                    dmc.Button(
                                        dmc.Avatar(
                                            src=dash.get_asset_url(
                                                "branding/pip_logo.jpeg"
                                            ),
                                        ),
                                        variant="subtle",
                                        size="lg",
                                    )
                                ),
                                dmc.MenuDropdown(
                                    children=[
                                        dmc.MenuLabel("Account Logged In"),
                                        # MenuItem is being called to open login modal
                                        dmc.MenuItem(
                                            "Login",
                                            id="login-modal-button",
                                            icon=DashIconify(icon="mdi:user-lock"),
                                        ),
                                        dmc.MenuItem(
                                            "Register",
                                            href="/register_user",
                                            icon=DashIconify(
                                                icon="simple-icons:theregister"
                                            ),
                                        ),
                                        dmc.MenuDivider(),
                                        dmc.MenuItem(
                                            href="/about", children=["About"]
                                        ),
                                        # account-menu-dropdown is being called to change the above to a logged in vs logged out state
                                    ],
                                    id="render-navbar-based-on-logged-in-status",
                                ),
                            ],
                            trigger="hover",
                        )
                    ],
                    span=1,
                ),
                dmc.Col(
                    html.Center(
                        html.A(
                            href="/",
                            children=[
                                dmc.Space(h=3),
                                html.H2(
                                    "Django-Dash-Token-Authentication",
                                ),
                            ],
                        )
                    ),
                    span=8,
                ),
                dmc.Col(
                    children=[
                        side_bar_u,
                    ],
                    ml="auto",
                    span=1,
                ),
                dmc.Col(span=1),
            ],
            style={"z-index": "26"},
            gutter="sm",
        )


# Burger modal for lower navigation
@app.callback(Output("burger-state", "children"), Input("burger-button", "opened"))
def open(b_opened):
    if b_opened:
        return dmc.Footer(
            height=60,
            fixed=True,
            children=[
                dmc.Group(
                    [

                        html.A(
                            href="/trade_route",
                            children=[
                                dmc.ActionIcon(
                                    DashIconify(icon="noto:globe-showing-americas", width=50),
                                    size=55,
                                    variant="transparent",
                                )
                            ],
                        ),

                    ],
                    position="center",
                ),
            ],
            style={'background': 'linear-gradient(to bottom, #515960 0%, #ecf0f1 100%)'},
        )
    else:
        pass

@dash.callback(
    Output('display-data', 'children'),  # Output to the display-data div
    Input('fetch-button', 'n_clicks'),  # Triggered by the button click
    Input('auth-store', 'data'),
    prevent_inital_callbacks=True
)
def fetch_and_display_data(n_clicks, user_state_value):
    if n_clicks is None or user_state_value is None:
        # Prevents the callback from firing upon app initialization
        return "Click the button to fetch data."
    else:
        # Returns the data fetched from dcc.State to be displayed
        return f"Fetched data: {user_state_value}"

# Store Data through Callbacks
@app.callback(
    # Output("store", "data"), hiding the modal on success
    [
        Output("login-modal-form", "hidden"),
        Output("url", "href"),
        Output('auth-store', 'data')
    ],
    [
        Input("login-button", "n_clicks"),
        Input("login-username", "value"),
        Input("login-password", "value"),
    ],
    prevent_initial_call=True,
)
def get_data(login_button, username, password):
    if login_button is None:
        return dash.no_update
    elif login_button:
        if username and password is not None:
            login_test = login(username, password)
            if login_test:
                user_token = create_user_token(
                    username=f'{login_test["username"]}', password=f"{password}"
                )
                return (
                    True,
                    '/profile/',
                    user_token
                )
            else:
                return dash.no_update
    else:
        return dash.no_update


@app.callback(
    Output("login-account-modal", "opened"),
    Input("login-modal-button", "n_clicks"),
    State("login-account-modal", "opened"),
    prevent_initial_call=True,
)
def toggle_register_modal(n_clicks, opened):
    if n_clicks:
        return not opened


if __name__ == "__main__":
    app.run_server(
        debug=True,
        port=8311,
        threaded=True,
    )
