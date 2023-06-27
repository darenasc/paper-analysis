from enum import Enum

import pandas as pd
import requests
import plotly.express as px
from semanticscholar import SemanticScholar

SUPPORTED_WEBSITE_URL = [
    "semanticscholar.org",
    "arxiv.org",
    "aclweb.org",
    "acm.org",
    "biorxiv.org",
]

SEARCH_TYPE_ID = {
    "URL": "URL:",
    "DOI": "DOI:",
    "ARXIV": "ARXIV:",
    "MAG": "MAG:",
    "ACL": "ACL:",
    "PMID": "PMID:",
    "PMCID": "PMCID",
}


def get_id_from_url(url: str) -> str:
    """Returns the id of the specified URL.

    Args:
        url (str): The URL to get the id from.

    Returns:
        str: The id of the URL.
    """
    return url.split("/")[-1]


def get_paper_from_id(paper_id: str):
    """Returns the paper with the given id.

    Args:
        paper_id (str): Paper id

    Returns:
        _type_: _description_
    """
    sch = SemanticScholar()
    paper = sch.get_paper(paper_id)
    return paper


def get_references(references: list) -> pd.DataFrame:
    """Returns a list of references.

    Args:
        references (list): List of references.

    Returns:
        list: List of references.
    """
    data = []
    for ref in references:
        if ref["publicationVenue"]:
            if "type" in ref["publicationVenue"]:
                publication_venue_type = ref["publicationVenue"]["type"]
        else:
            publication_venue_type = None
        data.append(
            (
                ref["paperId"],
                ref["title"],
                ref["url"],
                ref["publicationDate"],
                ref["venue"],
                publication_venue_type,
                ref["referenceCount"],
                ref["citationCount"],
            )
        )
    return data


def get_references_df(references: list) -> pd.DataFrame:
    """Returns a dataframe of references.

    Args:
        paper (list): List of references.

    Returns:
        pd.DataFrame: Dataframe of references.
    """
    data = get_references(references)
    df = pd.DataFrame(
        data,
        columns=[
            "paperId",
            "title",
            "url",
            "publicationDate",
            "venue",
            "publication_venue_type",
            "referenceCount",
            "citationCount",
        ],
    )
    df.citationCount = df.citationCount.fillna(0)
    df["binning"] = pd.qcut(df.citationCount, 8, labels=False)
    df["binning"] = df["binning"] + 1
    return df


def generate_url(input_str: str, id_type: str = "URL") -> str:
    """Generate a URL for the given input string.

    Args:
        input_str: The input string.

    Returns:
        str: The generated URL.
    """
    endpoint = "https://api.semanticscholar.org/graph/v1/paper/"
    if id_type == "URL":
        if any([x for x in SUPPORTED_WEBSITE_URL if x in input_str]):
            return endpoint + "URL:" + input_str
    elif id_type in SEARCH_TYPE_ID:
        return endpoint + SEARCH_TYPE_ID[id_type] + input_str

    else:
        print(f"Paper {input_str} not found")


def get_paper_id(paper_url: str, id_type: str) -> str:
    """Returns the paper id.

    Args:
        paper_url (str): url to search in the API.

    Returns:
        str: paperID string.
    """
    s2_url = generate_url(paper_url, id_type)
    response = requests.get(s2_url, timeout=10)
    return response.json()["paperId"]


def plot_references_timeline(df: pd.DataFrame, title: str):
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
        size_max=80,
        color="citationCount",
        # marginal_x="histogram",
        title=title,
        hover_data=["title", "referenceCount", "citationCount"],
        height=int(25 * len(df.venue.unique())),
    )
    fig.update_yaxes(dtick=1, type="category", showgrid=True)
    fig.update_layout(template="plotly_dark")
    return fig
