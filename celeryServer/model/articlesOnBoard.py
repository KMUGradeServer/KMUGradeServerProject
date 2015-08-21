# -*- coding: utf-8 -*-
"""
    게시판 글 정보 모듈
"""


from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, DATETIME, TEXT, ENUM

from model import Base
from model.registeredCourses import RegisteredCourses
from model.members import Members
from model.registeredProblems import RegisteredProblems
from resource.enumResources import ENUMResources

class ArticlesOnBoard(Base) :
    
    __tablename__ = 'ArticlesOnBoard'
    
    articleIndex = Column(INTEGER(unsigned = True),
                          primary_key = True,
                          autoincrement = True,
                          nullable = False) 
    articleType = Column(ENUM(ENUMResources().const.NOTICE,
                              ENUMResources().const.QUESTION,
                              ENUMResources().const.NORMAL),
                         default = ENUMResources().const.NORMAL,
                         nullable = False)    # checker for notice
    writerIdIndex = Column(INTEGER(unsigned = True),
                           ForeignKey(Members.memberIdIndex,
                                      onupdate = 'CASCADE',
                                      ondelete = 'CASCADE'),
                           nullable = False)
    writerOrganizationIndex = Column(INTEGER(unsigned = True),
                                     ForeignKey(Members.organizationIndex,
                                                onupdate = 'CASCADE',
                                                ondelete = 'CASCADE'),
                                     nullable = False)
    problemIndex = Column(INTEGER(unsigned = True),
                          ForeignKey(RegisteredProblems.problemIndex,
                                     onupdate = 'CASCADE',
                                     ondelete = 'CASCADE'),
                          nullable =True)
    courseIndex = Column (INTEGER(unsigned = True),
                          ForeignKey(RegisteredCourses.courseIndex,
                                     onupdate = 'CASCADE',
                                     ondelete = 'CASCADE'),
                          nullable =True)
    title = Column(VARCHAR(1024),
                   nullable = False)
    content = Column(TEXT,
                     nullable = False) # contents of article
    viewCount = Column(INTEGER(unsigned = True),
                       default = 0,
                       nullable = False) 
    replyCount = Column(INTEGER(unsigned = True),
                        default = 0,
                        nullable = False)
    sumOfLikeCount = Column(INTEGER(unsigned = True),
                            default = 0,
                            nullable = False)
    updateIp = Column(VARCHAR(20),
                      nullable = False)
    updateDate = Column(DATETIME,
                         nullable = False)
    isDeleted = Column(ENUM (ENUMResources().const.TRUE,
                             ENUMResources().const.FALSE),
                       default = ENUMResources().const.FALSE,
                       nullable = False)
    
