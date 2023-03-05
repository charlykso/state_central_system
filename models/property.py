#!/usr/bin/python3
"""Property object"""

import models
from models.base_model import BaseModel, Base
from models.owner import Owner
from sqlalchemy import Column, String, ForeignKey


class Property(BaseModel, Base):
    """representing the property model"""
    __tablename__ = "properties"
    type = Column(String(20), nullable=False)
    description = Column(String(255), nullable=False)
    owner_id = Column(String(60), ForeignKey('owners.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes a property"""
        super().__init__(*args, **kwargs)
        