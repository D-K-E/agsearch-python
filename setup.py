# setup py for agsearch
import os
import setuptools


with open("README.md", "r", encoding="utf-8") as f:
    long_desc = f.read()

with open("LICENSE", "r", encoding="utf-8") as f:
    license_str = f.read()

setuptools.setup(
    name="agsearch",
    version="0.1.0",
    author="Qm Auber",
    python_requires=">=3.6.0",
    descriptions="command line search engine for ancient greek",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    license=license_str,
    url="https://gitlab.com/QmAuber/agsearch-python",
    test_suite="tests",
    install_requires=["numpy", "cltk", "scikit-learn"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
