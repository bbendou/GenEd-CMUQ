import dash
from dash import dcc, html, Input, Output
import requests
import pandas as pd
import plotly.graph_objects as go

# Base URL for your FastAPI endpoint (adjust as needed)
API_BASE_URL = "http://localhost:8000"

# Define available majors (mapping code to full name)
majors = {
    "is": "Information Systems",
    "ba": "Business Administration",
    "cs": "Computer Science",
    "bio": "Biological Sciences"
}

def fetch_course_coverage(major_code, semester=None):
    """
    Call the /analytics/course-coverage endpoint with the selected major and optional semester.
    Returns the JSON response.
    """
    params = {"major": major_code}
    if semester:
        params["semester"] = semester
    response = requests.get(f"{API_BASE_URL}/analytics/course-coverage", params=params)
    if response.status_code != 200:
        raise Exception(f"API call failed with status code {response.status_code}")
    return response.json()

def create_figure(major_code, semester):
    """
    Fetch data for the given major and semester, then build a Plotly horizontal bar chart.
    """
    data = fetch_course_coverage(major_code, semester)
    # The API returns a dict with keys: "major", "semester", and "coverage" (a list of dicts).
    df = pd.DataFrame(data.get("coverage", []))
    if df.empty:
        fig = go.Figure()
        fig.update_layout(title="No data returned for the selected parameters.")
        return fig

    # Extract a short requirement label (using the part after the last '---')
    df["short_requirement"] = df["requirement"].apply(lambda x: x.split("---")[-1].strip())
    if "num_courses" in df.columns:
        df = df.rename(columns={"num_courses": "NumCourses"})
    df_sorted = df.sort_values("NumCourses", ascending=True)

    fig = go.Figure(
        data=[
            go.Bar(
                x=df_sorted["NumCourses"].tolist(),
                y=df_sorted["short_requirement"].tolist(),
                orientation="h",
                hovertemplate="Count: %{x}<extra></extra>"
            )
        ]
    )
    title_text = f"Course Count per Requirement for {majors[major_code]}"
    if semester:
        title_text += f" ({semester})"
    fig.update_layout(
        title=title_text,
        xaxis_title="Number of Courses",
        yaxis_title="Requirement",
        margin={"l": 150, "r": 50, "t": 50, "b": 50},
    )
    return fig

# Create Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Course Coverage Dashboard"),
    html.Div([
        html.Label("Select Major:"),
        dcc.Dropdown(
            id="major-dropdown",
            options=[{"label": name, "value": code} for code, name in majors.items()],
            value="bio"  # default major
        ),
    ], style={"width": "300px", "display": "inline-block", "verticalAlign": "top", "marginRight": "50px"}),
    html.Div([
        html.Label("Enter Semester (optional):"),
        dcc.Input(
            id="semester-input",
            type="text",
            placeholder="e.g., F23",
            value="",
        )
    ], style={"width": "300px", "display": "inline-block", "verticalAlign": "top"}),
    dcc.Graph(id="coverage-graph")
])

@app.callback(
    Output("coverage-graph", "figure"),
    Input("major-dropdown", "value"),
    Input("semester-input", "value")
)
def update_graph(selected_major, semester):
    # Clean the semester input: use None if empty or only whitespace.
    semester = semester.strip() if semester and semester.strip() else None
    fig = create_figure(selected_major, semester)
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
