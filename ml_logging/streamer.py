import logging
import threading
from queue import Queue

import ml_logging.messages as messaging
from ml_logging.connection import GCSBackend


LOGGER = logging.getLogger(__name__)


# TODO: Think about queue size to the streamer. If for some reason it fails to
#       push messages to the back end, the queue fills up -> user code hangs


class Streamer(threading.Thread):
    """
    Receives messages (wrappers on top of objects a user wants to log) from
    the BaseRun object, depending on the object's nature, the appropriate
    backend handle or whatever is used to upload the item
    """

    MESSAGE_QUEUE_SIZE = 100

    def __init__(self, run_id: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._message_queue: "Queue[messaging.BaseMessage]" = Queue(
            Streamer.MESSAGE_QUEUE_SIZE
        )
        self._backend = GCSBackend(run_id)
        LOGGER.info("Streamer initialized")

    @property
    def queue(self) -> Queue:
        return self._message_queue

    def enqueue_message(self, message: messaging.BaseMessage) -> None:
        # TODO: Blocking operation -> dangerous
        self._message_queue.put(message)

    def run(self) -> None:
        while True:
            message = self._message_queue.get()

            if isinstance(message, messaging.CloseMessage):
                LOGGER.debug("CloseMessage received")
                # TODO: There might be pending messages in the queue
                break

            if isinstance(message, messaging.LogImageMessage):
                self._backend.upload_image(message.item)
            elif isinstance(message, messaging.LogAssetMessage):
                self._backend.upload_asset(message.item)
            elif isinstance(message, messaging.LogHyperParamMessage):
                self._backend.upload_hyper_parameter(
                    message.key, message.value
                )
            elif isinstance(message, messaging.LogTextMessage):
                self._backend.upload_text(message.item)

        LOGGER.info("Streamer stopped")
