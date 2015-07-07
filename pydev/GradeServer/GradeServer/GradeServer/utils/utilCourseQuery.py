# -*- coding: utf-8 -*-


from GradeServer.resource.enumResources import ENUMResources
from GradeServer.database import dao

from GradeServer.model.registeredCourses import RegisteredCourses
from GradeServer.model.languages import Languages
from GradeServer.model.languagesOfCourses import LanguagesOfCourses


'''
Select RegisteredCourses
'''
def select_registered_courses(isDeleted = ENUMResources().const.FALSE):
    return dao.query(RegisteredCourses).\
               filter(RegisteredCourses.isDeleted == isDeleted).\
               order_by(RegisteredCourses.endDateOfCourse.desc())
               
               
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
