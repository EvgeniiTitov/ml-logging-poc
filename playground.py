import sys
import threading
from queue import Queue
import time

import comet_ml


class Streamer(threading.Thread):

    def __init__(self, stream: Queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._steam_queue = stream
        self.file = open("text.txt", "w")

    def run(self) -> None:
        while True:
            payload = self._steam_queue.get()
            if "STOP" in payload:
                break

            self.file.write(payload)
            self.file.flush()
        self.file.close()


class Tee:
    BATCH_SIZE = 10

    def __init__(self, stream_queue: Queue):
        self.stream = stream_queue
        self.batch = []
        self.stdout = sys.stdout
        sys.stdout = self

    def _unload_batch(self):
        self.stream.put(" ".join([str(e) for e in self.batch]))

    def write(self, data):
        if len(self.batch) < Tee.BATCH_SIZE:
            self.batch.append(data)
        else:
            self._unload_batch()
            self.batch = [data]
        self.stdout.write(data)

    def flush(self):
        self.stdout.flush()

    # def close(self):
    #     sys.stdout = self.stdout
    #     if len(self.batch):
    #         self._unload_batch()

    def __del__(self):
        sys.stdout = self.stdout
        if len(self.batch):
            self._unload_batch()


def train_model():
    print("Started to train the model")
    for i in range(10):
        print("Epoch:", i)
    print("Model trained!")


def main():
    stream_queue = Queue(100)
    streamer = Streamer(stream_queue)
    streamer.start()

    t = Tee(stream_queue)
    train_model()

    stream_queue.put("STOP")
    streamer.join()
    print("Done")


if __name__ == '__main__':
    main()
