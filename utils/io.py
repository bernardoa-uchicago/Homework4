import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_data() -> pd.DataFrame:
    df_2324 = pd.read_csv('../Data/PL-season-2324.csv')
    df_2425 = pd.read_csv('../Data/PL-season-2425.csv')
    df_2324["total_fouls"] = df_2324["HF"] + df_2324["AF"]
    df_2324["total_cards"] = df_2324["HY"] + df_2324["AY"] + df_2324["HR"] + df_2324["AR"]
    df_2324["season"] = "23-24"
    df_2425["season"] = "24-25"

    ref_2324 = (
        df_2324
        .groupby("Referee")
        .agg(
            avg_fouls=("total_fouls", "mean"),
            avg_cards=("total_cards", "mean"),
            matches=("Referee", "count")
        )
        .reset_index()
    )

    ref_2324["season"] = "23-24"
    df_2425["total_fouls"] = df_2425["HF"] + df_2425["AF"]
    df_2425["total_cards"] = df_2425["HY"] + df_2425["AY"] + df_2425["HR"] + df_2425["AR"]
    ref_2425 = (
        df_2425
        .groupby("Referee")
        .agg(
            avg_fouls=("total_fouls", "mean"),
            avg_cards=("total_cards", "mean"),
            matches=("Referee", "count")
        )
        .reset_index()
    )

    ref_2425["season"] = "24-25"

    ref_df = pd.concat([ref_2324, ref_2425], ignore_index=True)
    print(ref_df.columns)
    df = pd.concat([df_2324, df_2425], ignore_index=True)

    df["goal_diff"] = df["FTHG"] - df["FTAG"]
    df["total_goals"] = df["FTHG"] + df["FTAG"]

    df["home_goal_diff"] = df["FTHG"] - df["FTAG"]
    df["away_goal_diff"] = df["FTAG"] - df["FTHG"]

    df["home_points"] = np.where(df["FTHG"] > df["FTAG"], 3, np.where(df["FTHG"] == df["FTAG"], 1, 0))

    df["away_points"] = np.where(df["FTAG"] > df["FTHG"], 3, np.where(df["FTAG"] == df["FTHG"], 1, 0))

    df["home_win"] = (df["FTHG"] > df["FTAG"]).astype(int)
    df["away_win"] = (df["FTAG"] > df["FTHG"]).astype(int)

    home_df = df[[
        "season",
        "HomeTeam",
        "FTHG",
        "FTAG",
        "home_points",
        "home_win",
        "home_goal_diff"
    ]].copy()

    home_df.columns = [
        "season",
        "Team",
        "goals_for",
        "goals_against",
        "points",
        "win",
        "goal_diff"
    ]

    away_df = df[[
        "season",
        "AwayTeam",
        "FTHG",
        "FTAG",
        "away_points",
        "away_win",
        "away_goal_diff"
    ]].copy()

    away_df.columns = [
        "season",
        "Team",
        "goals_for",
        "goals_against",
        "points",
        "win",
        "goal_diff"
    ]

    long_df = pd.concat([home_df, away_df], ignore_index=True)

    team_df = (
        long_df
        .groupby(["season", "Team"])
        .agg(
            points=("points", "sum"),
            wins=("win", "sum"),
            goal_diff=("goal_diff", "sum"),
            goals_for=("goals_for", "sum"),
            goals_against=("goals_against", "sum"),
            matches=("points", "count")
        )
        .reset_index()
    )

    team_df["position"] = (
        team_df
        .groupby("season")["points"]
        .rank(method="dense", ascending=False)
    )

    return df, ref_df, team_df
