import logging
import threading
from queue import Queue
import typing as t

from ml_logging.messages import BaseMessage, CloseMessage
from ml_logging.connection import GCSBackend


LOGGER = logging.getLogger(__name__)


class Streamer(threading.Thread):
    """
    If given run id, must be able to connect to an existing run
    Else, a new one must be created
    """

    MESSAGE_QUEUE_SIZE = 100

    def __init__(self, run_id: t.Any, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._message_queue = Queue(Streamer.MESSAGE_QUEUE_SIZE)
        self._backend = GCSBackend(run_id)
        LOGGER.info("Streamer initialized")

    def enqueue_message(self, message: BaseMessage) -> None:
        self._message_queue.put(message)

    def run(self) -> None:
        while True:
            message = self._message_queue.get()
            if isinstance(message, CloseMessage):
                LOGGER.debug("CloseMessage received, stopping")
                break

            # TODO: Process the message received
