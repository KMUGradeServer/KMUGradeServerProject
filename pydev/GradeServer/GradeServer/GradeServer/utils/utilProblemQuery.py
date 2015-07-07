# -*- coding: utf-8 -*-


from datetime import datetime
from sqlalchemy import and_

from GradeServer.database import dao

from GradeServer.utils.memberCourseProblemParameter import MemberCourseProblemParameter

from GradeServer.model.registeredProblems import RegisteredProblems
from GradeServer.model.submissions import Submissions
from GradeServer.model.problems import Problems
from GradeServer.resource.enumResources import ENUMResources
from GradeServer.resource.otherResources import OtherResources


'''
Get Select Problems
case Gold, Silver, Bronze
'''
def select_problems(activeTabId = OtherResources().const.ALL, isDeleted = ENUMResources().const.FALSE):
    
    if activeTabId == OtherResources().const.ALL:
        return dao.query(Problems).\
                   filter(Problems.isDeleted == isDeleted).\
                   order_by(Problems.problemId.asc())
    elif activeTabId == OtherResources().const.GOLD:
        return dao.query(Problems).\
                   filter(Problems.problemId >= int(30000),
                          Problems.isDeleted == isDeleted).\
                   order_by(Problems.problemId.asc())
    elif activeTabId == OtherResources().const.SILVER:
        return dao.query(Problems).\
                   filter(and_(30000 > Problems.problemId,
                               Problems.problemId >= int(20000)),
                          Problems.isDeleted == isDeleted).\
                   order_by(Problems.problemId.asc())
    elif activeTabId == OtherResources().const.BRONZE:
        return dao.query(Problems).\
                   filter(and_(20000 > Problems.problemId,
                               Problems.problemId >= int(10000)),
                          Problems.isDeleted == isDeleted).\
                   order_by(Problems.problemId.asc())
            


'''
Get Problem Information
'''
def select_problem_informations(memberCourseProblemParameter = MemberCourseProblemParameter(), isDeleted = ENUMResources().const.FALSE):
    return dao.query(Problems).\
               filter(Problems.problemId == memberCourseProblemParameter.problemId,
                      Problems.isDeleted == isDeleted)
               
               
               
'''
Get Problems of Course
'''
def select_problems_of_course(memberCourseProblemParameter = MemberCourseProblemParameter()):
    return dao.query(RegisteredProblems).\
               filter(RegisteredProblems.courseId == memberCourseProblemParameter.courseId,
                      (RegisteredProblems.problemId == memberCourseProblemParameter.problemId if memberCourseProblemParameter.problemId
                       else RegisteredProblems.openDate <= datetime.now()))


'''
Join Problem Names
'''
def join_problems_names(registeredProblems, isDeleted = ENUMResources().const.FALSE):
    return dao.query(registeredProblems,
                     Problems.problemName).\
               join(Problems,
                    registeredProblems.c.problemId == Problems.problemId).\
               filter(Problems.isDeleted == isDeleted)


'''
OuterJoin Problem List and submission_code
'''
def join_problem_lists_submissions(problems, submissions):
    return dao.query(problems,
                     submissions.c.score,
                     submissions.c.status,
                     submissions.c.submissionCount,
                     submissions.c.solutionCheckCount).\
               outerjoin(submissions,
                         problems.c.problemId == submissions.c.problemId).\
               order_by(problems.c.startDateOfSubmission.desc())
   

'''
Submission code View Counting
'''
def update_submission_code_view_count(lastSubmission, memberCourseProblemParameter = MemberCourseProblemParameter()):
    dao.query(Submissions).\
        filter(Submissions.memberId == memberCourseProblemParameter.memberId,
               Submissions.courseId == memberCourseProblemParameter.courseId,
               Submissions.problemId == memberCourseProblemParameter.problemId,
               Submissions.submissionCount == lastSubmission.c.submissionCount).\
        update(dict(viewCount = Submissions.viewCount + 1))