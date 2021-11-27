import logging

import sys
from queue import Queue


LOGGER = logging.getLogger(__name__)


class Tee:
    """
    Catches all user generated logs and puts them in the steamer queue to get
    logged to the backend
    TODO: Check if it works with logging
    """

    def __init__(self, stream_queue: Queue, buffer_size: int = 10) -> None:
        self._buffer_size = buffer_size
        self._stream = stream_queue

        self._batch = []
        self.stdout = sys.stdout
        sys.stdout = self

        self._closed = False
        LOGGER.info("Tee initialized")

    def _unload_batch(self) -> None:
        # TODO: Could block indefinitely, use .put_nowait() + while
        self._stream.put(" ".join([str(e) for e in self._batch]))

    def write(self, data) -> None:
        if len(self._batch) < self._buffer_size:
            self._batch.append(data)
        else:
            self._unload_batch()
            self._batch = [data]
        self.stdout.write(data)

    def flush(self) -> None:
        self.stdout.flush()

    def close(self) -> None:
        sys.stdout = self.stdout
        if len(self._batch):
            self._unload_batch()
        self._closed = True
        LOGGER.info("Tee closed")

    def __del__(self) -> None:
        if not self._closed:
            sys.stdout = self.stdout
            if len(self._batch):
                self._unload_batch()
            LOGGER.info("Tee closed")
