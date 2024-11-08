import os
import dash
import pandas as pd
from dash import Dash, Input, Output, State, dcc, html, dash_table
from dash.exceptions import PreventUpdate
from dash_ag_grid.AgGrid import AgGrid
from plotly import graph_objects as go
import plotly.express as px
from collections import namedtuple
from typing import Final
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

# from pinch.project import page1

from typing import Final

dash.register_page(__name__)
app: Dash = dash.get_app()


PAGE_TITLE = "Data Collection"


class PageIDs:
    def __init__(self) -> None:
        # Get the base name of the file where this instance is created
        filename = os.path.basename(__file__)
        # Remove the file extension to use only the file name as the prefix
        prefix: Final[str] = filename.replace(".py", "")
        self.prefix: Final[str] = prefix
        self.status: Final[str] = f"{prefix}_status"
        self.input: Final[str] = f"{prefix}_input"

        self.stream_inputs: Final[str] = f"{prefix}_str_inputs"
        self.submit_streams: Final[str] = f"{prefix}_str_submit"
        self.num_streams: Final[str] = f"{prefix}_num_str"
        self.output_table: Final[str] = f"{prefix}_op_table"
        self.save_confirmation: Final[str] = f"{prefix}_save_conf"
        self.collect_data: Final[str] = f"{prefix}_clt_data"
        self.delta_t_min: Final[str] = f"{prefix}_dt_min"
        self.cp: Final[str] = f"{prefix}_cp"
        self.supply_temp: Final[str] = f"{prefix}_sup_temp"
        self.target_temp: Final[str] = f"{prefix}_tar_temp"


ids = PageIDs()


# callback function to display the input fields and save btn if project is loaded


layout = html.Div("Hello World")
# My homepage
# layout = html.Div(
#     [
#         # Input for delta T min
#         html.Div(
#             [
#                 InputCustom(
#                     id=ids.input,
#                     type="number",
#                     placeholder="Enter \u0394T min",
#                 ).layout,
#             ],
#         ),
#         # Input for the number of streams
#         html.Div(
#             [
#                 InputCustom(
#                     id=ids.num_streams,
#                     type="number",
#                     # addon_text="Enter the number of streams:",
#                     placeholder="Enter number of streams",
#                 ).layout,
#             ],
#             style={"margin-bottom": "20px"},
#         ),
#         # Button to submit number of streams
#         ButtonCustom(label="Submit Number of Streams", id=ids.submit_streams).layout,
#         # Div to show stream input fields
#         html.Div(ids.stream_inputs, style={"margin-top": "20px"}),
#         # Output Table
#         html.Div(ids.output_table, style={"margin-top": "20px"}),
#         # Confirmation message
#         html.Div(ids.save_confirmation, style={"margin-top": "20px", "color": "green"}),
#     ]
# )


# @app.callback(
#     Output(ids.status, "children"),
#     [Input(STORE_ID, "data")],
# )
# def load_status(data):

#     if data is None:
#         return MessageCustom(
#             messages="Project not loaded. Go to start page and create new or open existing project.",
#             success=False,
#         ).layout


# @app.callback(
#     Output(ids.input, "children"),
#     [Input(STORE_ID, "data")],
# )
# def display_input(data):


# # Callback to create the input fields based on the number of streams
# @app.callback(
#     Output(ids.stream_inputs, "children"),
#     [Input(ids.submit_streams, "n_clicks")],
#     [State(ids.num_streams, "value")],
# )
# def create_stream_inputs(n_clicks, num_streams):
#     if n_clicks > 0 and num_streams:
#         inputs = []

#         for i in range(num_streams):
#             inputs.append(
#                 html.Div(
#                     [
#                         html.H3(f"Stream {i + 1}"),
#                         InputCustom(
#                             id={"type": "cp", "index": i},
#                             type="number",
#                             # addon_text="Heat Capacity (Cp):",
#                             placeholder="Enter Cp",
#                         ).layout,
#                         html.Label("Supply Temperature (°C):"),
#                         InputCustom(
#                             id={"type": "supply-temp", "index": i},
#                             type="number",
#                             #  addon_text="Ts (°C):",
#                             placeholder="Enter supply temperature",
#                         ).layout,
#                         InputCustom(
#                             id={"type": "target-temp", "index": i},
#                             label="Target Temperature (°C):",
#                             #   addon_text="TT (°C):",
#                             type="number",
#                             placeholder="Enter target temperature",
#                             #  addon_text="°C",
#                         ).layout,
#                         html.Hr(),
#                     ]
#                 )
#             )

#         inputs.append(
#             ButtonCustom(
#                 "Collect Data",
#                 id="collect_data",
#                 n_clicks=0,
#                 style={"margin-top": "20px"},
#             )
#         )
#         return inputs

#     return None


# # Callback to collect and display data and save it as CSV
# @app.callback(
#     [
#         Output(ids.output_table, "children"),
#         Output(ids.save_confirmation, "children"),
#     ],
#     [Input(ids.collect_data, "n_clicks")],
#     [
#         State(ids.delta_t_min, "value"),
#         State({"type": ids.cp, "index": dash.dependencies.ALL}, "value"),
#         State({"type": ids.supply_temp, "index": dash.dependencies.ALL}, "value"),
#         State({"type": ids.target_temp, "index": dash.dependencies.ALL}, "value"),
#     ],
# )
# def display_table(n_clicks, delta_t_min, cps, supply_temps, target_temps):
#     if n_clicks > 0:
#         data = {
#             "Heat Capacity (Cp)": cps,
#             "Supply Temperature (°C)": supply_temps,
#             "Target Temperature (°C)": target_temps,
#         }

#         df = pd.DataFrame(data)

#         # Create the CSV structure
#         csv_data = [
#             ["Tmin", delta_t_min],  # First row
#             ["CP", "TSUPPLY", "TTARGET"],
#         ]  # Second row

#         for i in range(len(cps)):
#             csv_data.append([cps[i], supply_temps[i], target_temps[i]])

#         # Save to CSV
#         file_path = os.path.join(os.getcwd(), "pinch_analysis_data.csv")
#         with open(file_path, mode="w", newline="") as file:
#             for row in csv_data:
#                 file.write(",".join(map(str, row)) + "\n")

#         return (
#             html.Div(
#                 [
#                     html.H2(f"Collected Data (ΔT min = {delta_t_min} °C):"),
#                     dash_table.DataTable(
#                         data=df.to_dict("records"),
#                         columns=[{"name": i, "id": i} for i in df.columns],
#                         style_table={"overflowX": "auto"},
#                         style_cell={"textAlign": "center"},
#                     ),
#                 ]
#             ),
#             f"Data successfully saved to {file_path}",
#         )

#     return None, None
