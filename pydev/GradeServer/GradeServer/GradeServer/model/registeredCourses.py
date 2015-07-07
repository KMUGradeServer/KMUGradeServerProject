# -*- coding: utf-8 -*-
"""
    photolog.model.photo
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    photolog 어플리케이션을 사용할 사용자 정보에 대한 model 모듈.

    :copyright: (c) 2013 by 4mba.
    :license: MIT LICENSE 2.0, see license for more details.
"""


from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import DATETIME, VARCHAR, TEXT, ENUM

from GradeServer.model import Base
from GradeServer.model.members import Members

from GradeServer.resource.enumResources import ENUMResources

class RegisteredCourses (Base) :
    
    __tablename__ = "RegisteredCourses"
    
    # YYYY학기(1)과목(3)분반(2)
    courseId = Column(VARCHAR(10), 
                      primary_key = True, 
                      nullable = False)
    courseName = Column(VARCHAR(1024), 
                        nullable = False)
    courseDescription = Column(TEXT, 
                               nullable = True)
    startDateOfCourse = Column(DATETIME, 
                               nullable = True)
    endDateOfCourse = Column(DATETIME, 
                             nullable = True)
    courseAdministratorId = Column(VARCHAR(20),
                                   ForeignKey(Members.memberId, 
                                              onupdate = "CASCADE", 
                                              ondelete = "CASCADE"), 
                                   nullable = False)
    isTeam = Column(ENUM(ENUMResources().const.TRUE,
                         ENUMResources().const.FALSE),
                    default = ENUMResources().const.FALSE)
    isDeleted = Column(ENUM(ENUMResources().const.TRUE,
                            ENUMResources().const.FALSE),
                       default = ENUMResources().const.FALSE)