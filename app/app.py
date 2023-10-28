import numpy as np
import streamlit as st

from paper_analysis import semantic_scholar as s2

if "_id" not in st.session_state:
    st.session_state["_id"] = 0

if "widget_id" not in st.session_state:
    st.session_state["widget_id"] = (id for id in range(1, 100_00))

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


input_str = st.text_input("Search", "")


def function_to_display(url: str, id_type: str):
    """Function to display GUI items.

    Args:
        url (str): String the user input.
        id_type (str): Where to search for the paper.
    """
    paper_id = s2.get_paper_id(url, id_type)
    paper = s2.get_paper_from_id(paper_id)

    st.markdown(
        f"<h1 style='text-align: center;'>{paper.title} ({paper.year})</h1>",
        unsafe_allow_html=True,
    )

    authors, tltr, fields_of_study = st.columns(3)

    # Increment the session states
    st.session_state["_id"] += len(paper.references) + 1

    # First column with authors
    with authors:
        st.markdown(
            "<h3 style='text-align: center;'>Authors</h3>", unsafe_allow_html=True
        )
        for author in paper.authors:
            st.markdown(
                f"[{author['name']}]({author['url']}) (papers: {author['paperCount']}, citations: {author['citationCount']}, hIndex: {author['hIndex']})"
            )

    # Second column with summary and abstract
    with tltr:
        if paper.tldr:
            st.markdown(
                "<h3 style='text-align: center;'>tl;dr</h3>", unsafe_allow_html=True
            )
            st.markdown(
                f"<p style='text-align: center;'>{paper.tldr}</p>",
                unsafe_allow_html=True,
            )
        if paper.abstract:
            with st.expander("See abstract"):
                st.markdown(
                    f"<p style='text-align: center;'><b>{paper.abstract}</p>",
                    unsafe_allow_html=True,
                )

    # Third column with fielf of study
    with fields_of_study:
        fos = s2.get_fields_of_study(paper)
        if fos:
            st.markdown(
                "<h3 style='text-align: center;'>Fields of study</h3>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p style='text-align: center;'>{s2.get_fields_of_study(paper)}</p>",
                unsafe_allow_html=True,
            )
            st.divider()
        if paper.citationCount:
            st.markdown(
                f"<h3 style='text-align: center;'>{paper.citationCount:,} citations</h3>",
                unsafe_allow_html=True,
            )

    df_references = s2.get_references_df(paper.references)
    if paper.referenceCount:
        title = f"This paper has {paper.referenceCount:,} references"
    else:
        title = f"{paper.title}"

    # Chart with timeline of references and number of citations
    fig = s2.plot_references_timeline(df_references, title)
    st.plotly_chart(fig, use_container_width=True, theme=None)

    # References
    colms = st.columns((2, 1, 1, 2, 2, 1, 1))
    fields = [
        "title",
        "year",
        "citations",
        "venue",
        "authors",
        "download",
        "visualize paper",
    ]

    # header columns
    for col, field_name in zip(colms, fields):
        col.write(field_name)

    df_for_markdown = s2.get_df_for_markdown(paper)
    for i, r in df_for_markdown.iterrows():
        col1, col2, col3, col4, col5, col6, col7 = st.columns((2, 1, 1, 2, 2, 1, 1))
        col1.write(df_for_markdown["title"][i])
        col2.write(
            f'{int(df_for_markdown["year"][i]) if not np.isnan(df_for_markdown["year"][i]) else ""}'
        )
        col3.write(
            f'{(int(df_for_markdown["citations"][i]) if not np.isnan(df_for_markdown["citations"][i]) else "")}'
        )
        col4.write(df_for_markdown["venue"][i])
        col5.write(df_for_markdown["authors"][i])
        col6.write(df_for_markdown["download"][i])
        if df_for_markdown["url"][i] is not None:
            button_phold = col7.empty()
            _ = button_phold.button(
                "Visualize paper",
                key=next(st.session_state["widget_id"]),
                on_click=function_to_display,
                args=[df_for_markdown["url"][i], "URL"],
            )
    st.divider()


if input_str != "":
    function_to_display(input_str, id_type)
