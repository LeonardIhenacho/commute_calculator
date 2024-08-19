from setuptools import setup, find_packages

setup(
    name="commute_calculator",
    version="0.2.0",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "pydantic",
    ],
    entry_points={
        'console_scripts': [
            'commute-calculator=main:run_cli',  # Correctly reference the main module
        ],
    },
)
