from setuptools import setup, find_packages

setup(
    name="vulnhunter",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "vulnhunter=vulnhunter.main:main"
        ]
    }
)