import os
import dash
import pandas as pd
from dash import Dash, Input, Output, State, dcc, html
from dash.exceptions import PreventUpdate
from dash_ag_grid.AgGrid import AgGrid
from collections import namedtuple
from typing import Final
from PyPinch import PyPinch
from io import BytesIO
import matplotlib.pyplot as plt
import base64
import traceback
import math

from agility.components import (
    ButtonCustom,
    InputCustom,
    MessageCustom,
    DropdownCustom,
    CheckboxCustom,
    DisplayField,
    ContainerCustom,
)

from pinch.config.main import STORE_ID
from pinch.project import page2
from pinch.schemas.page2 import Page2Input, generate_table_record

from typing import Final

dash.register_page(__name__)
app: Dash = dash.get_app()


PAGE_TITLE = "Shifted Temperature Interval diagram"


class PageIDs:
    def __init__(self) -> None:
        # Get the base name of the file where this instance is created
        filename = os.path.basename(__file__)
        # Remove the file extension to use only the file name as the prefix
        prefix: Final[str] = filename.replace(".py", "")
        self.prefix: Final[str] = prefix
        self.status: Final[str] = f"{prefix}_status"
        self.output_data1: Final[str] = f"{prefix}_output_data1"
        self.run_pinch1: Final[str] = f"{prefix}_run_pinch1"


ids = PageIDs()


layout = html.Div(
    [
        html.H1("pinch", className="app-title"),
        html.H2(PAGE_TITLE, className="page-title"),
        html.Hr(),
        html.Div(
            children="This diagram breaks down the temperature range into intervals based on \u0394Tₘᵢₙ and the stream data. It identifies temperature ranges where heat exchange can potentially take place."
        ),
        # html.Div(id="output_data1", style={"margin-top": "20px"}),
        html.Br(),
        ButtonCustom(
            label="Show The Temperature Interval Diagram", id="run_pinch1"
        ).layout,
        dcc.Loading(
            id="loading", children=[html.Div(id="output_data1")], type="default"
        ),
    ]
)


@app.callback(Output("output_data1", "children"), [Input("run_pinch1", "n_clicks")])
def run_pinch_analysis(n_clicks):
    csv_file_path = os.path.join(os.getcwd(), "pinch_analysis_data.csv")

    if n_clicks and os.path.exists(csv_file_path):
        try:
            # Run the PyPinch analysis
            options = {"draw"}
            pinch = PyPinch(csv_file_path, options)
            pinch.solve(options)  # Ensure that this runs without error

            # Define paths for the generated images
            image_files = [
                "ShiftT.png", 
            ]
            images_divs = []

            # Convert each image to base64 and create img tags
            for image_file in image_files:
                image_path = os.path.join(os.getcwd(), image_file)

                if os.path.exists(image_path):
                    with open(image_path, "rb") as img_file:
                        image_base64 = base64.b64encode(img_file.read()).decode("utf-8")
                        images_divs.append(
                            html.Div(
                                [
                                    #html.H3(image_file.split(".")[0].replace("_", " ")),
                                    html.Img(
                                        src=f"data:image/png;base64,{image_base64}",
                                        style={"width": "50%", "height": "auto"},
                                    ),
                                ]
                            )
                        )
                else:
                    print(f"Image file not found: {image_path}")

            if not images_divs:
                return html.Div([html.H3("No images were generated.")])

            return html.Div(images_divs)

        except Exception as e:
            print(traceback.format_exc())  # Print the traceback for debugging
            return html.Div(
                [html.H3("An error occurred while running PyPinch:"), html.P(str(e))]
            )

    return html.Div("No analysis run yet or missing input file.")