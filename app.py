import dash_editor_components
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import requests
from time import time
import os


app = dash.Dash(__name__)
server = app.server

with open("solution_template.py") as template:
    solution_template = template.read()


app.layout = html.Div([
    html.Div([
        html.Div([
            dash_editor_components.PythonEditor(
                id="code_input",
                value=solution_template,
                className="code-box"),
        ], className="five columns double scrolled"),
        html.Div([
            html.Div([
                html.Div([
                    html.Pre("The results of your code will appear here",
                             id="code_output", className="code-box code-box-height")
                ]),
                html.Br(),
                html.Div([
                    html.Pre("The output printed to console will appear here",
                             id="console_output", className="code-box code-box-height")
                ])
            ], className="row"),
        ], className="five columns"),
    ], className="row"),

    html.Div([
        html.Div([
            html.Button("Submit code", id="code_test", n_clicks=0),
        ], className="two columns"),
        html.Div([
            html.Button("Submit code", id="code_submit", n_clicks=0),
        ], className="two columns"),
    ], className="row"),

    html.Br(),
    html.Br(),
    html.Br(),

    html.Div([
        html.Div([
            html.H4("DEBUG WINDOW"),
            html.H5("Snapshots for user kmourat"),
            html.H6("./snapshots/kmourat"),
            html.Hr(),
            html.Div([
                html.P(file)
                for file in os.listdir("snapshots/kmourat")
            ], id="snapshot_debug", className="scrolled")
        ], className="five columns code-box"),
        html.Div([
            # Max = max intervals per task
            # For 1 snapshot per 1.5 second (40 per minute)
            # and 60 minutes we get max = 60 * 60
            dcc.Slider(id="select_snapshot", min=0, max=20, step=1,
                       marks={}),
            html.Div(html.Pre(id="file_preview"), className="scrolled"),
        ], className="five columns")
    ], className="row", style={"padding": "15px"}),

    # Every 1.5 second
    dcc.Interval(id="interval", interval=1.5 * 1000, n_intervals=0),
    dcc.Textarea(value=".", id="prev_code_input", style={"display": "none"})
])


@app.callback([Output("code_output", "children"),
               Output("console_output", "children")],
              [Input("code_test", "n_clicks")],
              [State("code_input", "value")])
def execute_code(n_clicks, code):
    if n_clicks < 1 or code is None:
        raise PreventUpdate

    try:
        resp = requests.post("http://127.0.0.1:5000/code/kostas",
                             json={"code": code})
        code_output = resp.json()["code_output"]
        console_output = str(resp.json()["console_output"])

        return [
            [html.Div([html.H4(k), html.Pre("Output: " + str(v)), html.Hr()])
             for (k, v) in code_output.items()],
            str(console_output)
        ]

    except Exception as e:
        return str(e)


@app.callback([Output("prev_code_input", "value"),
               Output("snapshot_debug", "children"),
               Output("select_snapshot", "marks"),
               Output("select_snapshot", "max")],
              [Input("interval", "n_intervals")],
              [State("code_input", "value"),
               State("prev_code_input", "value")])
def track_code_modifications(n_intervals, code, prev_code):
    if not all([n_intervals, code, prev_code]):
        raise PreventUpdate

    elif abs(len(code) - len(prev_code)) < 5:
        raise PreventUpdate

    user = "kmourat"
    n_intervals = str(n_intervals).zfill(5)
    base_dir = f"snapshots/{user}"
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)

    with open(f"{base_dir}/n{n_intervals}.py", "w") as snapshot:
        snapshot.write(code)

    intervals = [int(f[1:-3]) for f in os.listdir("snapshots/kmourat")]

    return [
        code,
        [html.P(file) for file in os.listdir("snapshots/kmourat")],
        {interval: str(interval) for interval in intervals},
        max(intervals)
    ]


@app.callback(Output("file_preview", "children"),
              [Input("select_snapshot", "value")])
def show_file_preview(interval):
    if interval is None:
        raise PreventUpdate

    try:
        files = [int(f[1:-3]) for f in os.listdir("snapshots/kmourat")]
        with open(f"snapshots/kmourat/n{str(interval).zfill(5)}.py") as snapshot:
            preview_file = snapshot.read()

        return preview_file

    except FileNotFoundError:
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
