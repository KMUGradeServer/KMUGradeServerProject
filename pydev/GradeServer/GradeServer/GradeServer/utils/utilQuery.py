# -*- coding: utf-8 -*-

from flask import session
from sqlalchemy import func

from GradeServer.resource.setResources import SETResources
from GradeServer.resource.enumResources import ENUMResources
from GradeServer.resource.languageResources import LanguageResources
from GradeServer.resource.routeResources import RouteResources
from GradeServer.resource.messageResources import MessageResources
from GradeServer.resource.htmlResources import HTMLResources
from GradeServer.resource.otherResources import OtherResources
from GradeServer.resource.sessionResources import SessionResources

from GradeServer.utils.utilCourseQuery import select_accept_courses,\
                                              select_current_courses,\
                                              select_past_courses

from GradeServer.database import dao
        
        
'''
Record count
'''
def select_count(keySub):
    return dao.query(func.count(keySub).label('count'))


'''
Template
'''
from repoze.lru import lru_cache
from GradeServer.GradeServer_blueprint import GradeServer
@lru_cache(maxsize = 256)
@GradeServer.context_processor
def utility_processor():
    # Return Current, Past courses
    def get_current_past_courses():
        # Init Courses 
        currentCourses, pastCourses = [], []
        # Login status
        if session:   
            courses = select_accept_courses().subquery()
            try:
                currentCourses = select_current_courses(courses).all()
                pastCourses = select_past_courses(courses).all()
            except Exception:
                pass
            
            return (currentCourses, pastCourses)
        
    def get_enum_resources():
        return ENUMResources
    
    def get_html_resources():
        return HTMLResources
    
    def get_language_resources():
        return LanguageResources
    
    def get_message_resources():
        return MessageResources
    
    def get_other_resources():
        return OtherResources
    
    def get_route_resources():
        return RouteResources
    
    def get_session_resources():
        return SessionResources
    
    def get_set_resources():
        return SETResources
    
    return dict(get_current_past_courses = get_current_past_courses,
                ENUMResources = get_enum_resources,
                HTMLResources = get_html_resources,
                LanguageResources =get_language_resources,
                MessageResources = get_message_resources,
                OtherResources = get_other_resources,
                RouteResources = get_route_resources,
                SessionResources = get_session_resources,
                SETResources = get_set_resources)
    