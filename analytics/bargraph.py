# import requests
# import plotly.graph_objects as go
# import pandas as pd

# # Base URL for your API endpoints (adjust if needed)
# API_BASE_URL = "http://127.0.0.1:8000/courses"

# def fetch_requirement_coverage(major: str, semester: str):
#     """
#     Calls the API endpoint to get analytics data instead of reading Excel files directly.
#     Expected endpoint: GET /courses/analytics?major=<major>&semester=<semester>
#     """
#     url = f"{API_BASE_URL}/analytics"
#     params = {"major": major, "semester": semester}
#     response = requests.get(url, params=params)
#     response.raise_for_status()  # raises an HTTPError for bad responses
#     return response.json()

# def create_bargraph(data, selected_major: str):
#     """
#     Given analytics data (list of dicts with keys: major, short_requirement, NumCourses),
#     create and display a horizontal bar graph using Plotly.
#     """
#     if not data:
#         print("No data available to plot.")
#         return

#     # Convert the JSON data into a DataFrame for easier plotting
#     df_grouped = pd.DataFrame(data)
#     # Get all majors in the data
#     majors = sorted(df_grouped["major"].dropna().unique())

#     def get_trace(major: str):
#         subset = df_grouped[df_grouped["major"] == major].copy()
#         subset = subset.sort_values(by="NumCourses", ascending=True)
#         return go.Bar(
#             x=subset["NumCourses"],
#             y=subset["short_requirement"],
#             orientation="h",
#             name=major,
#         )

#     init_trace = get_trace(selected_major)
#     fig = go.Figure(data=[init_trace])

#     # Create a dropdown for selecting different majors
#     buttons = []
#     for m in majors:
#         buttons.append({
#             "label": m,
#             "method": "update",
#             "args": [
#                 {"data": [get_trace(m)]},
#                 {"title": f"Course Count per Requirement for {m}"}
#             ]
#         })

#     fig.update_layout(
#         updatemenus=[{
#             "buttons": buttons,
#             "direction": "down",
#             "x": 0.0,
#             "xanchor": "left",
#             "y": 1.15,
#             "yanchor": "top",
#             "showactive": True,
#             "pad": {"r": 10, "t": 10}
#         }],
#         title=f"Course Count per Requirement for {selected_major}",
#         xaxis_title="Number of Courses",
#         yaxis_title="Requirement",
#         margin={"l": 100, "r": 100, "t": 150, "b": 50}
#     )
#     fig.add_annotation(
#         x=0.0,
#         y=1.22,
#         xanchor="left",
#         yanchor="top",
#         text="Select Major:",
#         showarrow=False,
#         font={"size": 12},
#     )
#     fig.show()

# def main():
#     """
#     Client entry point for the bar graph.
#     Instead of reading from Excel, it fetches data from the API endpoint.
#     """
#     major = input("Enter major (e.g., IS): ").strip().upper()
#     semester = input("Enter semester (e.g., F21): ").strip().upper()
#     try:
#         data = fetch_requirement_coverage(major, semester)
#         create_bargraph(data, major)
#     except Exception as e:
#         print("Error fetching or plotting data:", e)

