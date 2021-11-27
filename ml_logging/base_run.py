import logging
import typing as t
import uuid

from ml_logging.streamer import Streamer
import ml_logging.messages as messaging
from ml_logging.tee import Tee
from ml_logging.utils import get_machine_details


LOGGER = logging.getLogger(__name__)


class BaseRun:
    def __init__(self, auto_logging: bool) -> None:
        self._run_id = self._generate_run_id()
        self._streamer: t.Optional[Streamer] = None
        self._start()

        if auto_logging:
            self._logging_tee = Tee(self._streamer.queue)
        else:
            self._logging_tee = None

    @property
    def run_id(self) -> str:
        return self._run_id

    def _init_streamer(self, *args, **kwargs) -> None:
        try:
            self._streamer = Streamer(self._run_id, *args, **kwargs)
            self._streamer.start()
        except Exception as e:
            LOGGER.exception(f"Failed to init streamer. Error: {e}")
            raise e

    def _start(self) -> None:
        self._init_streamer()

        # TODO: Parse config determining how our Run objects works (auto
        #       logging, etc)

        # TODO: Log general information such as:
        #       a) Environment
        #       b) OS, kernel
        #       c) Config data etc
        #       d) Installed packages
        self._log_system_details()
        self._log_config()
        LOGGER.info("General information logged")

    def complete_experiment(self) -> None:
        self._end()
        LOGGER.info("Close message sent to the streamer")

    def _send_message_to_streamer(
        self, message: messaging.BaseLogMessage
    ) -> None:
        self._streamer.enqueue_message(message)
        LOGGER.debug(f"Message {message} send to the Streamer")

    def log_hyper_param(self, key: str, value: t.Any) -> None:
        self._send_message_to_streamer(
            messaging.LogHyperParamMessage(key, value)
        )

    def log_image(self, image) -> None:
        self._send_message_to_streamer(messaging.LogImageMessage(image))

    def log_asset(self, asset) -> None:
        self._send_message_to_streamer(messaging.LogAssetMessage(asset))

    def _log_system_details(self) -> None:
        self._send_message_to_streamer(
            messaging.LogTextMessage(str(get_machine_details()))
        )

    def _log_config(self) -> None:
        pass

    def _generate_run_id(self) -> str:
        return str(uuid.uuid4())

    def _end(self) -> None:
        # TODO: How to determine session end?
        if self._logging_tee:
            self._logging_tee.close()
        self._streamer.enqueue_message(messaging.CloseMessage())
