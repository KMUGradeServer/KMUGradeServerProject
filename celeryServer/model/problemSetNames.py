    # -*- coding: utf-8 -*-
"""
    문제집 Name에 대한 정보 모듈
"""


from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR

from model import Base 

class ProblemSetNames(Base) :
    
    __tablename__ = 'ProblemSetNames'
    
    problemSetNameIndex = Column(INTEGER(unsigned = True),
                                 primary_key = True, 
                                 autoincrement = True,
                                 nullable = False)
    problemSetName = Column(VARCHAR(255),
                            nullable = False,
                            unique = True) 
