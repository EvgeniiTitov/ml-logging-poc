import logging

from ml_logging.base_run import BaseRun


LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class NewRun(BaseRun):
    pass


class ExistingRun(BaseRun):

    # TODO: Existing run has pull functionality
    pass
