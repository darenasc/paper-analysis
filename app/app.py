import pandas as pd
import plotly.express as px
import streamlit as st

from paper_analysis import semantic_scholar as s2

st.set_page_config(
    page_title="Paper Analysis App",
    layout="wide",
    initial_sidebar_state="expanded",
)

paper_url = st.text_input(
    "Paper URL from SemanticScholar.org",
    "https://www.semanticscholar.org/paper/Mapping-poverty-at-multiple-geographical-scales-Nicolò-Fabrizi/f24dc845602d5b395b3c33697e6edcf29ad5776a",
)
paper_id = s2.get_id_from_url(paper_url)
st.write("The paper id is: ", paper_id)


def plot_references_timeline(df: pd.DataFrame):
    """Returns a plotly chart with the references timeline.

    Args:
        df (pd.DataFrame): data frame with references.

    Returns:
        px.scatter: figure with the references timeline.
    """
    fig = px.scatter(
        df,
        x="publicationDate",
        y="venue",
        # size="citationCount",
        size_max=80,
        color="citationCount",
        # marginal_x="histogram",
        title=f"Paper: {paper.title} ({paper.year})",
        hover_data=["title", "referenceCount", "citationCount"],
        height=int(25 * len(df.venue.unique())),
    )
    fig.update_yaxes(dtick=1, type="category", showgrid=True)
    fig.update_layout(template="plotly_dark")
    return fig


if paper_id:
    paper = s2.get_paper_from_id(paper_id=paper_id)
    df_references = s2.get_references_df(paper.references)
    fig = plot_references_timeline(df_references)
    # st.plotly_chart(fig)
    st.plotly_chart(fig, use_container_width=True, theme=None)
