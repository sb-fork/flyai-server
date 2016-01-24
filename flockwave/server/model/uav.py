"""Model classes related to a single UAV."""

from __future__ import absolute_import

from datetime import datetime
from flockwave.spec.schema import get_complex_object_schema
from pytz import utc
from .metamagic import ModelMeta
from .vectors import GPSCoordinate


__all__ = ("UAVStatusInfo", )


class UAVStatusInfo(object):
    """Class representing the status information available about a single
    UAV.
    """

    __metaclass__ = ModelMeta

    class __meta__:
        schema = get_complex_object_schema("uavStatusInfo")

    def __init__(self, id=None, timestamp=None):
        """Constructor.

        Parameters:
            id (str or None): ID of the UAV
            timestamp (datetime or None): time when the status information
                was received. ``None`` means to use the current date and
                time.
        """
        self.id = id
        self.position = GPSCoordinate()
        self.update_timestamp(timestamp)

    def update_timestamp(self, timestamp=None):
        """Updates the timestamp of the UAV status information.

        Parameters:
            timestamp (datetime or None): the new timestamp; ``None`` means
            to use the current date and time.
        """
        if timestamp is None:
            # datetime.utcnow() is not okay here because it returns a
            # datetime object with tzinfo set to None. As a consequence,
            # isoformat() will not add the timezone information correctly
            # when the datetime object is formatted into JSON
            timestamp = utc.localize(datetime.now())
        assert timestamp.tzinfo is not None, \
            "UAV status information timestamp must be timezone-aware"
        self.timestamp = timestamp
