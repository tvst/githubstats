import streamlit as st
import pages

"""
# Github stats viewer
"""

token = st.sidebar.text_input("Github token").strip()

show_help = len(token) == 0

if show_help:
    """
    To get started, create a [personal access token for Github](https://github.com/settings/tokens)
    and paste it in the sidebar on the left 👈.

    _Note: this app doesn't need any special permissions, so no need to check those boxes when
    creating a token! The only exception is if you want to get stats for a private repo, of course._
    """

else:
    repo_path = st.sidebar.text_input("Repo", "streamlit/streamlit")

    st.sidebar.markdown("---")

    options = {
        "View open pull requests": pages.view_open_pull_requests,
        "View merged PRs by user": pages.view_merged_prs_by_user,
    }
    page_key = st.sidebar.radio("What do you want to do?", list(options.keys()))
    page = options[page_key]

    repo_parts = repo_path.split("/")

    context = {
        "repo_path": repo_path,
        "repo_owner": repo_parts[0],
        "repo_name": repo_parts[1],
        "token": "token " + token
    }

    page(context)
