from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declared_attr
from __init__ import db

##TODO add medicine selection and storage when selecting treatments (Not implemented)
class Treatment(db.Model, Base):
	lotNo = Column(String)
	expiration = Column(DateTime)
	withdrawal = Column(Integer)
	dosage = Column(Integer)
	unit = Column(String)