from app import app
from pages import lightFuncs as lf
import random

try:
    from dash import dcc
    from dash import html
except ModuleNotFoundError:
    import dash_core_components as dcc
    import dash_html_components as html
from dash import callback
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

import skimage as ski
import pandas as pd
import random


colors = {
    'background': 'rgba(255, 245, 245, 0.85)',
    'title': 'rgb(26, 26, 26)',
    'text': 'rgb(38, 38, 38)',
}

layout = html.Div(id="main", children=[

    html.Div([
        dcc.Dropdown(
            id="laserColor_dropdown",
            options=[
                {'label': 'infrared (not visible), ca. 1000 nm', 'value': 1000},
                {'label': 'red (visible), ca. 700 nm', 'value': 700},
                {'label': 'green (visible), ca. 500 nm', 'value': 500},
                {'label': 'ultraviolet (not visible) ca. 300 nm', 'value': 300 }
            ],
            value=780
        )
    ],
    
    ),

    html.Div([
        html.Div([
            html.Img(
                src=app.get_asset_url("1024px-Laser.svg"),
                style={"width": "100%"}
            )
        ],
            className="two columns"
        ),
        html.Div(id="laserLine_div",
            className="two columns"
        ),
        html.Div([
            html.Img(
                src=app.get_asset_url("beamSplitter.png"),
                style={"width": "100%"}
            )
        ],
            className="two columns"
        ),

        html.Div(id="splitBeam",
            className="two columns"
        ),
    ],
        className="row",
        style={"margin": "1rem"}
    ),

    html.Div([
        dcc.RadioItems(id="pulseShape", options=[
                {
                    "label":
                        [
                            dbc.Card([
                                dbc.CardImg(src=app.get_asset_url("hg-zero.png"), top=True),
                                dbc.CardBody([
                                        html.H4("Zero-th Order", className="card-title"),
                                ]),
                            ],
                                style={
                                        "width": "18rem",
                                        "padding": "1rem",
                                        "margin": "1rem",
                                      },
                            )
                        ],
                    "value": 0.0000001
                },
                {
                    "label":
                        [
                            dbc.Card([
                                dbc.CardImg(src=app.get_asset_url("hg-first.png"), top=True),
                                dbc.CardBody([
                                        html.H4("First Order", className="card-title"),
                                ]),
                            ],
                                style={
                                        "width": "18rem",
                                        "padding": "1rem",
                                        "margin": "1rem",
                                      },
                            )
                        ], 
                    "value": 1,
                },
                {
                    "label":
                        [
                            dbc.Card([
                                dbc.CardImg(src=app.get_asset_url("hg-second.png"), top=True),
                                dbc.CardBody([
                                        html.H4("Second Order", className="card-title"),
                                ]),
                            ],
                                style={
                                        "width": "18rem",
                                        "padding": "1rem",
                                        "margin": "1rem",
                                      },
                            )
                        ],
                    "value": 2,
                },
                {
                    "label":
                        [
                            dbc.Card([
                                dbc.CardImg(src=app.get_asset_url("hg-third.png"), top=True),
                                dbc.CardBody([
                                        html.H4("Third Order", className="card-title"),
                                ]),
                            ],
                                style={
                                        "width": "18rem",
                                        "padding": "1rem",
                                        "margin": "1rem",
                                      },
                            )
                        ],
                    "value": 3,
                },
            ], 
                # labelStyle={"display": "flex", "align-items": "center"},
                inline=True
            )
    ]),

    # html.Div(id="drag_container", className="container", children=[
    #     html.Div([
    #         dbc.Card([
    #             dbc.CardImg(src=app.get_asset_url("hg-zero.png"), top=True),
    #             dbc.CardBody([
    #                     html.H4("Zero-th Order", className="card-title"),
    #             ]),
    #         ],
    #             style={"width": "18rem"},
    #         )
    #     ],
    #         style={"padding": "1rem"}
    #     ),
    #     html.Div([
    #         dbc.Card([
    #             dbc.CardImg(src=app.get_asset_url("hg-first.png"), top=True),
    #             dbc.CardBody([
    #                     html.H4("First Order", className="card-title"),
    #             ]),
    #         ],
    #             style={"width": "18rem"},
    #         )
    #     ],
    #         style={"padding": "1rem"}
    #     ),
    #     html.Div([
    #         dbc.Card([
    #             dbc.CardImg(src=app.get_asset_url("hg-second.png"), top=True),
    #             dbc.CardBody([
    #                     html.H4("Second Order", className="card-title"),
    #             ]),
    #         ],
    #             style={"width": "18rem"},
    #         )
    #     ],
    #         style={"padding": "1rem"}
    #     ),
    #     html.Div([
    #         dbc.Card([
    #             dbc.CardImg(src=app.get_asset_url("hg-third.png"), top=True),
    #             dbc.CardBody([
    #                     html.H4("Third Order", className="card-title"),
    #             ]),
    #         ],
    #             style={"width": "18rem"},
    #         )
    #     ],
    #         style={"padding": "1rem"}
    #     ),
    # ]),
])

# app.clientside_callback(
#     ClientsideFunction(namespace="clientside", function_name="make_draggable"),
#     Output("drag_container", "data-drag"),
#     [Input("drag_container", "id")],
# )


@callback(
    Output("laserLine_div", "children"),
    Input("laserColor_dropdown", "value")
)
def updateLaserColor(chosenLaser):

    # print("The selected input laser is", chosenLaser)
    
    outputColor = lf.wave2rgb(chosenLaser)
    # print(outputColor)
    
    return     html.Hr(
                    id="laserLine",
                    style={
                        "borderWidth": "0.5rem",
                        "width": "100%",
                        "borderColor": f"rgb{outputColor}",
                        "opacity": "100%",
                        "margin-top": "35%"
                    }
            )


@callback(
    Output("splitBeam", "children"),
    [Input("pulseShape", "value")],
    [State("laserColor_dropdown", "value")],
)
def updateLaserColor(chosenPulseShape, inputWaveL):

    print("The selected order HG mode is: ", chosenPulseShape)
    print("The wavelength of the input laser in nm is: ", inputWaveL)

    if chosenPulseShape is None:
        raise PreventUpdate

    outputWaveL = lf.some_fake_function_to_downconvert_when_run_through_a_beamsplitter(chosenPulseShape, inputWaveL)

    outputColor = lf.wave2rgb(outputWaveL)
    print(outputColor)
    
    return     html.Hr(
                    id="outputLine",
                    style={
                        "borderWidth": "0.5rem",
                        "width": "100%",
                        "borderColor": f"rgb{outputColor}",
                        "opacity": "100%",
                        "margin-top": "35%"
                    }
            )