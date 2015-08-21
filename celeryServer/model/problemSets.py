# -*- coding: utf-8 -*-
"""
    문제집에 대한 정보 모듈
"""


from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, ENUM

from model import Base 
from model.members import Members
from model.problemSetNames import ProblemSetNames

from resource.enumResources import ENUMResources

class ProblemSets(Base) :
    
    __tablename__ = 'ProblemSets'
    
    problemSetIndex = Column(INTEGER(unsigned = True),
                             primary_key = True, 
                             autoincrement = True,
                             nullable = False)
    problemSetOrganizationIndex = Column(INTEGER(unsigned = True),
                                         ForeignKey(Members.organizationIndex,
                                                    onupdate = 'CASCADE',
                                                    ondelete = 'CASCADE'),
                                         nullable = False,
                                         unique = True)
    problemSetMemberIdIndex = Column(INTEGER(unsigned = True),
                                     ForeignKey(Members.memberIdIndex,
                                                onupdate = 'CASCADE',
                                                ondelete = 'CASCADE'),
                                     nullable = False,
                                     unique = True)
    
    problemSetNameIndex = Column(INTEGER(unsigned = True),
                                 ForeignKey(ProblemSetNames.problemSetNameIndex,
                                            onupdate = 'CASCADE',
                                            ondelete = 'CASCADE'),
                                 nullable = False,
                                 unique = True)
    isPublic = Column(ENUM(ENUMResources().const.TRUE,
                           ENUMResources().const.FALSE),
                      default = ENUMResources().const.FALSE,
                      nullable = False)    
