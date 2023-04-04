"""Types specific to the local positioning system support extension."""

from abc import ABCMeta, abstractmethod, abstractproperty
from blinker import Signal
from typing import (
    Any,
    ClassVar,
    Dict,
    Generic,
    TypeVar,
)

from flockwave.server.model.object import ModelObject

__all__ = ("LocalPositioningSystem", "LocalPositioningSystemType")


class LocalPositioningSystem(ModelObject):
    """Representation of a single local positioning system (LPS) on the server.

    A local positioning system consists of a _type_, an associated
    _configuration_, and a set of base stations that provide position information
    to objects using the services of the local positioning system.
    """

    _id: str = ""
    """The unique identifier of the LPS."""

    type: str = ""
    """The type of the LPS. Must be one of the identifiers from the LPS type
    registry.
    """

    on_updated: ClassVar[Signal] = Signal(
        doc="Signal that is emitted when the state of the local positioning "
        "system changes in any way that clients might be interested in."
    )

    @property
    def device_tree_node(self) -> None:
        return None

    @property
    def id(self) -> str:
        return self._id

    @property
    def json(self) -> Dict[str, Any]:
        """Returns the JSON representation of the local positioning system."""
        return {
            "id": self.id,
            "type": self.type,
        }

    def notify_updated(self) -> None:
        """Notifies all subscribers to the `on_updated()` event that the state
        of the local positioning system was updated.
        """
        self.on_updated.send(self)


T = TypeVar("T", bound=LocalPositioningSystem)
"""Type variable representing a subclass of LocalPositioningSystem_ that a given
LocalPositioningSystemType_ creates when asked to create a new instance.
"""


class LocalPositioningSystemType(Generic[T], metaclass=ABCMeta):
    """Base class for local positioning system (LPS) types.

    New LPS types in the Skybrush server may be implemented by deriving a class
    from this base class and then registering it in the LPS type registry.
    """

    @abstractproperty
    def description(self) -> str:
        """A longer, human-readable description of the LPS type that can be
        used by clients for presentation purposes.
        """
        raise NotImplementedError

    @abstractproperty
    def name(self) -> str:
        """A human-readable name of the LPS type that can be used by
        clients for presentation purposes.
        """
        raise NotImplementedError

    @abstractmethod
    def create(self) -> T:
        """Creates a new instance with a default parameter set.

        Returns:
            a new LPS instance
        """
        raise NotImplementedError

    @abstractmethod
    def get_configuration_schema(self) -> Dict[str, Any]:
        """Returns the JSON schema associated with general configuration
        parameters of instances of this LPS type.

        If you do not intend to use a schema, simply return an empty dictionary.
        Note that an empty dictionary is not a valid JSON schema; if you want to
        declare that you need no parameters, return ``{ "type": "object" }``
        instead.

        Returns:
            JSON schema of general LPS configuration parameters
        """
        raise NotImplementedError
