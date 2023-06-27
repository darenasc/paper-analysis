import plotly.express as px
import streamlit as st

from paper_analysis import semantic_scholar as s2


st.set_page_config(
    page_title="Paper Analysis App",
    layout="wide",
    page_icon=":coffee:",
    initial_sidebar_state="expanded",
)

id_type = st.radio(
    "Search by",
    ([x for x in s2.SEARCH_TYPE_ID]),
    horizontal=True,
    key="URL",
)
if id_type == "URL":
    st.write(
        "Valid URLs from: arxiv.org, aclweb.org, acm.org, biorxiv.org, or SemanticScholar.org"
    )
input_str = st.text_input(
    "Search",
)

if input_str:
    paper_id = s2.get_paper_id(input_str, id_type)
    paper = s2.get_paper_from_id(paper_id)
    df_references = s2.get_references_df(paper.references)
    title = f"Paper: {paper.title} ({paper.year})"
    fig = s2.plot_references_timeline(df_references, title)
    st.plotly_chart(fig, use_container_width=True, theme=None)
