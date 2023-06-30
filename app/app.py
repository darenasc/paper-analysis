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

    authors, tltr, fields_of_study = st.columns(3)

    with authors:
        st.markdown(
            "<h3 style='text-align: center;'>Authors</h3>", unsafe_allow_html=True
        )
        for author in paper.authors:
            st.markdown(
                f"[{author['name']}]({author['url']}) (papers: {author['paperCount']}, citations: {author['citationCount']}, hIndex: {author['hIndex']})"
            )

    with tltr:
        st.markdown(
            "<h3 style='text-align: center;'>tl;dr</h3>", unsafe_allow_html=True
        )
        st.markdown(
            f"<p style='text-align: center;'>{paper.tldr}</p>", unsafe_allow_html=True
        )
        with st.expander("See abstract"):
            st.markdown(
                f"<p style='text-align: center;'><b>{paper.abstract}</p>",
                unsafe_allow_html=True,
            )

    with fields_of_study:
        st.markdown(
            "<h3 style='text-align: center;'>Fields of study</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<p style='text-align: center;'>{s2.get_fields_of_study(paper)}</p>",
            unsafe_allow_html=True,
        )

    df_references = s2.get_references_df(paper.references)
    title = f"Paper: {paper.title} ({paper.year})"
    fig = s2.plot_references_timeline(df_references, title)
    st.plotly_chart(fig, use_container_width=True, theme=None)
