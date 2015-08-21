# -*- coding: utf-8 -*-
"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    등록된 과목의 정보
"""


from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import DATETIME, VARCHAR, INTEGER, TEXT, ENUM

from model import Base
from model.members import Members

from resource.enumResources import ENUMResources

class RegisteredCourses(Base) :
    
    __tablename__ = 'RegisteredCourses'
    
    courseIndex = Column(INTEGER(unsigned = True), 
                         primary_key = True, 
                         autoincrement = True,
                         nullable = False)
    # yyyy.organization.ID.index
    courseCode = Column(VARCHAR(255), 
                        nullable = False,
                        unique = True)
    courseName = Column(VARCHAR(1024),
                        nullable = False)
    courseDescription = Column(TEXT, 
                               nullable = True)
    limitedCourseUsers = Column(INTEGER(unsigned = True),
                                default = 100,
                                nullable = False)
    startDateOfCourse = Column(DATETIME, 
                               nullable = True)
    endDateOfCourse = Column(DATETIME, 
                             nullable = True)
    courseAdministratorIdIndex = Column(INTEGER(unsigned = True),
                                        ForeignKey(Members.memberIdIndex, 
                                                   onupdate = 'CASCADE', 
                                                   ondelete = 'CASCADE'), 
                                        nullable = False)
    courseAdministratorOrganizationIndex = Column(INTEGER(unsigned = True),
                                                  ForeignKey(Members.organizationIndex,
                                                             onupdate = 'CASCADE',
                                                             ondelete = 'CASCADE'),
                                                  nullable = False)
    isTeam = Column(ENUM(ENUMResources().const.TRUE,
                         ENUMResources().const.FALSE),
                    default = ENUMResources().const.FALSE,
                    nullable = False)
    isChance = Column(ENUM(ENUMResources().const.TRUE,
                           ENUMResources().const.FALSE),
                      default = ENUMResources().const.FALSE,
                      nullable = False)
    isDeleted = Column(ENUM(ENUMResources().const.TRUE,
                            ENUMResources().const.FALSE),
                       default = ENUMResources().const.FALSE,
                       nullable = False)
