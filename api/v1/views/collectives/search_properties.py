#!/usr/bin/python3
"""for searching properties by unique id"""

import models
from flask import abort


class SearchP:
    """search class"""

    def get(cls, unique_id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if unique_id is None:
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.unique_id == unique_id):
                return value.owner_id

        return None