from datetime import date, timedelta
import altair as alt
import pandas as pd
import streamlit as st

import api

def view_merged_prs_by_user(context):
    st.header("View merged PRs")

    username = st.text_input("Username (can be blank)")

    now = date.today()
    from_date = st.date_input("From date", now - timedelta(days=30))
    to_date = st.date_input("To date", now)

    df = api.get_merged_prs(context, from_date, to_date, user=username)

    # Reduce dataset to send over the wire.
    if df.empty:
        st.write("""
            ---

            _No PRs found on the selected dates_

            ---
        """)
        return

    st.write("### Total PRs:", df.shape[0])

    small_df = pd.DataFrame({'linesTouched': df['linesTouched']})

    st.write('### PRs by size')
    st.write(alt.Chart(small_df)
        .mark_bar()
        .encode(
            x=alt.X('linesTouched:Q', title='Number of lines touched in PR', bin=True),
            y=alt.Y('count()', title='Number of PRs'),
        )
    )

    st.write('### Raw data')
    st.table(df)


def view_open_pull_requests(context):
    df = api.get_open_pull_requests(context)

    st.write("### Total open PRs:", df.shape[0])

    small_df = pd.DataFrame({'linesTouched': df['linesTouched']})

    st.write('### PRs by size')
    st.write(alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X('linesTouched:Q', title='Number of lines touched in PR', bin=True),
            y=alt.Y('count()', title='Number of PRs'),
        )
    )

    st.write('### Raw data')
    st.table(df)
