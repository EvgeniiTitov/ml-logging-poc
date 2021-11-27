import os
import typing as t
import platform


def get_machine_details() -> t.MutableMapping[str, str]:
    # TODO: Add a bunch of useful information here
    info = {
        "os_name": os.name,
        "platform": platform.system(),
        "release": platform.release(),
        "architecture": platform.architecture(),
        "cpu_count": os.cpu_count()
    }
    return info
