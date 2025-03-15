import os
import pandas as pd
import plotly.graph_objects as go


def main():
    # Construct the path to the data directory where the Excel files are stored (data/audit)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "..", "data", "audit")

    # Optional: Print paths to verify
    data_path_counts = os.path.join(data_dir, "Countsfor.xlsx")
    data_path_reqs = os.path.join(data_dir, "Requirement.xlsx")

    # 1. Load the Excel files using the correct paths
    df_counts = pd.read_excel(data_path_counts, engine="openpyxl")
    df_reqs = pd.read_excel(data_path_reqs, engine="openpyxl")

    # 2. Merge on 'requirement'
    df_merged = pd.merge(df_counts, df_reqs, on="requirement", how="left")

    # 3. Extract the major code from something like "is_0" -> "is"
    df_merged["major"] = df_merged["audit_id"].apply(
        lambda x: x.split("_")[0] if pd.notnull(x) else None
    )

    # 4. (Optional) Map short codes to full major names
    major_map = {
        "is": "Information Systems",
        "ba": "Business Administration",
        "cs": "Computer Science",
        "bio": "Biological Sciences",
    }
    df_merged["major"] = df_merged["major"].map(major_map)

    # 5. Create a short requirement label by taking the text after the last '---'
    df_merged["short_requirement"] = df_merged["requirement"].apply(
        lambda x: x.split("---")[-1].strip()
    )

    # 6. Group by major, short_requirement, and (optionally) semester if your data had it
    grouped = (
        df_merged.groupby(["major", "short_requirement"])["course_code"]
        .nunique()
        .reset_index(name="NumCourses")
    )

    # 7. Get a sorted list of unique majors
    majors = sorted(grouped["major"].dropna().unique())

    def get_trace(selected_major):
        data = grouped[grouped["major"] == selected_major].copy()
        data = data.sort_values(by="NumCourses", ascending=True)
        trace = go.Bar(
            x=data["NumCourses"],
            y=data["short_requirement"],
            orientation="h",
            name=selected_major,
        )
        return trace

    # Initialize the figure with the first major
    init_major = majors[0]
    init_trace = get_trace(init_major)
    fig = go.Figure(data=[init_trace])

    # Create dropdown menu for major selection (no 'title' key, to avoid the ValueError)
    buttons_major = []
    for m in majors:
        buttons_major.append(
            {
                "label": m,
                "method": "update",
                "args": [
                    {"data": [get_trace(m)]},
                    {"title": f"Course Count per Requirement for {m}"},
                ],
            }
        )

    fig.update_layout(
        updatemenus=[
            {
                "buttons": buttons_major,
                "direction": "down",
                "x": 0.0,
                "xanchor": "left",
                "y": 1.15,
                "yanchor": "top",
                "showactive": True,
                "pad": {"r": 10, "t": 10},
            }
        ],
        title=f"Course Count per Requirement for {init_major}",
        xaxis_title="Number of Courses",
        yaxis_title="Requirement",
        margin={"l": 100, "r": 100, "t": 150, "b": 50},
    )

    # Add an annotation to label the dropdown
    fig.add_annotation(
        x=0.0,
        y=1.22,
        xanchor="left",
        yanchor="top",
        text="Select Major:",
        showarrow=False,
        font={"size": 12},
    )

    fig.show()


if __name__ == "__main__":
    main()
