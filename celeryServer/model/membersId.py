# -*- coding: utf-8 -*-
"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    어플리케이션을 사용할 사용자 ID정보

"""


from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER

from model import Base

class MembersId(Base) :
    
    __tablename__ ='MembersId'
    
    memberIdIndex = Column(INTEGER(unsigned = True), 
                           primary_key = True, 
                           autoincrement = True, 
                           nullable = False)
    memberId = Column(VARCHAR(20), 
                      nullable = False, 
                      unique = True)
