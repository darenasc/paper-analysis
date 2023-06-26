from semanticscholar import SemanticScholar


def get_paper(paper_id: str):
    """Returns the paper with the given id.

    Args:
        paper_id (str): Paper id

    Returns:
        _type_: _description_
    """
    sch = SemanticScholar()
    paper = sch.get_paper(paper_id)
    return paper


def get_references(references: list) -> list:
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
