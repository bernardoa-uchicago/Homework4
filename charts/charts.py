import altair as alt
import pandas as pd

def base_theme():
    return {
        "config": {
            "view": {"stroke": None},
            "axis": {"labelFontSize": 12, "titleFontSize": 14},
            "legend": {"labelFontSize": 12, "titleFontSize": 14},
        }
    }

def Q_1(df: pd.DataFrame, ref_df: pd.DataFrame) -> alt.Chart:
    season_select = alt.selection_point(
        fields=["season"],
        bind=alt.binding_radio(
            options=["23-24", "24-25"],
            name="Season: "
        )
    )

    ref_select = alt.selection_point(
        fields=["Referee"]
    )

    brush = alt.selection_interval()

    ref_chart = (
        alt.Chart(
            ref_df,
            title="Referees Ranked by Cards per Match"
        ).transform_filter(
            season_select
        ).mark_circle(
            size=120
        ).encode(
            x=alt.X("avg_cards:Q", title="Average Cards per Match"),
            y=alt.Y("Referee:N", sort=alt.SortField("avg_cards", order="descending"), title="Referee"),
            opacity=alt.condition(ref_select, alt.value(1), alt.value(0.3)),
            tooltip=[
                "Referee:N",
                alt.Tooltip("avg_fouls:Q"),
                alt.Tooltip("avg_cards:Q"),
                "matches:Q"
            ],
            color=alt.Color("season:N", legend=alt.Legend(title="Season"))
        ).add_params(
            ref_select
        )
    )

    match_chart = (
        alt.Chart(
            df,
            title="Match-Level Cards and Fould Counts Given by each Referee per Match"
        ).transform_filter(
            season_select
        ).mark_circle(
            size=60
        ).encode(
            x=alt.X("total_fouls:Q", title="Fouls in Match"),
            y=alt.Y("total_cards:Q", title="Cards in Match"),
            color="Referee:N",
            opacity=alt.condition(ref_select, alt.value(1), alt.value(0)),
            tooltip=[
                alt.Tooltip("Referee:N"),
                alt.Tooltip("total_fouls:Q"),
                alt.Tooltip("total_cards:Q"),
                alt.Tooltip("season:N")
            ]
        ).add_params(
            brush
        )
    )

    ref_chart = ref_chart.encode(
        color=alt.condition(
            brush,
            alt.value("red"),
            alt.value("blue")
        )
    )

    dashboard = ref_chart | match_chart
    dashboard = dashboard.add_params(season_select)
    dashboard
        
    return (dashboard)

def Q_2(df: pd.DataFrame) -> alt.Chart:
    brush = alt.selection_interval()

    hist = (
        alt.Chart(
            df,
            title='Goal Difference Counts'
        ).mark_bar(
        ).encode(
            x=alt.X("goal_diff:Q", bin=alt.Bin(maxbins=20), title="Goal Difference (Home - Away)"),
            y="count()",
            color=alt.value("red"),
            tooltip=["count()"]
        ).transform_filter(
            brush
        )
    )

    scatter = (
        alt.Chart(
            df,
            title='Home vs. Away Goals'
        ).mark_circle(
            size=100
        ).encode(
            x=alt.X("FTHG:Q", title="Home Goals"),
            y=alt.Y("FTAG:Q", title="Away Goals"),
            color=alt.condition(brush, alt.value("red"), alt.value("blue")),
            tooltip=["HomeTeam:N","AwayTeam:N","FTHG:Q","FTAG:Q","goal_diff:Q","total_goals:Q","season:N"]
        ).add_params(
            brush
        )
    )

    return (scatter | hist)

def Q_3(team_df: pd.DataFrame) -> alt.Chart:
    season_select = alt.selection_point(
    fields=["season"],
    bind=alt.binding_radio(
        options=["23-24", "24-25"],
        name="Season: "
    )
    )

    team_select = alt.selection_point(
        fields=["Team"]
    )

    dot_plot = (
        alt.Chart(
            team_df,
            title="Team Performance by Season"
        ).transform_filter(
            season_select
        ).mark_circle(
            size=120
        ).encode(
            x=alt.X("points:Q", title="Points"),
            y=alt.Y("Team:N",sort=alt.SortField("points", order="descending"),title="Team"),
            color = "season:N",
            opacity=alt.condition(team_select, alt.value(1), alt.value(0.3)),
            tooltip=[
                "Team:N",
                "points:Q",
                "wins:Q",
                "goal_diff:Q",
                "position:Q",
                "season:N"
            ]
        ).add_params(
            season_select, 
            team_select
        )
    )
    return dot_plot
