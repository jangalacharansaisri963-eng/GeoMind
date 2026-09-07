from setuptools import setup, find_packages

setup(
    name="geomind-ai",
    version="0.1.0",
    description="An intelligent Python-based AI focused on Geography, History, and Social Studies.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "cli": ["rich>=12.0.0"],
        "research": ["playwright>=1.40.0"],
        "test": ["pytest>=7.0.0"]
    },
    entry_points={
        "console_scripts": [
            "geomind = geomind.cli:main"
        ]
    }
)
