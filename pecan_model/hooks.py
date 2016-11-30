from pecan import hooks

from pecan_model.db import api


class DBHook(hooks.PecanHook):
    """Create a db connection instance."""

    def before(self, state):
        state.request.db_conn = api.Connection()
