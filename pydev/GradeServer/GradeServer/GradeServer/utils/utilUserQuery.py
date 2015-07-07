
# -*- coding: utf-8 -*-

from GradeServer.utils.memberCourseProblemParameter import MemberCourseProblemParameter

from GradeServer.database import dao

from GradeServer.model.departments import Departments
from GradeServer.model.departmentsDetailsOfMembers import DepartmentsDetailsOfMembers
from GradeServer.model.colleges import Colleges
from GradeServer.model.members import Members
from GradeServer.model.registrations import Registrations

from GradeServer.resource.setResources import SETResources
from GradeServer.resource.sessionResources import SessionResources


'''
 DB Select All Members to User in Authority
 '''
def select_all_users():
        # 자동 완성을 위한 모든 유저기록
    return dao.query(Members.memberId,
                     Members.memberName).\
               filter(Members.authority == SETResources().const.USER)
    
'''
 DB Select MAtch Course
'''
def select_match_members_of_course(memberCourseProblemParameter = MemberCourseProblemParameter()):
    # courseId FilterLing
    members = select_all_users().subquery()
    return dao.query(Registrations.courseId,
                     members).\
               join(members,
                    Registrations.memberId == members.c.memberId).\
               filter(Registrations.courseId == memberCourseProblemParameter.courseId if memberCourseProblemParameter.courseId
                      else Registrations.courseId != None)
                      
'''
 DB Select Match MemberId
 '''
def select_match_member(memberCourseProblemParameter):
    # memberId Filterling
    return dao.query(Members).\
               filter(Members.memberId == memberCourseProblemParameter.memberId)
               
def select_match_member_sub(members, memberCourseProblemParameter = MemberCourseProblemParameter()):
    # memberId Filterling
    return dao.query(members).\
               filter(members.c.memberId == memberCourseProblemParameter.memberId)
               
               

'''
Update Member Information
'''
def update_member_informations(members, password, contactNumber, emailAddress, comment):
    members.update(dict(password = password,
                        contactNumber = contactNumber,
                        emailAddress = emailAddress,
                        comment = comment) if password 
                   else dict(contactNumber = contactNumber,
                        emailAddress = emailAddress,
                        comment = comment))
    
                    
'''
Join Members, College, Departments
'''
def join_member_informations(members):
    return dao.query(members,
                     Colleges.collegeName,
                     Departments.departmentName).\
               outerjoin(DepartmentsDetailsOfMembers,
                         members.c.memberId == DepartmentsDetailsOfMembers.memberId).\
               outerjoin(Colleges,
                         Colleges.collegeIndex == DepartmentsDetailsOfMembers.collegeIndex).\
               outerjoin(Departments,
                         Departments.departmentIndex == DepartmentsDetailsOfMembers.departmentIndex).\
               order_by(members.memberId)