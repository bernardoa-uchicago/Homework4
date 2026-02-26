import streamlit as st
import altair as alt
from utils.io import load_data
from charts.charts import (
    base_theme,
    Q_1,
    Q_2,
    Q_3
)

st.set_page_config(page_title="Story", layout="wide")

alt.themes.register("project", base_theme)
alt.themes.enable("project")

df, ref_df, team_df = load_data()

st.title("A Data Story: The Effects Referees have on Team Performance")
st.markdown("**Central question:** *Did referee trends reflect on certain team performances over the two seasons?*")

st.header("1) Fouls and Cards per match and referee by season")
st.write("First let's analyse anay unusual patterns for each referee by season")
st.altair_chart(Q_1(df, ref_df), use_container_width=True)
st.caption("Takeaway: Most referees fall in the middle of the distribution with not many fouls or cards." \
"\nOutliers usually come from referees with small number of matches.\n" \
"Referees seem to have little to no influence in the overall outcome of the season, but important matches could be impacted by harsher referees.")

st.header("2) Goal Differences per match")
st.write("Next, we explore how evenly matched teams are by comparing overall goal differences trends.")
st.altair_chart(Q_2(df), use_container_width=True)
st.caption("Takeaway: Most teams seem to be evenly matched with a mean distribution around 0,\n" \
"there are some outliers but those represent when the lower and upper teams in the league compete.")

st.header("3) Points difference per team across seasons")
st.write("Finally we compare changes in team placements across seasons.")
st.altair_chart(Q_3(team_df), use_container_width=True)
st.caption("Takeaway: Some teams really improved and others stayed near their previous placement.\n"
"With the information about referees and goal differences alone we cannot pinpoint an specific reason for team placement movement across season.")