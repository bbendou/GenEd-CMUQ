import os
import pandas as pd
import plotly.graph_objects as go


def generate_requirement_coverage():
    """
    Returns the grouped coverage data (as a list of dicts)
    for each major & requirement, rather than displaying a Plotly figure.
    """
    # 1) Build absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, "..", "data", "audit")
    data_path_counts = os.path.join(data_dir, "Countsfor.xlsx")
    data_path_reqs = os.path.join(data_dir, "Requirement.xlsx")

    # 2) Load data
    df_counts = pd.read_excel(data_path_counts, engine="openpyxl")
    df_reqs = pd.read_excel(data_path_reqs, engine="openpyxl")

    # 3) Merge
    df_merged = pd.merge(df_counts, df_reqs, on="requirement", how="left")

    # 4) Extract major code
    df_merged["major"] = df_merged["audit_id"].apply(
        lambda x: x.split("_")[0] if pd.notnull(x) else None
    )

    # 5) (Optional) Map short codes
    major_map = {
        "is": "Information Systems",
        "ba": "Business Administration",
        "cs": "Computer Science",
        "bio": "Biological Sciences",
    }
    df_merged["major"] = df_merged["major"].map(major_map)

    # 6) Short requirement label
    df_merged["short_requirement"] = df_merged["requirement"].apply(
        lambda x: x.split("---")[-1].strip()
    )

    # 7) Group
    grouped = (
        df_merged.groupby(["major", "short_requirement"])["course_code"]
        .nunique()
        .reset_index(name="NumCourses")
    )

    # 8) Return as a list of dicts
    return grouped.to_dict(orient="records")


def show_plotly_chart():
    """
    Retains your Plotly code for local viewing if you still want to
    run `bargraph.py` directly via `python bargraph.py`.
    """
    coverage_data = generate_requirement_coverage()  # get the data
    import pandas as pd
    import plotly.graph_objects as go

    df_grouped = pd.DataFrame(coverage_data)
    # We assume the DataFrame has columns: [major, short_requirement, NumCourses]
    # Next, replicate your figure logic:
    majors = sorted(df_grouped["major"].dropna().unique())

    def get_trace(selected_major):
        data = df_grouped[df_grouped["major"] == selected_major].copy()
        data = data.sort_values(by="NumCourses", ascending=True)
        return go.Bar(
            x=data["NumCourses"],
            y=data["short_requirement"],
            orientation="h",
            name=selected_major,
        )

    init_major = majors[0]
    init_trace = get_trace(init_major)
    fig = go.Figure(data=[init_trace])

    # Create dropdown
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


def main():
    """
    Entry point if running `bargraph.py` directly. Calls `show_plotly_chart()`.
    """
    show_plotly_chart()


if __name__ == "__main__":
    main()
