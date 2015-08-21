# -*- coding: utf-8 -*-
"""
    GradeServer.model
    ~~~~~~~~~~~~~~

    GradeSever에 적용될 model에 대한 패키지 초기화 모듈.

    :copyright: (c) 2015 kookminUniv
"""


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

__all__ = ['organizations', 'membersId', 'members', 
           'languages', 'registeredCourses', 'languageOfCourses', 
           'registrations', 
           'problems', 'problemSetNames', 'problemSets', 'detailsOfProblemSets', 'registeredProblems', 
           'submittedRecordsOfProblems', 'submittedFiles', 'dataOfSubmissionBoard',
           'likesOnSubmission', 'submissions', 'repliesOnSubmission', 'likesOnReplyOfSubmission',
           'articlesOnBoard', 'likesOnBoard', 'repliesOnBorad', 'likesOnReplyOfBoard', 
           'teams', 'registeredTeamMembers', 'teamInvitations']
