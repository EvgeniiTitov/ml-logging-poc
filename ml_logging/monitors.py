import logging
import threading
import time
from queue import Queue
import typing as t

import psutil

from ml_logging.messages import LogSystemInfoMessage


LOGGER = logging.getLogger(__name__)


class CPUMonitor(threading.Thread):

    def __init__(
            self,
            event: threading.Event,
            message_queue: Queue,
            interval: float,
            *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self._event = event
        self._interval = interval
        self._queue = message_queue
        LOGGER.info("CPUMonitor initialized")

    def run(self) -> None:
        while not self._event.is_set():
            time.sleep(self._interval)
            stats = self.collect_system_info()
            # Blocking call -> dangerous
            self._queue.put(
                LogSystemInfoMessage(item=str(stats))
            )

    def collect_system_info(self) -> t.MutableMapping[str, t.Any]:
        # TODO: Think what info is useful
        ram = (
                int(psutil.virtual_memory().total -
                    psutil.virtual_memory().available) / 1024 / 1024
        )
        stats = {
            "percent": psutil.cpu_percent(),
            "ram": ram,
        }
        return stats


class GPUMonitor(threading.Thread):
    # TODO: Think about the package to use for that

    def __init__(
            self,
            event: threading.Event,
            message_queue: Queue,
            interval: float,
            *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self._event = event
        self._interval = interval
        self._queue = message_queue
        LOGGER.info("GPUMonitor initialized")

    def run(self) -> None:
        pass

    def collect_gpu_info(self) -> t.Any:
        pass


if __name__ == '__main__':
    queue = Queue(5)
    event = threading.Event()
    cpu_monitor_thread = CPUMonitor(event, queue, 1.0)
    cpu_monitor_thread.start()

    for i in range(10):
        print("\nGot stats:", queue.get())

    event.set()
    cpu_monitor_thread.join()
    print("Done")
