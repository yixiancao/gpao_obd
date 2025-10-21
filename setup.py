from pathlib import Path
from setuptools import setup, find_packages

readme_path = Path(__file__).with_name("README.md")
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="gpao_obd",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Generate templates and finding charts from astronomical data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests", "notebooks")),
    include_package_data=True,
    package_data={
        "gpao_obd": ["template.obd"],
    },
    install_requires=[
        "astropy",
        "numpy",
        "matplotlib",
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)