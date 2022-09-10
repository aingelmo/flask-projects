"""Sample callback Dash app"""
import dash_table as dt
import pandas as pd
import pandas_gbq
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output
from google.oauth2 import service_account
from website.dash_apps import create_dash_app

# endpoint of this page
URL_RULE = "/bq-test"
# dash internal route prefix, must be start and end with "/"
URL_BASE_PATHNAME = "/dash/bq-test-app/"

credentials = service_account.Credentials.from_service_account_file(
    "/home/andres/projects/web/flask-projects/wherever-it-takes/bq-private-key.json"
)

queries = {
    "top_types": "SELECT type, COUNT(*) count FROM hacker_news_copy.full_201510 GROUP BY 1 ORDER BY 2 LIMIT 100",
    "counts": """
        SELECT a.month month, stories, comments, comment_authors, story_authors
        FROM (
            SELECT FORMAT_TIMESTAMP('%Y-%m', time_ts) month, COUNT(*) stories, COUNT(DISTINCT author) story_authors
            FROM hacker_news_copy.stories
            GROUP BY 1
        ) a
        JOIN (
            SELECT FORMAT_TIMESTAMP('%Y-%m', time_ts) month, COUNT(*) comments, COUNT(DISTINCT author) comment_authors
            FROM hacker_news_copy.comments
            GROUP BY 1
        ) b
        ON a.month=b.month
        ORDER BY 1
    """,
}


def create_dash(server):
    """Create a Dash view"""
    app = create_dash_app(server, URL_RULE, URL_BASE_PATHNAME)

    dfs = {}
    for query_name in queries:
        df = pd.read_gbq(
            queries[query_name], project_id="frogfit-data-prod", credentials=credentials
        )
        dfs[query_name] = df

    table_label = html.Label("Hacker News BigQuery Public Dataset")
    table = dt.DataTable(
        id="top_types-table",
        columns=[{"name": i, "id": i} for i in dfs["top_types"].columns],
        data=dfs["top_types"].to_dict("records"),
        style_cell={"textAlign": "left"},
        style_data={"whiteSpace": "normal", "height": "auto"},
        fill_width=False,
    )

    df = dfs["counts"].copy(deep=True)
    df.set_index("month", inplace=True)
    df = df.unstack().reset_index()
    df.columns = ["category", "month", "value"]
    fig = px.bar(
        df,
        x="category",
        y="value",
        color="category",
        animation_frame="month",
        range_y=[0, df["value"].max() * 1.1],
        title="Hacker News interactions over time, animated",
    )
    histogram = dcc.Graph(id="counts-histogram", figure=fig)

    fig = go.Figure()
    for category in ["stories", "comments", "comment_authors", "story_authors"]:
        fig.add_trace(
            go.Scatter(
                x=dfs["counts"]["month"],
                y=dfs["counts"][category],
                mode="lines+markers",
                name=category,
            )
        )
    fig.update_layout(title="Hacker News interactions over time")
    line = dcc.Graph(id="counts-line", figure=fig)

    app.layout = html.Div([table_label, table, histogram, line])

    return app.server
