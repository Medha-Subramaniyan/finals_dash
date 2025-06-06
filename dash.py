{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "3e9e63bc-af99-4acb-ac4b-fb8f0abe56bc",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "from sqlalchemy import create_engine\n",
    "import plotly.express as px\n",
    "import time\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "9685bf09-230b-41a9-aa05-c03133d5089c",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2025-06-05 20:21:59.199 \n",
      "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
      "  command:\n",
      "\n",
      "    streamlit run /opt/anaconda3/lib/python3.12/site-packages/ipykernel_launcher.py [ARGUMENTS]\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "DeltaGenerator()"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "\n",
    "# === CONFIG ===\n",
    "DATABASE_URL = 'postgresql://postgres:password@localhost:5432/dash'\n",
    "engine = create_engine(DATABASE_URL)\n",
    "\n",
    "# === STREAMLIT SETUP ===\n",
    "st.set_page_config(page_title=\"NBA Finals Dashboard\", layout=\"wide\")\n",
    "st.title(\"🏀 NBA Finals 2025 – Live Game 1 Dashboard\")\n",
    "\n",
    "# === AUTO-REFRESH EVERY 60 SECONDS ===\n",
    "st_autorefresh = st.experimental_rerun if st.button(\"🔁 Manual Refresh\") else None\n",
    "time.sleep(60)\n",
    "\n",
    "# === PLAYER STATS ===\n",
    "player_df = pd.read_sql(\"\"\"\n",
    "    SELECT * FROM player_stats\n",
    "    WHERE pts IS NOT NULL\n",
    "    ORDER BY time_collected DESC\n",
    "    LIMIT 100\n",
    "\"\"\", engine)\n",
    "\n",
    "# === TEAM STATS ===\n",
    "team_df = pd.read_sql(\"\"\"\n",
    "    SELECT * FROM team_stats\n",
    "    ORDER BY time_collected DESC\n",
    "    LIMIT 2\n",
    "\"\"\", engine)\n",
    "\n",
    "# === PLAY-BY-PLAY ===\n",
    "pbp_df = pd.read_sql(\"\"\"\n",
    "    SELECT * FROM play_by_play\n",
    "    ORDER BY time_collected DESC, event_num DESC\n",
    "    LIMIT 20\n",
    "\"\"\", engine)\n",
    "\n",
    "# === CHARTS ===\n",
    "col1, col2 = st.columns(2)\n",
    "\n",
    "with col1:\n",
    "    st.subheader(\"Top Scorers\")\n",
    "    fig = px.bar(player_df.sort_values(by=\"pts\", ascending=False).head(10),\n",
    "                 x=\"player_name\", y=\"pts\", title=\"Top Scoring Players\")\n",
    "    st.plotly_chart(fig)\n",
    "\n",
    "with col2:\n",
    "    st.subheader(\"Team Points Breakdown\")\n",
    "    fig2 = px.pie(team_df, names=\"team_name\", values=\"points\", title=\"Team Score Share\")\n",
    "    st.plotly_chart(fig2)\n",
    "\n",
    "# === STATS TABLE ===\n",
    "st.subheader(\"Live Player Stats\")\n",
    "st.dataframe(player_df[['player_name', 'team_id', 'min', 'pts', 'reb', 'ast', 'fg_pct', 'usg_pct']])\n",
    "\n",
    "# === PLAY-BY-PLAY ===\n",
    "st.subheader(\"Latest Play-by-Play Events\")\n",
    "st.dataframe(pbp_df[['period', 'clock', 'home_desc', 'visitor_desc']])\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "50614015-4d52-4228-b35a-eceaed1a0c37",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
