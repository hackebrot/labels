import pathlib
import setuptools


def read(*args: str) -> str:
    file_path = pathlib.Path(__file__).parent.joinpath(*args)
    return file_path.read_text("utf-8")


setuptools.setup(
    name="labels",
    version="20.1.0",
    author="Raphael Pierzina",
    author_email="raphael@hackebrot.de",
    maintainer="Raphael Pierzina",
    maintainer_email="raphael@hackebrot.de",
    license="MIT",
    url="https://github.com/hackebrot/labels",
    project_urls={
        "Repository": "https://github.com/hackebrot/labels",
        "Issues": "https://github.com/hackebrot/labels/issues",
    },
    description="CLI app for managing GitHub labels for Python 3.6 and newer. 📝",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=["click", "requests", "pytoml", "attrs"],
    entry_points={"console_scripts": ["labels = labels.cli:labels"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Utilities",
    ],
    keywords=["github", "command-line"],
)
