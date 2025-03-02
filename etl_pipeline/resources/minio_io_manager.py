"""MinIO IO Manager for the ETL pipeline."""
import os
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from dagster import IOManager, InputContext, OutputContext, ConfigurableIOManager
from minio import Minio


class MinIOIOManager(ConfigurableIOManager):
    """IO Manager for MinIO storage."""

    def __init__(
        self,
        endpoint: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        secure: Optional[bool] = None,
        region: Optional[str] = None,
    ):
        self.endpoint = endpoint or os.getenv("MINIO_ENDPOINT", "localhost:9000")
        self.access_key = access_key or os.getenv("MINIO_ACCESS_KEY", "minioadmin")
        self.secret_key = secret_key or os.getenv("MINIO_SECRET_KEY", "minioadmin")
        self.secure = secure if secure is not None else os.getenv("MINIO_SECURE", "False").lower() == "true"
        self.region = region

    def _get_client(self) -> Minio:
        """Get a MinIO client."""
        return Minio(
            self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=self.secure,
            region=self.region,
        )

    def _ensure_bucket_exists(self, client: Minio, bucket: str) -> None:
        """Ensure the bucket exists."""
        if not client.bucket_exists(bucket):
            client.make_bucket(bucket)

    def handle_output(self, context: OutputContext, obj: Any) -> None:
        """Handle output to MinIO."""
        if not isinstance(obj, pd.DataFrame):
            raise TypeError(f"Expected pandas DataFrame, got {type(obj)}")

        # Extract metadata from context
        layer = context.metadata.get("layer", "bronze")
        bucket = context.metadata.get("bucket", layer)
        format_type = context.metadata.get("format", "parquet")
        
        # Build the object path
        asset_path = "/".join(context.asset_key.path)
        
        # Add partitioning if specified
        partitioning = context.metadata.get("partitioning", [])
        partition_path = ""
        
        if partitioning and isinstance(obj, pd.DataFrame):
            for partition in partitioning:
                if partition in obj.columns:
                    # Use the first value for partitioning (assuming batch processing by partition)
                    partition_value = str(obj[partition].iloc[0])
                    partition_path += f"{partition}={partition_value}/"
        
        # Combine paths
        object_path = f"{asset_path}/{partition_path}"
        if not object_path.endswith(".parquet") and format_type == "parquet":
            object_path += "data.parquet"
        
        # Convert DataFrame to bytes
        client = self._get_client()
        self._ensure_bucket_exists(client, bucket)
        
        if format_type == "parquet":
            # Convert to PyArrow Table and then to Parquet
            table = pa.Table.from_pandas(obj)
            
            # Write to a temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=".parquet") as temp_file:
                pq.write_table(table, temp_file.name)
                
                # Upload the file
                client.fput_object(
                    bucket_name=bucket,
                    object_name=object_path,
                    file_path=temp_file.name,
                    content_type="application/octet-stream",
                )
        elif format_type == "csv":
            # Convert to CSV
            csv_bytes = obj.to_csv(index=False).encode("utf-8")
            
            # Upload the CSV data
            import io
            client.put_object(
                bucket_name=bucket,
                object_name=object_path if object_path.endswith(".csv") else f"{object_path}.csv",
                data=io.BytesIO(csv_bytes),
                length=len(csv_bytes),
                content_type="text/csv",
            )
        else:
            raise ValueError(f"Unsupported format type: {format_type}")
        
        context.log.info(f"Wrote {len(obj)} rows to MinIO: {bucket}/{object_path}")

    def load_input(self, context: InputContext) -> pd.DataFrame:
        """Load data from MinIO."""
        # Extract metadata from context
        layer = context.metadata.get("layer", "bronze")
        bucket = context.metadata.get("bucket", layer)
        format_type = context.metadata.get("format", "parquet")
        
        # Build the object path
        asset_path = "/".join(context.asset_key.path)
        object_path = context.metadata.get("object_path", asset_path)
        
        if not object_path.endswith(f".{format_type}"):
            object_path = f"{object_path}.{format_type}"
        
        client = self._get_client()
        
        # Download the object to a temporary file
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=f".{format_type}") as temp_file:
            client.fget_object(bucket, object_path, temp_file.name)
            
            # Read the data based on format
            if format_type == "parquet":
                df = pd.read_parquet(temp_file.name)
            elif format_type == "csv":
                df = pd.read_csv(temp_file.name)
            else:
                raise ValueError(f"Unsupported format type: {format_type}")
        
        context.log.info(f"Loaded {len(df)} rows from MinIO: {bucket}/{object_path}")
        return df