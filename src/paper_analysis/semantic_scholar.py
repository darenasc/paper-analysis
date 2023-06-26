import pandas as pd
from semanticscholar import SemanticScholar


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
            if ref["publicationVenue"]["type"]:
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
