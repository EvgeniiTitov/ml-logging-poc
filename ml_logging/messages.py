"""
Different types of messages could be used as the streamer and the underlying
connection implementation might upload different messages in different ways.
Uploading a text and 500 Mb model weights is different
"""
import typing as t


class BaseMessage:
    pass


class CloseMessage(BaseMessage):
    """
    Message used to signal a worker to stop
    """

    pass


class BaseLogMessage(BaseMessage):
    """
    Message used to signal a worker to do some task
    """

    def __init__(self, item: t.Any) -> None:
        self._item = item
        self._name = self.__class__.__name__

    def __repr__(self):
        return f"{self._name} - {self._item}"

    @property
    def item(self) -> t.Any:
        return self._item

    def to_dict(self) -> dict:
        return self.__dict__


class LogHyperParamMessage(BaseLogMessage):
    def __init__(self, key: str, value: t.Any):
        self.key = key
        self.value = value
        super().__init__(f"{key} {value}")


class LogImageMessage(BaseLogMessage):
    pass


class LogAssetMessage(BaseLogMessage):
    pass


class LogTextMessage(BaseLogMessage):
    pass


class LogSystemInfoMessage(BaseLogMessage):
    pass


class LogWhateverMessage(BaseLogMessage):
    pass
