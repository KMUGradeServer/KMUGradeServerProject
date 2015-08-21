# -*- coding: utf-8 -*-
"""

    어플리케이션을 사용할 Team 정보

"""


from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, TEXT, ENUM

from model import Base
from model.registeredCourses import RegisteredCourses
from resource.enumResources import ENUMResources

class Teams(Base) :
    
    __tablename__ = 'Teams'
    
    teamIndex = Column(INTEGER(unsigned = True),
                       primary_key = True,
                       autoincrement = True,
                       nullable = False)
    courseIndex = Column(INTEGER(unsigned = True),
                         ForeignKey(RegisteredCourses.courseIndex,
                                    onupdate = 'CASCADE',
                                    ondelete = 'CASCADE'),
                         nullable = False)
    teamName = Column(VARCHAR (255),
                      nullable =False,
                      unique = True)
    teamDescription = Column(TEXT,
                             nullable = True)
    teamMemberCount = Column(INTEGER(unsigned = True),
                             default =1,
                             nullable = False)
    isDeleted = Column(ENUM(ENUMResources().const.TRUE,
                            ENUMResources().const.FALSE),
                       default = ENUMResources().const.FALSE,
                       nullable = False)
    
