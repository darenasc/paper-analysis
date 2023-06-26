from setuptools import setup, find_packages

setup(
    name="paper-analysis",
    version="0.0.1",
    description="App to analyze publications",
    url="https://github.com/darenasc/paper-analysis",
    author="Diego Arenas",
    author_email="darenasc@gmail.com",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
