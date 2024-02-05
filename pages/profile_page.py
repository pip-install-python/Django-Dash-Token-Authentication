import dash
from dash import html, dcc
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
import colorama
from dash_iconify import DashIconify
import os
from data.ninja_test import get_user_info, update_account
import dash_leaflet as dl

import requests
from flask import Flask, render_template, request, make_response

dash.register_page(__name__, path="/profile")

# User Profile Page

# Initialize an empty list to store the image elements
image_elements = []
raw_image_element = []

# Get Root Directory
root_dir = os.getcwd()
# get the path to the assets folder
parent_dir = os.path.abspath(os.path.join(root_dir, '..'))


# Loop through all the files in the assets folder
for filename in os.listdir(f'{root_dir}/assets/static/profile_images'):
    # Check if the file is an image file
    if filename.endswith('.png'):
        # print(filename)
        # Open the image file
        # Create an <img> element for the image

        img_element = html.Img(src=dash.get_asset_url(f'static/profile_images/{filename}'), style={'width': '100px', 'height': '250px'})
        # avatar_elements.append(dmc.Avatar(src=dash.get_asset_url(f'static/profile_images/{filename}'), size='xl', radius="xl"))
        # Add the image element to the list
        image_elements.append(img_element)
        raw_image_element.append(f'static/profile_images/{filename}')



layout = html.Div(
    [
        dcc.Location(
            id="redirect-save-profile",
            refresh=True
        ),
        html.Button(id='profile-on-load', n_clicks=1, style={'display': 'none'}),
        html.Div(id="welcome-back-alert"),
        dbc.Container(
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader("Changing Room"),
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                html.Center(
                                                    ''
                                                ),
                                            ]
                                        ),

                                        dbc.Row(
                                            [
                                                html.Center(
                                                    html.Div(id="output-profile-upload")
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dmc.Slider(
                                                    min=0,
                                                    max=(len(image_elements) - 1),
                                                    step=1,
                                                    id="profile-select-slider",
                                                    value=int(len(image_elements) / 2),
                                                    size="xl",
                                                    radius="xl",
                                                    color="dark",
                                                    thumbChildren=DashIconify(
                                                        icon="wpf:add-user", width=32
                                                    ),
                                                    labelAlwaysOn=False,

                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dmc.TextInput(
                                                    label="Change Your Email",
                                                    style={"width": "100%"},
                                                    placeholder="Your Email",
                                                    icon=DashIconify(
                                                        icon="ic:round-alternate-email"
                                                    ),
                                                    id='email-value'
                                                )
                                            ], id="profile-email",
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dmc.TextInput(
                                                        label="Add a Donation Link:",
                                                        style={"width": "100%"},
                                                        placeholder="Your Donation Link",
                                                        icon=DashIconify(
                                                            icon="flat-color-icons:money-transfer"
                                                        ),
                                                        id='donation-value'
                                                    ), id="profile-donation-link",
                                                ),
                                                dbc.Col(
                                                    dmc.TextInput(
                                                        label="Add a Youtube Link:",
                                                        style={"width": "100%"},
                                                        placeholder="Your Youtube Channel",
                                                        icon=DashIconify(
                                                            icon="logos:youtube-icon"
                                                        ),
                                                        id='youtube-value'
                                                    ), id="profile-youtube-link",
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dmc.TextInput(
                                                        label="Add a Discord Link:",
                                                        style={"width": "100%"},
                                                        placeholder="Your Discord",
                                                        icon=DashIconify(
                                                            icon="logos:discord-icon"
                                                        ),
                                                        id='discord-value'
                                                    ), id="profile-discord-link",
                                                ),
                                                dbc.Col(
                                                    dmc.TextInput(
                                                        label="Add a r/reddit Link:",
                                                        style={"width": "100%"},
                                                        placeholder="Your Reddit",
                                                        icon=DashIconify(
                                                            icon="line-md:reddit-loop"
                                                        ),
                                                        id='reddit-value'
                                                    ), id="profile-reddit-link",
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dmc.TextInput(
                                                        label="Add a Github Link:",
                                                        style={"width": "100%"},
                                                        placeholder="Your Github",
                                                        icon=DashIconify(
                                                            icon="typcn:social-github-circular"
                                                        ),
                                                        id='github-value'
                                                    ), id="profile-github-link",
                                                ),
                                                dbc.Col(
                                                    dmc.TextInput(
                                                        label="Add a Snapchat Link:",
                                                        style={"width": "100%"},
                                                        placeholder="Your Snapchat Username",
                                                        icon=DashIconify(
                                                            icon="fa-brands:snapchat-square",
                                                            style={"color": "yellow"},
                                                        ),
                                                        id='snapchat-value'
                                                    ), id="profile-snapchat-link",
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dmc.TextInput(
                                                        label="Add a DM Link:",
                                                        style={"width": "100%"},
                                                        placeholder="Your Direct Message Link",
                                                        icon=DashIconify(
                                                            icon="openmoji:mobile-message"
                                                        ),
                                                        id='dm-value'
                                                    ), id="profile-dm-link",
                                                ),
                                                dbc.Col(
                                                    dmc.TextInput(
                                                        label="Add a Website Link:",
                                                        style={"width": "100%"},
                                                        placeholder="Your Website",
                                                        icon=DashIconify(
                                                            icon="carbon:app"
                                                        ),
                                                        id='website-value'
                                                    ), id="profile-website-link",
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                            ],
                            style={"background-color": "#ecf0f1"},
                        )
                    ],
                    style={"height": "100%"},
                    md=6,
                    sm=12,
                ),
                html.Br(),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader("Profile Mirror"),
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    html.Center(
                                                        html.Div(id="profile-mirror")
                                                    )
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Row(
                                                            [dbc.Col(html.H5(f"Username: Create an Account",
                                                                     id='profile-username')), dbc.Col(html.A(
                                                            href="/register",
                                                            children=[
                                                                html.Center(
                                                                    DashIconify(icon="openmoji:openstreetmap", width=45)
                                                                )
                                                            ],
                                                        ), style={'float': 'right'})],
                                                        ),
                                                        dbc.Row(
                                                            [
                                                                html.H4("Email: Add an Email",
                                                                        id='profile-email-mirror'),

                                                            ]
                                                        ),
                                                        dbc.Row(
                                                            dmc.Textarea(
                                                                label="About Me:",
                                                                placeholder="Hello World! I am a new user to Maply!",
                                                                style={"width": 500},
                                                                autosize=True,
                                                                minRows=2,
                                                                maxRows=4,
                                                                id='about-me-value'
                                                            ), id="profile-about-me",
                                                        ),
                                                        html.Br(),
                                                        dbc.Row(
                                                            dmc.Group(
                                                                [
                                                                    html.A(
                                                                        href="https://shorturl.at/FIRT3",
                                                                        children=[
                                                                            DashIconify(
                                                                                icon="flat-color-icons:money-transfer",
                                                                                width=32,
                                                                            )
                                                                        ],
                                                                        id='donation'
                                                                    ),
                                                                    html.A(
                                                                        href="https://www.youtube.com/channel/UC-pBvv8mzLpj0k-RIbc2Nog?sub_confirmation=1",
                                                                        children=[
                                                                            DashIconify(
                                                                                icon="logos:youtube-icon",
                                                                                width=32,
                                                                            )
                                                                        ],
                                                                        id='youtube'
                                                                    ),
                                                                    html.A(
                                                                        href="https://discord.gg/VXW7cpsnJk",
                                                                        children=[
                                                                            DashIconify(
                                                                                icon="logos:discord-icon",
                                                                                width=32,
                                                                            )
                                                                        ],
                                                                        id='discord'
                                                                    ),
                                                                    html.A(
                                                                        href="https://www.reddit.com/r/PipInstallPython/",
                                                                        children=[
                                                                            DashIconify(
                                                                                icon="line-md:reddit-loop",
                                                                                width=32,
                                                                                style={
                                                                                    "color": "rgb(255, 69, 0)"
                                                                                },
                                                                            )
                                                                        ],
                                                                        id='reddit'
                                                                    ),
                                                                    html.A(
                                                                        href="https://github.com/Pip-Install-Pirate",
                                                                        children=[
                                                                            DashIconify(
                                                                                icon="typcn:social-github-circular",
                                                                                style={
                                                                                    "color": "gray"
                                                                                },
                                                                                width=32,
                                                                            )
                                                                        ],
                                                                        id='github'
                                                                    ),
                                                                    html.A(
                                                                        href="https://www.snapchat.com/add/thegatsbypirate?share_id=6ZAGSwu2Kts&locale=en-US",
                                                                        children=[
                                                                            DashIconify(
                                                                                icon="fa-brands:snapchat-square",
                                                                                style={
                                                                                    "color": "yellow"
                                                                                },
                                                                                width=32,
                                                                            )
                                                                        ],
                                                                        id='snapchat'
                                                                    ),
                                                                    html.A(
                                                                        href="https://pipinstallpython.pythonanywhere.com/home/direct_message/",
                                                                        children=[
                                                                            DashIconify(
                                                                                icon="openmoji:mobile-message",
                                                                                width=32,
                                                                            )
                                                                        ],
                                                                        id='dm'
                                                                    ),
                                                                ],
                                                                spacing="md",
                                                                position="center",
                                                            )
                                                        ),
                                                    ],
                                                    width=8,
                                                ),
                                            ],
                                            style={"height": "30vh"},
                                        ),
                                    dbc.Col(dmc.Select(
                                                label="Select a Theme",
                                                placeholder="What Theme do you like?",
                                                id="r-theme-register-select",
                                                value="SKETCHY",
                                                disabled=True,
                                                data=[
                                                    {"value": "BOOTSTRAP", "label": "Bootstrap"},
                                                    {"value": "CERULEAN", "label": "Cerulean"},
                                                    {"value": "COSMO", "label": "Cosmo"},
                                                    {"value": "CYBORG", "label": "Cyborg"},
                                                    {"value": "DARKLY", "label": "Darkly"},
                                                    {"value": "FLATLY", "label": "Flatly"},
                                                    {"value": "JOURNAL", "label": "Journal"},
                                                    {"value": "LITERA", "label": "Litera"},
                                                    {"value": "LUMEN", "label": "Lumen"},
                                                    {"value": "LUX", "label": "Lux"},
                                                    {"value": "MATERIA", "label": "Materia"},
                                                    {"value": "MINTY", "label": "Minty"},
                                                    {"value": "MORPH", "label": "Morph"},
                                                    {"value": "PULSE", "label": "Pulse"},
                                                    {"value": "QUARTZ", "label": "Quartz"},
                                                    {"value": "SANDSTONE", "label": "SandStone"},
                                                    {"value": "SIMPLEX", "label": "Simplex"},
                                                    {"value": "SKETCHY", "label": "Sketchy"},
                                                    {"value": "SLATE", "label": "Slate"},
                                                    {"value": "SOLAR", "label": "Solar"},
                                                    {"value": "SPACELAB", "label": "SpaceLab"},
                                                    {"value": "SUPERHERO", "label": "SuperHero"},
                                                    {"value": "UNITED", "label": "United"},
                                                    {"value": "VAPOR", "label": "Vapor"},
                                                    {"value": "YETI", "label": "Yeti"},
                                                    {"value": "ZEPHYR", "label": "Zephyr"},
                                                ],
                                                style={"marginBottom": 10},
                                            ),),
                                        dbc.Row(html.Br()),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Card(
                                                        [
                                                            dbc.CardHeader(
                                                                "Profile Assets"
                                                            ),
                                                            dbc.CardBody(
                                                                [
                                                                    dmc.Group(
                                                                        [
                                                                            dmc.Badge(
                                                                                "$0.00",
                                                                                variant="gradient",
                                                                                gradient={
                                                                                    "from": "teal",
                                                                                    "to": "lime",
                                                                                    "deg": 105,
                                                                                },
                                                                                id="profile-credits",
                                                                            ),
                                                                        ]
                                                                    )
                                                                ]
                                                            ),
                                                        ],
                                                        className="mr-1",
                                                        style={"width": "100%"},
                                                    )
                                                )
                                            ]
                                        ),
                                        html.Br(),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Button(
                                                        "Save",
                                                        className="mr-1",
                                                        style={"width": "100%"},
                                                        id='save-profile'
                                                    )
                                                )
                                            ]
                                        ),
                                    ]
                                ),
                            ],
                            style={"background-color": "#ecf0f1"},
                        )
                    ],
                    style={"height": "100%"},
                    md=6,
                    sm=12,
                ),
            ]
        )),
    dl.Map(center=[41.3737, -100.1026], zoom=5, children=[dl.TileLayer(), dl.LayerGroup(id="layer")],
                       style={'width': '100vw', 'height': '100vh', 'margin': "auto", "display": "block", 'z-index': '-1', 'position': 'absolute', 'top':0}),
    ]
)


# Update slider & selected avatar image
@dash.callback(
    [Output("output-profile-upload", "children")],
    Input("profile-select-slider", "value"),
)
def update_value(value):
    for i in range(len(image_elements)):
        if value == 0:
            return (
                dmc.Group(
                    children=[
                        dmc.Tooltip(
                            image_elements[value],
                            label="Select an Avatar & Start Location",
                            withArrow=True,
                            arrowSize=6,
                            opened=True,
                        ),
                        html.Div(image_elements[i + 1], style={"opacity": 0.5}),
                        html.Div(image_elements[value + 2], style={"opacity": 0.25}),
                    ],
                    align="center",
                    position='center'

                ),
                # image_elements[value],
            )
        elif value == 1:
            return (
                dmc.Group(
                    children=[
                        html.Div(image_elements[value - 1], style={"opacity": 0.5}),
                        dmc.Tooltip(
                            image_elements[value],
                            label="Select an Avatar",
                            withArrow=True,
                            arrowSize=6,
                            opened=True,
                        ),
                        html.Div(image_elements[value + 1], style={"opacity": 0.5}),
                        # html.Div(image_elements[value + 2], style={"opacity": 0.25}),
                    ],
                    align="center",
                    position='center'
                ),
                # image_elements[value],
            )
        elif value == len(image_elements) - 2:
            return (
                dmc.Group(
                    children=[
                        # html.Div(image_elements[value - 2], style={"opacity": 0.25}),
                        html.Div(image_elements[value - 1], style={"opacity": 0.5}),
                        dmc.Tooltip(
                            image_elements[value],
                            label="Select an Avatar",
                            withArrow=True,
                            arrowSize=6,
                            opened=True,
                        ),
                        html.Div(image_elements[value + 1], style={"opacity": 0.5}),
                    ],
                    align="center",
                    position='center'
                ),
                # image_elements[value],
            )
        elif value == len(image_elements) - 1:
            return (
                dmc.Group(
                    children=[
                        html.Div(image_elements[value - 2], style={"opacity": 0.25}),
                        html.Div(image_elements[value - 1], style={"opacity": 0.5}),
                        dmc.Tooltip(
                            image_elements[value],
                            label="Select an Avatar",
                            withArrow=True,
                            arrowSize=6,
                            opened=True,
                        ),
                    ],
                    align="center",
                    position='center'
                ),
                # image_elements[value],
            )
        elif value == len(image_elements):
            return (
                dmc.Group(
                    children=[
                        html.Div(image_elements[value - 2], style={"opacity": 0.25}),
                        html.Div(image_elements[value - 1], style={"opacity": 0.5}),
                        dmc.Tooltip(
                            image_elements[value],
                            label="Select an Avatar",
                            withArrow=True,
                            arrowSize=6,
                            opened=True,
                        ),
                    ],
                    align="center",
                    position='center'
                ),
                # image_elements[value],
            )

        elif i == value:
            # print('testing')
            # print(image_elements[i])
            return (
                dmc.Group(
                    [
                        html.Div(image_elements[i - 1], style={"opacity": 0.5}),
                        dmc.Tooltip(
                            image_elements[value],
                            label="Select an Avatar",
                            withArrow=True,
                            arrowSize=6,
                            opened=True,
                        ),
                        html.Div(image_elements[i + 1], style={"opacity": 0.5}),
                    ],
                    align="center",
                    position="center",
                ),
                # image_elements[value],
            )


@dash.callback(
    Output("profile-email", "children"),
    Output("profile-donation-link", "children"),
    Output("profile-youtube-link", "children"),
    Output("profile-discord-link", "children"),
    Output("profile-reddit-link", "children"),
    Output("profile-github-link", "children"),
    Output("profile-snapchat-link", "children"),
    Output("profile-dm-link", "children"),
    Output("profile-website-link", "children"),
    Output('profile-email-mirror', 'children'),
    Output("profile-username", "children"),
    Output("profile-about-me", "children"),
    Output("profile-credits", "children"),
    Output('profile-mirror', 'children'),
    Output('donation', 'children'),
    Output('youtube', 'children'),
    Output('discord', 'children'),
    Output('reddit', 'children'),
    Output('github', 'children'),
    Output('snapchat', 'children'),
    Output('dm', 'children'),
    Output('r-theme-register-select', 'children'),
    # Output("profile-qr-code", "children"),
    Input('auth-store', 'data'),
)
def update(data):
    print('check the pull request on the profile of the active user')
    print(data)
    if data:
        print('testing key username')
        # print(data['data'][0][0])
        # print(type(data['data'][0][0]))
        # print('testing user info')
        user_info = get_user_info(username=data['username'])
        print(user_info)
        # Components updating
        email = user_info['email']
        donation_link = user_info['donation_link']
        youtube_link = user_info['youtube_link']
        discord_link = user_info['discord_link']
        reddit_link = user_info['reddit_link']
        github_link = user_info['github_link']
        snapchat_link = user_info['snapchat_link']
        dm_link = user_info['dm_link']
        website_link = user_info['website_link']
        about_me = user_info['description']
        credits = user_info['credits']
        avatar = html.Img(src=f'http://127.0.0.1:8000/media/{user_info["avatar"]}',
                          style={"width": "200px", "height": "250px"})

        # qr_code = user_info['qr_image']
        theme = user_info['theme']

        theme_slider = dmc.Select(
            label="Select a Theme",
            placeholder="What Theme do you like?",
            id="r-theme-register-select",
            value=f"{theme}",
            data=[
                {"value": "BOOTSTRAP", "label": "Bootstrap"},
                {"value": "CERULEAN", "label": "Cerulean"},
                {"value": "COSMO", "label": "Cosmo"},
                {"value": "CYBORG", "label": "Cyborg"},
                {"value": "DARKLY", "label": "Darkly"},
                {"value": "FLATLY", "label": "Flatly"},
                {"value": "JOURNAL", "label": "Journal"},
                {"value": "LITERA", "label": "Litera"},
                {"value": "LUMEN", "label": "Lumen"},
                {"value": "LUX", "label": "Lux"},
                {"value": "MATERIA", "label": "Materia"},
                {"value": "MINTY", "label": "Minty"},
                {"value": "MORPH", "label": "Morph"},
                {"value": "PULSE", "label": "Pulse"},
                {"value": "QUARTZ", "label": "Quartz"},
                {"value": "SANDSTONE", "label": "SandStone"},
                {"value": "SIMPLEX", "label": "Simplex"},
                {"value": "SKETCHY", "label": "Sketchy"},
                {"value": "SLATE", "label": "Slate"},
                {"value": "SOLAR", "label": "Solar"},
                {"value": "SPACELAB", "label": "SpaceLab"},
                {"value": "SUPERHERO", "label": "SuperHero"},
                {"value": "UNITED", "label": "United"},
                {"value": "VAPOR", "label": "Vapor"},
                {"value": "YETI", "label": "Yeti"},
                {"value": "ZEPHYR", "label": "Zephyr"},
            ],
            style={"marginBottom": 10},
        )

        email_form = dmc.TextInput(label="Change Your Email",
                                   style={"width": "100%"},
                                   placeholder=f"{email}",
                                   icon=DashIconify(
                                       icon="ic:round-alternate-email"
                                   ),
                                   id='email-value'
                                   )

        donation_link_form = dmc.TextInput(label="Add a Donation Link:",
                                           style={"width": "100%"},
                                           placeholder=f"{donation_link}",
                                           icon=DashIconify(
                                               icon="flat-color-icons:money-transfer"
                                           ),
                                           id='donation-value'
                                           )

        youtube_link_form = dmc.TextInput(label="Add a Youtube Link:",
                                          style={"width": "100%"},
                                          placeholder=f"{youtube_link}",
                                          icon=DashIconify(
                                              icon="logos:youtube-icon"
                                          ),
                                          id='youtube-value'
                                          )

        discord_link_form = dmc.TextInput(label="Add a Discord Link:",
                                          style={"width": "100%"},
                                          placeholder=f"{discord_link}",
                                          icon=DashIconify(
                                              icon="logos:discord-icon"
                                          ),
                                          id='discord-value'
                                          )

        reddit_link_form = dmc.TextInput(label="Add a r/reddit Link or Username:",
                                         style={"width": "100%"},
                                         placeholder=f"{reddit_link}",
                                         icon=DashIconify(
                                             icon="line-md:reddit-loop"
                                         ),
                                         id='reddit-value'
                                         )

        github_link_form = dmc.TextInput(label="Add a Github Link:",
                                         style={"width": "100%"},
                                         placeholder=f"{github_link}",
                                         icon=DashIconify(
                                             icon="typcn:social-github-circular"
                                         ),
                                         id='github-value'
                                         )

        snapchat_link_form = dmc.TextInput(label="Add a Snapchat Link:",
                                           style={"width": "100%"},
                                           placeholder=f"{snapchat_link}",
                                           icon=DashIconify(
                                               icon="fa-brands:snapchat-square",
                                               style={"color": "yellow"},
                                           ),
                                           id='snapchat-value'
                                           )

        dm_link_form = dmc.TextInput(label="Add a DM Link:",
                                     style={"width": "100%"},
                                     placeholder=f"{dm_link}",
                                     icon=DashIconify(
                                         icon="openmoji:mobile-message"
                                     ),
                                     id='dm-value'
                                     )

        website_link_form = dmc.TextInput(label="Add a Website Link:",
                                          style={"width": "100%"},
                                          placeholder=f"{website_link}",
                                          icon=DashIconify(
                                              icon="carbon:app"
                                          ),
                                          id='website-value'
                                          )
        username = f"Username: {data['username']}"

        profile_email_mirror = f"Email: {email}"

        about_me = dmc.Textarea(label="About Me:",
                                placeholder=f"{about_me}",
                                style={"width": 500},
                                autosize=True,
                                minRows=2,
                                maxRows=4,
                                id='about-me-value'
                                )

        credits = f"${credits}"

        don = html.A(
            href=f"{donation_link}",
            children=[
                DashIconify(
                    icon="flat-color-icons:money-transfer",
                    width=32,
                )
            ],
        )
        yt = html.A(
            href=f"{youtube_link}",
            children=[
                DashIconify(
                    icon="logos:youtube-icon",
                    width=32,
                )
            ],
        )
        dc = html.A(
            href=f"{discord_link}",
            children=[
                DashIconify(
                    icon="logos:discord-icon",
                    width=32,
                )
            ],
        )
        red = html.A(
            href=f"{reddit_link}",
            children=[
                DashIconify(
                    icon="line-md:reddit-loop",
                    width=32,
                    style={
                        "color": "rgb(255, 69, 0)"
                    },
                )
            ],
        )
        git = html.A(
            href=f"{github_link}",
            children=[
                DashIconify(
                    icon="typcn:social-github-circular",
                    style={
                        "color": "gray"
                    },
                    width=32,
                )
            ],
        )
        snap = html.A(
            href=f"{snapchat_link}",
            children=[
                DashIconify(
                    icon="fa-brands:snapchat-square",
                    style={
                        "color": "yellow"
                    },
                    width=32,
                )
            ],
        )
        dm = html.A(
            href=f"{dm_link}",
            children=[
                DashIconify(
                    icon="openmoji:mobile-message",
                    width=32,
                )
            ],
        )


        print()
        # qr_code = html.Img(src=f'http://0.0.0.0:8000/{qr_code}', style={"width": "100%"})
        print('Testing account data')
        print(f'email_form: {email_form}')
        print(f'donation_link_form: {donation_link_form}')
        print(f'youtube_link_form: {youtube_link_form}')
        print(f'discord_link_form: {discord_link_form}')
        print(f'reddit_link_form: {reddit_link_form}')
        print(f'github_link_form: {github_link_form}')
        print(f'snapchat_link_form: {snapchat_link_form}')
        print(f'dm_link_form: {dm_link_form}')
        print(f'website_link_form: {website_link_form}')
        print(f'profile_email_mirror: {profile_email_mirror}')
        print(f'username: {username}')
        print(f'about_me: {about_me}')
        print(f'credits: {credits}')
        print(f'avatar: {avatar}')
        print(f'don: {don}')
        print(f'yt: {yt}')
        print(f'dc: {dc}')
        print(f'red: {red}')
        print(f'git: {git}')
        print(f'snap: {snap}')
        print(f'dm: {dm}')
        print(f'theme_slider: {theme_slider}')
        print()


        return email_form, donation_link_form, youtube_link_form, discord_link_form, reddit_link_form, \
            github_link_form, snapchat_link_form, dm_link_form, website_link_form, profile_email_mirror, username, \
            about_me, credits, avatar, don, yt, dc, red, git, snap, dm, theme_slider


    else:
        return dash.no_update



@dash.callback(
    Output('redirect-save-profile', 'href'),
    # Output("profile-qr-code", "children"),
    [
        Input('save-profile', 'n_clicks'),
        Input("email-value", "value"),
        Input('donation-value', 'value'),
        Input('youtube-value', 'value'),
        Input('discord-value', 'value'),
        Input('reddit-value', 'value'),
        Input('github-value', 'value'),
        Input('snapchat-value', 'value'),
        Input('dm-value', 'value'),
        Input('website-value', 'value'),
        Input('about-me-value', 'value'),
        Input("profile-select-slider", "value"),
        Input('r-theme-register-select', 'value'),
        Input('auth-store', 'data'),
    ]
)
def update_profile(save, email_v, donation_v, youtube_v, discord_v, reddit_v, github_v, snapchat_v, dm_v, website_v, about_v, profile_v, theme, data):
    # print(colorama.Fore.GREEN+'check the Update Profile')
    if save:
        print('Testing Save Update - Profile')
        print(colorama.Fore.YELLOW+'cookie:' + colorama.Fore.RESET)
        # print(cookieJar)
        keys = []
        # for c in cookieJar:
        #     if c.name == 'account_cookie':
        #         keys.append([c.domain, c.comment])
        print(colorama.Fore.GREEN+'testing key')
        print(colorama.Fore.RESET+data['username'])


        user_info = get_user_info(data['username'])

        print(user_info)
        # Components updating
        if email_v:
            email = email_v
        else:
            email = user_info['email']
        if donation_v:
            donation_link = donation_v
        elif donation_v == None:
            donation_link = 'www.paypal.com'
        else:
            donation_link = user_info['donation_link']
        if youtube_v:
            youtube_link = youtube_v
        elif youtube_v == None:
            youtube_link = 'www.youtube.com'
        else:
            youtube_link = user_info['youtube_link']
        if discord_v:
            discord_link = discord_v
        elif discord_v == None:
            discord_link = 'www.discord.com'
        else:
            discord_link = user_info['discord_link']
        if reddit_v:
            reddit_link = reddit_v
        elif reddit_v == None:
            reddit_link = 'www.reddit.com'
        else:
            reddit_link = user_info['reddit_link']
        if github_v:
            github_link = github_v
        elif github_v == None:
            github_link = 'github.com'
        else:
            github_link = user_info['github_link']
        if snapchat_v:
            snapchat_link = snapchat_v
        elif snapchat_v == None:
            snapchat_link = 'snapchat.com'
        else:
            snapchat_link = user_info['snapchat_link']
        if dm_v:
            dm_link = dm_v
        elif dm_v == None:
            dm_link = 'dm.com'
        else:
            dm_link = user_info['dm_link']
        if website_v:
            website_link = website_v
        elif website_v == None:
            website_link = 'austinkiese.com'
        else:
            website_link = user_info['website_link']
        if about_v:
            about_me = about_v
        elif about_v:
            about_me = 'Add some context about yourself.'
        else:
            about_me = user_info['description']

        avatar = raw_image_element[profile_v]

        print('Testing Update Avatar')
        print(avatar)

        account_updated = update_account(username=data['username'], email=email, avatar=avatar, description=about_me,
                       donation=donation_link, youtube=youtube_link, discord=discord_link, reddit=reddit_link,
                       github=github_link, snapchat=snapchat_link, dm=dm_link, website=website_link,
                       theme=theme)

        print('why update_account')
        print(account_updated)

        return '/profile'
    else:
        return dash.no_update