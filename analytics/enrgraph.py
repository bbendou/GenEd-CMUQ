import requests
import pandas as pd
import plotly.graph_objects as go

def create_enrollment_line_graph(course_code: str, semester: str = None):
    """
    Fetches enrollment data from the API endpoint and creates a line graph 
    showing total enrollment by semester for the specified course.
    
    Parameters:
      - course_code (str): The course code to query (user input).
      - semester (str, optional): An optional semester filter.
      
    Returns:
      A Plotly Figure object representing enrollment trends.
    """
    # API endpoint for enrollment data
    API_URL = "http://127.0.0.1:8000/enrollment"
    
    # Set up query parameters
    params = {"course_code": course_code}
    if semester and semester.strip():
        params["sem"] = semester.strip()
    
    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

    data = response.json()  # expecting a list of dictionaries
    if not data:
        print("No enrollment data available for the given parameters.")
        return None

    # Convert JSON data to a DataFrame
    df = pd.DataFrame(data)
    if df.empty:
        print("No enrollment data available after conversion.")
        return None

    # Aggregate total enrollment by semester
    df_grouped = df.groupby("semester")["enrollment_count"].sum().reset_index()
    df_grouped = df_grouped.sort_values("semester")  # sort by semester

    # Create a line graph using Plotly
    fig = go.Figure(
        data=go.Scatter(
            x=df_grouped["semester"],
            y=df_grouped["enrollment_count"],
            mode="lines+markers",
            name=course_code,
            hovertemplate="Enrollment: %{y}<extra></extra>"
        )
    )
    fig.update_layout(
        title=f"Enrollment Trends for {course_code}",
        xaxis_title="Semester",
        yaxis_title="Total Enrollment",
        margin={"l": 50, "r": 50, "t": 50, "b": 50}
    )
    
    return fig

if __name__ == "__main__":
    course_code = input("Enter course code: ").strip()
    semester = input("Enter semester (optional): ").strip()
    fig = create_enrollment_line_graph(course_code, semester if semester != "" else None)
    if fig:
        fig.show()
