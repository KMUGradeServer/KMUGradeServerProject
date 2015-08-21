# -*- coding: utf-8 -*-
"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    어플리케이션을 사용할 사용자 Organizations정보

"""


from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, ENUM

from model import Base
from resource.enumResources import ENUMResources

class Organizations(Base) :
    
    __tablename__ ='Organizations'
    
    organizationIndex = Column(INTEGER(unsigned = True), 
                               primary_key = True, 
                               autoincrement = True, 
                               nullable = False)
    organizationCode = Column(VARCHAR(255),
                              nullable = True,
                              unique = True)
    organizationName = Column(VARCHAR(255), 
                              nullable = False,
                              unique = True)
    isAbolished = Column(ENUM(ENUMResources().const.TRUE,
                              ENUMResources().const.FALSE),
                         default = ENUMResources().const.FALSE,
                         nullable = False)
    
