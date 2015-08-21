# -*- coding: utf-8 -*-
"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    어플리케이션을 사용할 사용자 정보

"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import DATETIME, VARCHAR, INTEGER, TEXT, SET, ENUM

from model import Base
from model.membersId import MembersId
from model.organizations import Organizations

from resource.setResources import SETResources
from resource.enumResources import ENUMResources

class Members (Base) :
    
    __tablename__ ='Members'
    
    memberIdIndex = Column(INTEGER(unsigned = True),
                           ForeignKey(MembersId.memberIdIndex,
                                      onupdate = 'CASCADE',
                                      ondelete = 'CASCADE'),
                           primary_key =True,
                           autoincrement = False,
                           nullable =False)
    organizationIndex = Column(INTEGER(unsigned = True),
                               ForeignKey(Organizations.organizationIndex,
                                          onupdate = 'CASCADE',
                                          ondelete = 'CASCADE'),
                               primary_key = True,
                               autoincrement = False,
                               nullable = False)
    password = Column(VARCHAR(1024),
                      nullable =False)
    memberName = Column(VARCHAR(1024),
                        nullable =False)
    contactNumber = Column(VARCHAR(20),
                           nullable =True)
    emailAddress = Column(VARCHAR(1024),
                          nullable =True)
    detailInformation = Column(VARCHAR(1024),
                               nullable = True)
    authority = Column(SET(SETResources().const.SERVER_ADMINISTRATOR,
                           SETResources().const.FREE_ADMINISTRATOR,
                           SETResources().const.ADMINISTRATOR,
                           SETResources().const.USER),
                       default = SETResources().const.USER,
                       nullable = False)
    limitedCourses = Column(INTEGER(unsigned = True),
                            default = None,
                            nullable = True)
    limitedUseDate = Column(DATETIME,
                            default = None,
                            nullable = True)
    signedInDate = Column(DATETIME,
                          nullable = False)
    lastAccessDate = Column(DATETIME,
                            nullable =True)
    comment = Column(TEXT,
                     nullable = True)   
    isDeleted = Column(ENUM(ENUMResources().const.TRUE, 
                            ENUMResources().const.FALSE),
                       default = ENUMResources().const.FALSE,
                       nullable = False)
