# Paper Analysis App (PAApp)

Test the app in [paper-viz.streamlit.app](https://paper-viz.streamlit.app).

## How to use it
1. Paste the url of a paper or DOI or valid ID in the search bar
2. Check out the timeline of the references in the paper

## Install it locally

```
git clone https://github.com/darenasc/paper-analysis.git
cd paper-analysis
pipenv install -e .
pipenv run streamlit run app/app.py
```

## APIs
Using the following APIs and libraries:
- [Semantic Scholar](https://www.semanticscholar.org) as API for papers.
- [semanticscholar](https://github.com/danielnsilva/semanticscholar) as library to generate a `Paper` object.
- [streamlit](streamlit.io) to plot the timeline with the references of the paper.  

Pending to add:
- [DataCite API](https://support.datacite.org/docs/api)
- [arXiv API](https://info.arxiv.org/help/api/index.html)
- [CrossRef API](https://api.crossref.org/swagger-ui/index.html)

## ToDo

- Extract paper data:
    - [x] Authors
    - [x] Organizations
    - [x] Dates
    - [x] Venues
- [x] Timeline
- [ ] Graph
- [ ] Map
