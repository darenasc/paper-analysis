import pandas as pd
import plotly.express as px
import requests
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
                ref["influentialCitationCount"],
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
            "influentialCitationCount",
        ],
    )
    df.citationCount = df.citationCount.fillna(0)
    df.influentialCitationCount = df.influentialCitationCount.fillna(0)

    # Resizing for the scatter plot
    a, b = 12, 1000
    x, y = df.influentialCitationCount.min(), df.influentialCitationCount.max()
    df["influential_size"] = (df.influentialCitationCount - x) / (y - x) * (b - a) + a

    x, y = df.citationCount.min(), df.citationCount.max()
    df["citation_size"] = (df.citationCount - x) / (y - x) * (b - a) + a

    # min_size, max_size = 12, 1000
    # x, y = df.influentialCitationCount.min(), df.influentialCitationCount.max()
    # df["size"] = (df.influentialCitationCount - x) / (y - x) * (
    #     max_size - min_size
    # ) + min_size
    # x, y = df.citationCount.min(), df.citationCount.max()
    # df["size"] = (df.citationCount - x) / (y - x) * (max_size - min_size) + min_size

    # Sorting the dataframe by number of publications in venues
    df["total_citation_count"] = df.groupby(["venue"], as_index=False)[
        "citationCount"
    ].transform(sum)
    df = df.sort_values(by="total_citation_count").reset_index(drop=True)
    df = df.drop(columns=["total_citation_count"])
    return df


def generate_url(input_str: str, id_type: str = "URL") -> str:
    """Generate a URL for the given input string.

    Args:
        input_str: The input string.
        id_type (str): Options are "URL", "DOI", "ARXIV", "MAG", "ACL", "PMID", "PMCID".

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
        id_type (str): Options are "URL", "DOI", "ARXIV", "MAG", "ACL", "PMID", "PMCID".

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
    # 450 is the default value
    suggested_height = (
        25 * len(df.venue.unique()) + 300
        if int(25 * len(df.venue.unique())) + 300 > 450
        else 450
    )
    fig = px.scatter(
        df,
        x="publicationDate",
        y="venue",
        size="citation_size",
        size_max=70,
        color="citationCount",
        marginal_x="histogram",
        title=title,
        hover_data={"citationCount": True, "citation_size": False},
        hover_name="title",
        height=suggested_height,
    )
    fig.layout.yaxis.type = "category"
    fig.update_yaxes(showgrid=True)
    fig.update_layout(template="plotly_dark")

    fig.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        args=[{"marker.size": [df["citation_size"]]}],
                        label="Citations",
                        method="update",
                    ),
                    dict(
                        args=[{"marker.size": [df["influential_size"]]}],
                        label="Influence",
                        method="update",
                    ),
                ]
            )
        ]
    )
    return fig


def get_fields_of_study(paper: "Paper") -> str:
    """Returns a string with the fields of study.

    Args:
        paper (Paper): paper object to get fields of study.

    Returns:
        str: Fields of study.
    """
    fields_of_study = ""
    if paper["fieldsOfStudy"]:
        fields_of_study += ", ".join([x for x in paper.fieldsOfStudy])
    return fields_of_study


####### Functions to generate table of references #######
def get_publication_venue_name(publicationVenue):
    text = ""
    name = ""
    if publicationVenue:
        if "name" in publicationVenue:
            name += publicationVenue["name"]
        if "url" in publicationVenue:
            text += f'[{name}]({publicationVenue["url"]})'
        else:
            text = name

    return text


def get_authors(reference_authors: dict, paper_authors: list):
    author_list = []
    paper_authors = [author["authorId"] for author in paper_authors]
    for reference_author in reference_authors:
        if reference_author["authorId"] in paper_authors:
            author_list.append(f'**{reference_author["name"]}**')
        else:
            author_list.append(reference_author["name"])
    return ", ".join(author for author in author_list)


def get_open_access_url(openAccessPdf):
    if openAccessPdf:
        return f'[download]({openAccessPdf["url"]})'
    else:
        return ""


def format_citation_count(citationCount):
    if citationCount > 0:
        return f"{int(citationCount):,}"
    else:
        return None


def generate_ref_table(paper):
    markdown_text = """| title | venue | authors | download | citations |\n"""
    markdown_text += """| --- | --- | --- | --- | --- |\n"""
    for ref in paper.references:
        markdown_text += f'| [{ref["title"]} ({ref["year"]})]({ref["url"]}) | {get_publication_venue_name(ref["publicationVenue"])} | {get_authors(ref["authors"], paper["authors"])} | {get_open_access_url(ref["openAccessPdf"])} | {format_citation_count(ref["citationCount"])} |\n'
    return markdown_text


def get_df_for_markdown(paper):
    data = []
    for ref in paper.references:
        data.append(
            (
                ref["title"],
                ref["year"],
                ref["url"],
                get_publication_venue_name(ref["publicationVenue"]),
                get_authors(ref["authors"], paper["authors"]),
                get_open_access_url(ref["openAccessPdf"]),
                ref["citationCount"],
            )
        )

    df_table = pd.DataFrame(
        data,
        columns=["title", "year", "url", "venue", "authors", "download", "citations"],
    )
    df_table = df_table.sort_values(by="citations", ascending=False)
    df_table = df_table.reset_index()
    return df_table


def get_markdown_table(paper):
    data = []
    for ref in paper.references:
        data.append(
            (
                ref["title"],
                ref["year"],
                ref["url"],
                get_publication_venue_name(ref["publicationVenue"]),
                get_authors(ref["authors"], paper["authors"]),
                get_open_access_url(ref["openAccessPdf"]),
                ref["citationCount"],
            )
        )

    df_table = pd.DataFrame(
        data,
        columns=["title", "year", "url", "venue", "authors", "download", "citations"],
    )

    markdown = """| title | venue | authors | download | citations |\n"""
    markdown += """| --- | --- | --- | --- | --- |\n"""
    for i, r in df_table.sort_values(by="citations", ascending=False).iterrows():
        markdown += f'| [{r["title"]} ({r["year"]})]({r["url"]}) | {r["venue"]} | {r["authors"]} | {r["download"]} | {format_citation_count(r["citations"])} |\n'
    return markdown


####### End of functions to generate table of references #######
