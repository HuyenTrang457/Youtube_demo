"""PostgreSQL IO Manager for the ETL pipeline."""
import os
from typing import Any, Dict, Optional

import pandas as pd
import sqlalchemy as sa
from dagster import IOManager, InputContext, OutputContext, ConfigurableIOManager


class PostgreSQLIOManager(ConfigurableIOManager):
    """IO Manager for PostgreSQL database."""

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        schema: Optional[str] = None,
    ):
        self.host = host or os.getenv("POSTGRES_HOST", "localhost")
        self.port = port or int(os.getenv("POSTGRES_PORT", "5432"))
        self.user = user or os.getenv("POSTGRES_USER", "postgres")
        self.password = password or os.getenv("POSTGRES_PASSWORD", "postgres")
        self.database = database or os.getenv("POSTGRES_DB", "youtube_analytics")
        self.schema = schema or "public"

    def _get_engine(self):
        """Get a SQLAlchemy engine."""
        return sa.create_engine(
            f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        )

    def handle_output(self, context: OutputContext, obj: Any) -> None:
        """Handle output to PostgreSQL."""
        if not isinstance(obj, pd.DataFrame):
            raise TypeError(f"Expected pandas DataFrame, got {type(obj)}")

        table_name = context.asset_key.path[-1]
        schema = context.metadata.get("schema", self.schema)
        
        # Get write mode (default to replace)
        if_exists = context.metadata.get("if_exists", "replace")
        
        engine = self._get_engine()
        
        # Write DataFrame to PostgreSQL
        obj.to_sql(
            name=table_name,
            con=engine,
            schema=schema,
            if_exists=if_exists,
            index=False,
            method="multi",
            chunksize=1000,
        )
        
        context.log.info(f"Wrote {len(obj)} rows to PostgreSQL table {schema}.{table_name}")

    def load_input(self, context: InputContext) -> pd.DataFrame:
        """Load data from PostgreSQL."""
        table_name = context.asset_key.path[-1]
        schema = context.metadata.get("schema", self.schema)
        
        query = context.metadata.get("query", f"SELECT * FROM {schema}.{table_name}")
        
        engine = self._get_engine()
        df = pd.read_sql(query, engine)
        
        context.log.info(f"Loaded {len(df)} rows from PostgreSQL table {schema}.{table_name}")
        return df