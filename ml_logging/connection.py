'''
FAKE BACKEND FOR NOW ABSTRACTED AWAY WITH GCS
'''

import os
import logging
import typing as t
import uuid

from google.cloud import storage


LOGGER = logging.getLogger(__name__)


class GCSBackend:
    ROOT_BUCKET = "ml-logging-poc-etitov"

    def __init__(self, run_folder_name: str) -> None:
        self._storage_client = storage.Client()
        self._root_bucket = self._storage_client.bucket(GCSBackend.ROOT_BUCKET)
        LOGGER.info("Storage client and root bucket initialized")

        self._run_folder_name = run_folder_name
        folder_exists = self._does_run_level_folder_exist(run_folder_name)
        if folder_exists:
            LOGGER.info("Folder exists -> running experiment")
        else:
            LOGGER.info("Folder doest exist -> new experiment")

    def upload_asset(
            self,
            asset_path: str,
            dest_name: t.Optional[str] = None
    ) -> None:
        self._check_file_exists_locally(asset_path)
        destination_path = os.path.join(
            self._run_folder_name,
            "assets",
            dest_name if dest_name else os.path.basename(asset_path)
        )
        self._upload_from_filename(destination_path, asset_path)
        LOGGER.info(f"Asset {asset_path} uploaded")

    def upload_image(
            self,
            image_path: str,
            dest_name: t.Optional[str] = None
    ) -> None:
        self._check_file_exists_locally(image_path)
        destination_name = os.path.join(
            self._run_folder_name,
            "images",
            dest_name if dest_name else os.path.basename(image_path)
        )
        self._upload_from_filename(destination_name, image_path)
        LOGGER.info(f"Image {image_path} uploaded")

    def upload_hyper_parameter(self, key: str, value: t.Any) -> None:
        destination_name = os.path.join(
            self._run_folder_name,
            "hyperparameters",
            f"{uuid.uuid4()}.txt"
        )
        self._upload_from_string(destination_name, f"{key} {str(value)}")
        LOGGER.info("KV uploaded")

    def list_assets(self) -> t.List[str]:
        blobs = self._list_blobs(os.path.join(self._run_folder_name, "assets"))
        return [os.path.basename(blob) for blob in blobs]

    def list_images(self) -> t.List[str]:
        blobs = self._list_blobs(os.path.join(self._run_folder_name, "images"))
        return [os.path.basename(blob) for blob in blobs]

    def download_asset(self, asset_name: str, destination_path: str):
        full_asset_path = os.path.join(
            self._run_folder_name, "assets", asset_name
        )
        self._download_locally(full_asset_path, destination_path)

    def download_image(self, image_name: str, destination_path: str) -> t.Any:
        full_image_path = os.path.join(
            self._run_folder_name, "images", image_name
        )
        self._download_locally(full_image_path, destination_path)

    def download_hyper_parameters(self):
        # TODO: Download all files locally, open, concat contents. WTF!
        pass

    def _does_run_level_folder_exist(self, folder_name: str) -> bool:
        return storage.Blob(
            name=folder_name, bucket=self._root_bucket
        ).exists(self._storage_client)

    def _check_file_exists_locally(self, filename: str) -> None:
        if not os.path.exists(filename):
            raise FileNotFoundError(
                f"Failed to locate {filename} locally, cant upload"
            )

    def _upload_from_filename(
            self, destination_path: str, filepath: str
    ) -> None:
        blob = self._root_bucket.blob(destination_path)
        blob.upload_from_filename(filepath)

    def _upload_from_string(self, destination_path: str, text: str) -> None:
        blob: storage.Blob = self._root_bucket.blob(destination_path)
        blob.upload_from_string(text)

    def _list_blobs(self, prefix: str) -> t.List[str]:
        blobs = self._storage_client.list_blobs(
            bucket_or_name=GCSBackend.ROOT_BUCKET, prefix=prefix
        )
        return [blob.name for blob in blobs]

    def _download_locally(self, gcs_source: str, destination: str) -> None:
        try:
            blob = self._root_bucket.blob(gcs_source)
            blob.download_to_filename(destination)
        except Exception as e:
            LOGGER.exception(
                f"Failed to download file {gcs_source}. Error: {e}"
            )
            raise e
