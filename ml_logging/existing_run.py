import logging
import typing as t
import os

from ml_logging.connection import GCSBackend
from ml_logging.exceptions import RunDoesntExist

LOGGER = logging.getLogger(__name__)


class ExistingRun:

    def __init__(self, run_id: str) -> None:
        self._run_id = run_id
        self._backend = GCSBackend(run_id)

        # if not self._backend.run_exists:
        #     raise RunDoesntExist("There is no run with such run_id")
        # else:
        #     LOGGER.info("Detected run with provided ID")
        LOGGER.info("ExistingRun initialized")

    def list_assets(self) -> t.Sequence[t.Any]:
        return self._backend.list_assets()

    def list_images(self) -> t.Sequence[t.Any]:
        return self._backend.list_images()

    def get_hyper_params(self) -> t.Any:
        pass

    def get_asset(
            self, name: str, dest_folder: t.Optional[str] = None
    ) -> t.Tuple[bool, t.Optional[str]]:
        destination_folder = dest_folder if dest_folder else os.getcwd()
        return self._backend.download_asset(
            name, os.path.join(destination_folder, name)
        )

    def get_image(
            self, name: str, dest_folder: t.Optional[str] = None
    ) -> t.Tuple[bool, t.Optional[str]]:
        destination_folder = dest_folder if dest_folder else os.getcwd()
        return self._backend.download_image(
            name, os.path.join(destination_folder, name)
        )
