from setuptools import find_packages, setup

setup(
    name="etl_pipeline",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "dagster",
        "dagster-webserver",
        "dagster-postgres",
        "dagster-aws",
        "dagster-dbt",
        "dagster-pandas",
        "dagster-pyspark",
        "mysql-connector-python",
        "psycopg2-binary",
        "sqlalchemy",
        "minio",
        "pandas",
        "pyarrow",
        "pyspark",
        "python-dotenv",
        "pyyaml",
    ],
    extras_require={
        "dev": ["pytest"],
    },
)