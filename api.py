import streamlit as st
import pandas as pd
import requests


# Helpful link to Github Graphiql URL:
# https://developer.github.com/v4/explorer/


def union(dict1, dict2):
    return dict(list(dict1.items()) + list(dict2.items()))


def run_query(context, query):
    headers = {"Authorization": context['token']}

    request = requests.post(
        'https://api.github.com/graphql',
        json={'query': query},
        headers=headers
    )

    if request.status_code == 200:
        response = request.json()
        try:
            return response["data"]
        except Exception as e:
            raise Exception("{}\n {}".format(str(e), query))

    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


@st.cache(ttl=30, show_spinner=False)
def get_open_pull_requests(context, max=50):
    variables = union(context, {
        "max": max
    })

    query = """
    {
        repository(owner: "%(repo_owner)s", name: "%(repo_name)s") {
            pullRequests(states: [OPEN], last: 100) {
                nodes {
                    permalink
                    title
                    additions
                    deletions
                    reviewRequests(last:100) {
                        nodes {
                            requestedReviewer {
                                ... on User {
                                    login
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    """ % variables

    resp = run_query(context, query)
    df = pd.DataFrame(resp["repository"]["pullRequests"]["nodes"])

    if not df.empty:
        df["linesTouched"] = df["deletions"] + df["additions"]

    return df


@st.cache(ttl=30, show_spinner=False)
def get_merged_prs(context, from_date, to_date, user=None):
    if user:
        user_query = f"author:{user}"
    else:
        user_query = ""

    variables = union(context, {
        "user_query": user_query,
        "from_date_str": from_date.isoformat(),
        "to_date_str": to_date.isoformat(),
    })

    query = '''
    {
        search(
            type: ISSUE,
            query: """
                repo:%(repo_path)s
                %(user_query)s
                is:pr
                state:closed
                closed:%(from_date_str)s..%(to_date_str)s
            """,
            last: 100
        ) {
           nodes {
                ... on PullRequest {
                    permalink
                    title
                    merged
                    mergedAt
                    additions
                    deletions
                }
            }
        }
    }
    ''' % variables

    resp = run_query(context, query)
    df = pd.DataFrame(resp["search"]["nodes"])

    if not df.empty:
        df["linesTouched"] = df["deletions"] + df["additions"]

    return df
