import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tweet-suite",
    version="0.1.0",
    author="Nina Di Cara, Alastair Tanner, Valerio Maggio",
    author_email="ninadicara@protonmail.com",
    description="Collect and save daily Twitter data from Wales using Twitter's Academic API.",
    long_description=long_description,
    url="https://github.com/ninadicara/tweet-suite",
    project_urls={"Bug Tracker": "https://github.com/ninadicara/tweet-suite/issues",},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "tweet-suite"},
    packages=setuptools.find_packages(where="tweet-suite"),
    python_requires=">=3.6",
    install_requires=[
        "retry",
        "os",
        "logging",
        "itertools",
        "geopandas",
        "sqlite3",
        "json",
        "vaderSentiment",
        "schedule",
        "pandas",
        "shapley",
        "datetime",
        "requests",
        "re",
    ],
)
