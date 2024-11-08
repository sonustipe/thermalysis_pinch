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

from thermalysis_pinch.config.main import STORE_ID
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
        self.output_datan: Final[str] = f"{prefix}_output_datan"
        self.run_pinch_csv: Final[str] = f"{prefix}_run_pinch_csv"


ids = PageIDs()


layout = html.Div(
    [
        # html.Div(id="pinch_results", style={"margin-top": "20px"}),
        html.H1("pinch", className="app-title"),
        html.H2(PAGE_TITLE, className="page-title"),
        html.Hr(),
        html.Div(
            'The pinch point is the temperature level where the process is most constrained thermally, meaning no further heat exchange can occur without violating \u0394Tₘᵢₙ. The pinch point is critical for targeting maximum heat recovery. It divides the process into distinct "above pinch" and "below pinch" regions, guiding the placement of heat exchangers for optimal energy recovery.'
        ),
        html.Br(),
        ButtonCustom(label="Pinch Point", id="run_pinch_csv").layout,
        dcc.Loading(
            id="loading", children=[html.Div(id="output_datan")], type="default"
        ),
    ]
)


@app.callback(Output("output_datan", "children"), [Input("run_pinch_csv", "n_clicks")])
def run_csv_pinch_analysis(n_clicks):
    csv_file_path = os.path.join(os.getcwd(), "pinch_analysis_data.csv")

    if n_clicks and os.path.exists(csv_file_path):
        try:
            # Run the PyPinch analysis with CSV option
            options = {"csv"}
            pinchen = PyPinch(csv_file_path, options)
            pinchen.solve(options)

            # Load HeatCascade.csv and get the last row
            heat_cascade_path = os.path.join(os.getcwd(), "HeatCascade.csv")
            if os.path.exists(heat_cascade_path):
                heat_cascade_df = pd.read_csv(heat_cascade_path)

                # Check if DataFrame is empty
                if heat_cascade_df.empty:
                    return html.Div(
                        [
                            html.H3("HeatCascade.csv is empty."),
                        ]
                    )

                last_row = heat_cascade_df.tail(1)  # Get the last row

                # Extract the last row as a string
                last_row_str = last_row.to_string(index=False, header=False).strip()

                # Find the line containing "Pinch Temperature" and extract the value
                if "Pinch Temperature" in last_row_str:
                    # Split the string and extract the temperature value
                    pinch_temp_str = last_row_str.split("Pinch Temperature: ")[
                        1
                    ]  # Get the part after the label
                    pinch_temp_value = pinch_temp_str.split(" degC")[
                        0
                    ].strip()  # Get the numeric part

                    return html.Div(
                        [
                            # html.H3("CSV Pinch Analysis Complete"),
                            html.Pre(
                                f"Pinch Temperature: {pinch_temp_value} °C"
                            ),  # Display the temperature value
                        ]
                    )
                else:
                    return html.Div(
                        [
                            html.H3("Pinch Temperature not found in the last row."),
                        ]
                    )
            else:
                return html.Div(
                    [
                        html.H3("HeatCascade.csv not found."),
                    ]
                )
        except Exception as e:
            return html.Div(
                [
                    html.H3("An error occurred while running the CSV Pinch analysis:"),
                    html.P(str(e)),
                ]
            )

    return html.Div()
