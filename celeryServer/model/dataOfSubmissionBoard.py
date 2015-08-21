
# -*- coding: utf-8 -*-
"""
사용자들의 문제별 제출 소스 확인 모듈
"""


from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER

from model import Base
from model.teams import Teams
from model.members import Members
from model.registeredProblems import RegisteredProblems


class DataOfSubmissionBoard(Base) :
    
    __tablename__ = 'DataOfSubmissionBoard'
    
    submissionIndex = Column(INTEGER(unsigned = True),
                             primary_key = True,
                             autoincrement = True,
                             nullable = False)
    teamIndex = Column(INTEGER(unsigned = True),
                       ForeignKey(Teams.teamIndex,
                                  onupdate = 'CASCADE',
                                  ondelete = 'CASCADE'),
                       nullable = True,
                       unique = True)
    memberIdIndex = Column(INTEGER(unsigned = True),
                           ForeignKey(Members.memberIdIndex,
                                      onupdate = 'CASCADE',
                                      ondelete = 'CASCADE'),
                           nullable = False,
                           unique = True)
    organizationIndex = Column(INTEGER(unsigned = True),
                               ForeignKey(Members.organizationIndex,
                                          onupdate = 'CASCADE',
                                          ondelete = 'CASCADE'),
                               nullable = False,
                               unique = True)
    problemIndex = Column(INTEGER(unsigned = True),
                          ForeignKey(RegisteredProblems.problemIndex,
                                     onupdate = 'CASCADE',
                                     ondelete = 'CASCADE'),
                          nullable = False,
                          unique = True)
    courseIndex = Column(INTEGER(unsigned = True),
                         ForeignKey(RegisteredProblems.courseIndex,
                                    onupdate = 'CASCADE',
                                    ondelete = 'CASCADE'),
                         nullable = False,
                         unique = True)
    viewCount = Column(INTEGER(unsigned = True),
                       default = 0,
                       nullable = False)
    submissionReplyCount = Column(INTEGER(unsigned = True),
                                   default = 0,
                                   nullable = False)
    sumOfLikeCount = Column(INTEGER(unsigned = True),
                            default = 0,
                            nullable = False)
    
