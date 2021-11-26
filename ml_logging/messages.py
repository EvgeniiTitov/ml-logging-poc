
"""
Different types of messages could be used as the streamer and the underlying
connection implementation might upload different messages in different ways.
Uploading a text and 500 Mb model weights is different
"""
class BaseMessage:

    def __init__(self):
        self._text = None
        self._image = None
        self._asset = None
        self._kernel = None
        self._environment = None

    def set_text(self, text: str) -> None:
        self._text = text

    def set_image(self, image: str) -> None:
        self._image = image

    def set_asset(self, asset: str) -> None:
        self._asset = asset

    def set_kernel(self, info: str) -> None:
        self._kernel = info

    def set_environment(self, environment: str) -> None:
        self._environment = environment

    def to_dict(self) -> dict:
        return self.__dict__


class CloseMessage(BaseMessage):
    pass


class PostMessage(BaseMessage):

    def __init__(self) -> None:
        super().__init__()

    def __repr__(self):
        return f"PostMessage: {self.to_dict()}"


class GetMessage(BaseMessage):

    def __init__(self):
        super(GetMessage, self).__init__()

    def __repr__(self):
        return f"GetMessage: {self.to_dict()}"


class ListMessage(BaseMessage):

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f"ListMessage: {self.to_dict()}"
