"""MySQL IO Manager for the ETL pipeline."""
import os
from typing import Any, Dict, Optional

import mysql.connector
import pandas as pd
from dagster import IOManager, InputContext, OutputContext, ConfigurableIOManager


class MySQLIOManager(ConfigurableIOManager):
    """IO Manager for MySQL database."""

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
    ):
        self.host = host or os.getenv("MYSQL_HOST", "localhost")
        self.port = port or int(os.getenv("MYSQL_PORT", "3306"))
        self.user = user or os.getenv("MYSQL_USER", "root")
        self.password = password or os.getenv("MYSQL_PASSWORD", "")
        self.database = database or os.getenv("MYSQL_DATABASE", "youtube_data")

    def _get_connection(self):
        """Get a MySQL connection."""
        return mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
        )

    def handle_output(self, context: OutputContext, obj: Any) -> None:
        """Handle output to MySQL."""
        # This IO manager is read-only, so we don't implement writing to MySQL
        raise NotImplementedError("Writing to MySQL is not supported")

    def load_input(self, context: InputContext) -> pd.DataFrame:
        """Load data from MySQL."""
        table_name = context.asset_key.path[-1]
        
        # If the asset key has a region prefix, extract it
        if len(context.asset_key.path) > 1:
            region = context.asset_key.path[0]
            table_name = f"{region}_{table_name}"
        
        query = context.metadata.get("query", f"SELECT * FROM {table_name}")
        
        conn = self._get_connection()
        try:
            df = pd.read_sql(query, conn)
            context.log.info(f"Loaded {len(df)} rows from MySQL table {table_name}")
            return df
        finally:
            conn.close()