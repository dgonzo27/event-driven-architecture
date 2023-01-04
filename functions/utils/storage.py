"""azure storage client"""

import os
import tempfile
from typing import Optional

from azure.storage.blob import (
    BlobClient,
    BlobServiceClient,
    ContainerClient,
    ContentSettings,
)


class StorageClient:
    """azure storage client"""

    account_name: str
    connection_string: str

    service_client: BlobServiceClient
    container_client: ContainerClient
    blob_client: BlobClient

    def __init__(self, account_name: str, cnx_str: str):
        self.account_name = account_name
        self.connection_string = cnx_str
        self.service_client = BlobServiceClient.from_connection_string(
            cnx_str
        )
    
    def __repr__(self) -> str:
        return (
            "Azure Storage Client\n"
            f"account name: {self.account_name}\n"
            f"connection string: {self.connection_string[0:3]}****"
        )
    
    def download_file(self, container_name: str, source: str, dest: str) -> bool:
        """download a file to a path on the local filesystem"""
        try:
            if dest.endswith("."):
                dest += "/"
            blob_dest = dest + os.path.basename(source) if dest.endswith("/") else dest

            os.makedirs(os.path.dirname(blob_dest), exist_ok=True)
            blob_client = self.service_client.get_blob_client(
                container=container_name, blob=source
            )

            if not dest.endswith("/"):
                with open(blob_dest, "wb") as file:
                    data = blob_client.download_blob()
                    file.write(data.readall())
                return True
            return False
        except Exception as ex:
            print(f"unexpected exception occurred: {ex}")
            pass
        return False
    
    def upload_file(
        self,
        container_name: str,
        source: str,
        dest: str,
        content_type: Optional[str] = "application/octet-stream",
        overwrite: Optional[bool] = True,
    ) -> bool:
        """upload a single file to a path inside the container"""
        try:
            container_client = self.service_client.get_container_client(
                container=container_name
            )

            with open(source, "rb") as data:
                container_client.upload_blob(
                    name=dest,
                    data=data,
                    overwrite=overwrite,
                    content_settings=ContentSettings(content_type=content_type),
                )
            return True
        except Exception as ex:
            print(f"unexpected exception occurred: {ex}")
            pass
        return False
    
    def copy_file(
        self, container_name: str, source: str, dest_container: str, dest: str
    ) -> bool:
        """copy a file between any location within the same storage account"""
        try:
            # download to tempfile
            temp_file = tempfile.NamedTemporaryFile()
            download_result = self.download_file(
                container_name=container_name,
                source=source,
                dest=temp_file.name,
            )
            if not download_result:
                print(f"unable to download file: {container_name}/{source}")
                temp_file.close()
                return False
            
            # upload tempfile
            upload_result = self.upload_file(
                container_name=dest_container,
                source=temp_file.name,
                dest=dest,
            )
            if not upload_result:
                print(f"unable to upload file: {dest_container}/{dest}")
                temp_file.close()
                return False
            
            # cleanup
            temp_file.close()
            return True
        except Exception as ex:
            print(f"unexpected exception occurred: {ex}")
            try:
                temp_file.close()
            except Exception:
                pass
            pass
        return False
