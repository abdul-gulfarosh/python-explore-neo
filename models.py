"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional),
    diameter in kilometers (optional - sometimes unknown), and whether it's
    marked as potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the
        constructor.
        """
        self.designation = str(info.get('designation'))
        self.hazardous = bool(info.get('hazardous'))
        self.name = str(info.get('name')) if info.get('name') != '' else None
        if info.get('diameter') != '':
            self.diameter = float(info.get('diameter'))
        else:
            self.diameter = float('nan')

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name is not None:
            return f"{self.designation} ({self.name})"

        return self.designation

    def __str__(self):
        """Return `str(self)`."""
        is_hazardous = "is" if self.hazardous else "is not"
        return f"NEO {self.fullname} has a diameter of " \
            f"{self.diameter:.3f} km and {is_hazardous} potentially hazardous."

    def __repr__(self):
        """Return `repr(self)`."""
        return f"NearEarthObject(designation={self.designation!r}, " \
            f"name={self.name!r}, diameter={self.diameter:.3f},  " \
               f"hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach
    to Earth, such as the date and time (in UTC) of closest approach,
    the nominal approach distance in astronomical units, and the relative
    approach velocity in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the
        constructor.
        """
        self._designation = str(info.get('designation'))
        self.time = cd_to_datetime(info.get('time'))
        self.distance = float(info.get('distance'))
        self.velocity = float(info.get('velocity'))

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default
        representation includes seconds - significant figures that don't exist
        in our input data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return f"At {self.time_str}, '{self.neo.fullname}' " \
            f"approaches Earth at a distance of {self.distance:.2f} au " \
            f"and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`."""
        return f"CloseApproach(time={self.time_str!r}, " \
               f"distance={self.distance:.2f}, " \
            f"velocity={self.velocity:.2f}, neo={self.neo!r})"
