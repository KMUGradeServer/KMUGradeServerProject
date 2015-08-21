# -*- coding: utf-8 -*-
"""

   팀에 등록된 사용자 정보의 대한 모듈
"""


from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, ENUM

from model import Base
from model.teams import Teams
from model.members import Members

from resource.enumResources import ENUMResources

class RegisteredTeamMembers(Base) :
    
    __tablename__ = 'RegisteredTeamMembers'
    
    teamIndex = Column(INTEGER(unsigned = True),
                       ForeignKey(Teams.teamIndex,
                                  onupdate = 'CASCADE',
                                  ondelete = 'CASCADE'),
                       primary_key = True,
                       autoincrement = False,
                       nullable = False)
    teamMemberIdIndex = Column(INTEGER(unsigned = True),
                               ForeignKey(Members.memberIdIndex,
                                          onupdate = 'CASCADE',
                                          ondelete = 'CASCADE'),
                               primary_key = True,
                               autoincrement = False,
                               nullable = False)
    teamOrganizationIndex = Column(INTEGER(unsigned = True),
                                   ForeignKey(Members.organizationIndex,
                                              onupdate = 'CASCADE',
                                              ondelete = 'CASCADE'),
                                   primary_key = True,
                                   autoincrement = False,
                                   nullable = False)
    isTeamMaster = Column(ENUM(ENUMResources().const.TRUE,
                               ENUMResources().const.FALSE),
                          default = ENUMResources().const.FALSE,
                          nullable = False)
    isDeleted = Column(ENUM(ENUMResources().const.TRUE,
                            ENUMResources().const.FALSE),
                       default = ENUMResources().const.FALSE,
                       nullable = False)
    
