#!/usr/bin/python3
"""owner object"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv
from hashlib import md5


class Owner(BaseModel, Base):
    """Representation of owner model"""
    __tablename__ = 'owners'
    firstname = Column(String(128), nullable=False)
    lastname = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    gender = Column(String(10), nullable=True)
    phone_no = Column(String(20), nullable=False)
    properties = relationship("Property",
                              backref="owner",
                              cascade="all, delete, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """hash the password with md5 for security"""
        if name == 'password':
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)

    @property
    def properties(self):
        """
        getter method to get the list of 
        property instance for an owner
        """
        from models.property import Property
        propert_list = []
        all_properties = models.storage.all(Property)
        for property in all_properties.values():
            if property.owner_id == self.id:
                propert_list.append(property)
        return propert_list
