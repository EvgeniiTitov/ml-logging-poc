import logging
import typing as t


from ml_logging.streamer import Streamer
from ml_logging.messages import (
    CloseMessage,
    PostMessage,
    BaseMessage
)


LOGGER = logging.getLogger(__name__)


class BaseRun:

    def __init__(self) -> None:
        self._streamer: t.Optional[Streamer] = None
        self._start()

    def _init_streamer(self, *args, **kwargs) -> None:
        try:
            self._streamer = Streamer(*args, **kwargs)
        except Exception as e:
            LOGGER.exception(f"Failed to init streamer. Error: {e}")
            raise e

    def _start(self) -> None:
        self._init_streamer()

        # TODO: Log general information such as:
        #       a) Environment
        #       b) OS, kernel
        #       c) Config data etc

    def _send_message_to_streamer(self, message: BaseMessage) -> None:
        self._streamer.enqueue_message(message)
        LOGGER.debug(f"Message {message} send to the Streamer")

    def log_text(self, text: str) -> None:
        post = PostMessage()
        post.set_text(text)
        self._send_message_to_streamer(post)

    def log_image(self, image) -> None:
        post = PostMessage()
        post.set_image(image)
        self._send_message_to_streamer(post)

    def log_asset(self, asset) -> None:
        post = PostMessage()
        post.set_asset(asset)
        self._send_message_to_streamer(post)

    def _end(self) -> None:
        self._streamer.enqueue_message(CloseMessage())
