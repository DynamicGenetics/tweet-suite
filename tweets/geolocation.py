import pandas as pd
import geopandas as gpd
import logging
import os
import numpy as np
from shapely.geometry import Polygon, Point
from itertools import product

HERE = os.path.abspath(os.path.dirname(__file__))

logger = logging.getLogger(__name__)


class MatchPlaces:
    def __init__(self, unmatchedplaces: pd.DataFrame):
        self._matchedplaces = None
        self._unmatchedplaces = unmatchedplaces
        self._la_keys = None

    @property
    def la_keys(self):
        """Return the Local Authorities Keys Dataset"""
        if self._la_keys is None:
            self._la_keys = gpd.read_file(
                os.path.join(HERE, "datasets", "la_keys.geojson")
            )
        return self._la_keys

    @property
    def unmatchedplaces(self):
        """Return the unmatched places from the SQL database"""
        # If geo_objs exists, it means we've already added them
        # If not, we need to run that function before returning.
        if "geo_objs" in self._unmatchedplaces:
            pass
        else:
            self._unmatchedplaces = self._get_polygons(self._unmatchedplaces)

        return self._unmatchedplaces

    def get(self):
        if self._matchedplaces is None:
            self._matchedplaces = self.get_all_matches()
        return self._matchedplaces

    @staticmethod
    def _get_polygons(data: pd.DataFrame) -> pd.DataFrame:
        """Creates a new column in the data with BoundingBoxes encoded as
        tuples of floats (with no repetition). This column is meant
        to ease the processing to match closest local authority.

        Example
        --------
        >>> coords = "[-4.1952232, 51.665338, -4.0863, 51.708405]"
        >>> lcoords = list(coords[1:-1])
        >>> lcoords = coords[1:-1].split(",")
        >>> lcoords
        ['-4.1952232', ' 51.665338', ' -4.0863', ' 51.708405']
        >>> lcoords = list(map(float, lcoords))
        >>> lcoords
        [-4.1952232, 51.665338, -4.0863, 51.708405]
        >>> longs, lats = lcoords[::2], lcoords[1::2]
        >>> from itertools import product
        >>> tuple(product(longs, lats))
        ((-4.1952232, 51.665338), (-4.1952232, 51.708405), (-4.0863, 51.665338), (-4.0863, 51.708405))
        """
        # [long_min, lat_min, long_max, lat_max] ==>
        # ((long_min, lat_min), (long_min, lat_max), (long_max, lat_min), (long_max, lat_max))

        def transform_as_list_of_tuples(coords: str) -> Polygon:
            lcoords = coords[1:-1].split(
                ","
            )  # remove brackets, and then we split on comma
            lcoords = list(map(float, lcoords))
            longs, lats = lcoords[::2], lcoords[1::2]
            coords = list(product(longs, lats))
            # Make sure coords are in the correct order, otherwise poly will be invalid
            geo = Polygon([coords[3], coords[2], coords[0], coords[1]])

            if not geo.is_valid:
                geo = Point(coords[0])
            return geo

        data["geo_objs"] = data["geo_bbox"].apply(transform_as_list_of_tuples)

        return data

    def get_all_matches(self):
        """ Choose LA with highest likelihood. Add LA and LHB to dataset. """

        # Define interim dataframe of data
        data = self.unmatchedplaces

        matchings = data["geo_objs"].apply(lambda c: self.match_local_authority(c))

        # Split values for LA in three cols
        def get_index(object, index):
            try:
                return object[index]
            except TypeError:
                return None

        data["lad19cd"] = matchings.apply(lambda c: get_index(c, 0))
        data["lad19nm"] = matchings.apply(lambda c: get_index(c, 1))
        data["likelihood"] = matchings.apply(lambda c: get_index(c, 2))

        return data

    def match_local_authority(self, geo_obj):

        """Get the Intersection Over Union for the the Local Authorities that
        overlap with the bounding box. Requires 'geometry' col in LA geopandas df.
        Returns df or tuple of local authorities of interest.

        Parameters
        ----------
        polygon: Polygon
            Shapley Polygon object enclosing the tweet bounding box
            
        Returns
        -------
        A tuple containing the name, the code, and the reference of
        the top matching LA, or all of them (in the form of
        a pd.DataFrame)
        """

        # Local Authorities of Interest are those that overlap with the bbox
        laoi = self.la_keys[self.la_keys["geometry"].intersects(geo_obj)].copy()

        if laoi.shape[0] == 0:  # no overlap found
            return None

        # Intersection over the union is a measure of how exactly the bounding box
        # and the la overlap
        laoi["iou"] = self.la_keys["geometry"].apply(
            lambda g: g.intersection(geo_obj).area / g.union(geo_obj).area
        )

        # Pop weight is the proportion of the la population covered by the bounding box.
        laoi["pop_weight"] = (
            laoi["geometry"].apply(lambda g: (g.intersection(geo_obj).area / g.area))
            * laoi["population_count"]
        )
        # The final likelihood is the IoU multiplied by the population weight
        laoi["likelihood"] = laoi["iou"] * laoi["pop_weight"]
        # Sort dataframe by highest to lowest
        laoi = laoi.sort_values(by="likelihood", ascending=False)

        return laoi["lad19cd"].iat[0], laoi["lad19nm"].iat[0], laoi["likelihood"].iat[0]

