# -*- coding: utf-8 -*-


from flask import session
from datetime import datetime
from GradeServer.resource.enumResources import ENUMResources
from GradeServer.database import dao

from GradeServer.model.registeredCourses import RegisteredCourses
from GradeServer.model.languages import Languages
from GradeServer.model.languagesOfCourses import LanguagesOfCourses
from GradeServer.model.registrations import Registrations

from GradeServer.resource.setResources import SETResources
from GradeServer.resource.sessionResources import SessionResources


'''
허용된 과목 정보
'''
def select_accept_courses():
    # 서버 마스터는 모든 과목에 대해서, 그 외에는 지정된 과목에 대해서
    try:
        # Server Master
        if SETResources().const.SERVER_ADMINISTRATOR in session[SessionResources().const.AUTHORITY]:
            myCourses = dao.query(RegisteredCourses.courseId,
                                  RegisteredCourses.courseName,
                                  RegisteredCourses.endDateOfCourse)
        # Class Master
        elif SETResources().const.COURSE_ADMINISTRATOR in session[SessionResources().const.AUTHORITY]:
            myCourses = dao.query(RegisteredCourses.courseId,
                                  RegisteredCourses.courseName,
                                  RegisteredCourses.endDateOfCourse).\
                            filter(RegisteredCourses.courseAdministratorId == session[SessionResources().const.MEMBER_ID])
        # User
        else:
            myCourses = dao.query(Registrations.courseId,
                                  RegisteredCourses.courseName,
                                  RegisteredCourses.endDateOfCourse).\
                            join(RegisteredCourses,
                                 Registrations.courseId == RegisteredCourses.courseId).\
                            filter(Registrations.memberId == session[SessionResources().const.MEMBER_ID])
                            
                            
    # Session Error Catch
    except Exception:
        myCourses = dao.query(RegisteredCourses.courseId,
                              RegisteredCourses.courseName,
                              RegisteredCourses.endDateOfCourse).\
                        filter(RegisteredCourses.courseId == None)
                        
    return myCourses



'''
Select RegisteredCourses
'''
def select_registered_courses(isDeleted = ENUMResources().const.FALSE):
    return dao.query(RegisteredCourses).\
               filter(RegisteredCourses.isDeleted == isDeleted).\
               order_by(RegisteredCourses.endDateOfCourse.desc())
      
      
'''
Course Information
'''
def select_registered_course(courseId, isDeleted = ENUMResources().const.FALSE):
    return dao.query(RegisteredCourses).\
               filter(RegisteredCourses.courseId == courseId,
                      RegisteredCourses.isDeleted == isDeleted)
               
                        
               
'''
Select Language of Course
'''
def select_language_of_course():
    return dao.query(LanguagesOfCourses.courseId, 
                     Languages.languageName,
                     Languages.languageVersion).\
               join(Languages,
                    LanguagesOfCourses.languageIndex == Languages.languageIndex)
               
               
'''
Select Past, Current course
'''
def select_past_courses(myCourses):
    return dao.query(myCourses).\
               filter(myCourses.c.endDateOfCourse < datetime.now())
def select_current_courses(myCourses):
    return dao.query(myCourses).\
               filter(myCourses.c.endDateOfCourse >= datetime.now())
               
                  
           
'''
Insert RegisteredCourse
'''
def insert_registered_course(courseId, courseName, courseDescription, startDateOfCourse, endDateOfCourse, courseAdministratorId, isTeam):
    return RegisteredCourses(courseId = courseId, 
                             courseName = courseName, 
                             courseDescription = courseDescription,
                             startDateOfCourse = startDateOfCourse, 
                             endDateOfCourse = endDateOfCourse, 
                             courseAdministratorId = courseAdministratorId)
    
    
    
'''
Insert new_language_of_course
'''
def insert_language_of_course(courseId, languageIndex):
    return LanguagesOfCourses(courseId = courseId,
                              languageIndex = languageIndex)
    
    
'''
Update Deleted
'''
def update_registered_course_deleted(courseId, isDeleted = ENUMResources().const.TRUE):
    return dao.query(RegisteredCourses).\
               filter(RegisteredCourses.courseId == courseId).\
               update(dict(isDeleted = isDeleted))
