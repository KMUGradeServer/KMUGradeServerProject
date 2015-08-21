from model.submissions import Submissions
from resource.enumResources import ENUMResources
from resource.listResources import ListResources
from model.submittedRecordsOfProblems import SubmittedRecordsOfProblems

class DBUpdate(object):
    def __init__(self, stdNum, problemNum, courseNum, submitCount):
        self.stdNum = stdNum
        self.problemNum = problemNum
        self.courseNum = courseNum
        self.submitCount = submitCount
        
    def UpdateResutl(self, messageParaList, db_session, text):
        compileError = None
        testCase = None
        
        try:
            if len(messageParaList) != 4:
                return False
                
            else:
                result = messageParaList[0]
                score = messageParaList[1]
                runTime = messageParaList[2]
                usingMem = messageParaList[3]
            
                if result == ENUMResources.const.WRONG_ANSWER:
                    testCase = text
                    self.UpdateTable_SubmittedRecordsOfProblems_WrongAnswer(db_session)
                
                elif result == ENUMResources.const.TIME_OVER:
                    self.UpdateTable_SubmittedRecordsOfProblems_TimbeOver(db_session)
                
                elif result == ENUMResources.const.SOLVED:
                    self.UpdateTable_SubmittedRecordsOfProblems_Solved(db_session)
                    
                elif result == ENUMResources.const.RUNTIME_ERROR:
                    self.UpdateTable_SubmittedRecordsOfProblems_RunTimeError(db_session)
                    
                elif result == ENUMResources.const.COMPILE_ERROR:
                    compileError = text
                    self.UpdateTable_SubmittedRecordsOfProblems_CompileError(db_session)
                    
                else:
                    return False
                
                self.UpdateTableSubmissions(result, score, runTime, usingMem,
                                             db_session, compileError, testCase)
                
                db_session.commit()
                return True
        except Exception as e:
            db_session.rollback()
            return False
            
    
    def UpdateTableSubmissions(self, result, score, runTime, usingMem, db_session, compileError, testCase):
        try:
            db_session.query(Submissions).\
                filter_by(memberId = self.stdNum,
                          problemId = self.problemNum,
                          courseId = self.courseNum,
                          submissionCount = self.submitCount).\
                update(dict(status = ListResources.const.GRADERESULT_List.index(result),
                            score = score,
                            runTime = runTime,
                            usedMemory = usingMem,
                            solutionCheckCount = Submissions.solutionCheckCount+1,
                            compileErrorMessage = compileError,
                            wrongTestCaseNumber = int(testCase)))
        except Exception as e:
            raise e
    
    def UpdateTable_SubmittedRecordsOfProblems_CompileError(self, db_session):
        try:
            db_session.query(SubmittedRecordsOfProblems).\
                filter_by(problemId = self.problemNum,
                          courseId = self.courseNum).\
                          update(dict(sumOfSubmissionCount = SubmittedRecordsOfProblems.sumOfSubmissionCount + 1,
                                      sumOfCompileErrorCount = SubmittedRecordsOfProblems.sumOfCompileErrorCount + 1))
        except Exception as e:
            raise e
            
    def UpdateTable_SubmittedRecordsOfProblems_Solved(self, db_session):
        try:
            db_session.query(SubmittedRecordsOfProblems).\
                    filter_by(problemId = self.problemNum,
                              courseId = self.courseNum).\
                    update(dict(sumOfSubmissionCount = SubmittedRecordsOfProblems.sumOfSubmissionCount + 1,
                                sumOfSolvedCount = SubmittedRecordsOfProblems.sumOfSolvedCount + 1))
        except Exception as e:
            raise e
            
    def UpdateTable_SubmittedRecordsOfProblems_WrongAnswer(self, db_session):
        try:
            db_session.query(SubmittedRecordsOfProblems).\
                    filter_by(problemId = self.problemNum,
                              courseId = self.courseNum).\
                    update(dict(sumOfSubmissionCount = SubmittedRecordsOfProblems.sumOfSubmissionCount + 1,
                                sumOfWrongCount = SubmittedRecordsOfProblems.sumOfWrongCount + 1))
        except Exception as e:
            raise e
            
    def UpdateTable_SubmittedRecordsOfProblems_TimbeOver(self, db_session):
        try:
            db_session.query(SubmittedRecordsOfProblems).\
                    filter_by(problemId = self.problemNum,
                              courseId = self.courseNum).\
                    update(dict(sumOfSubmissionCount = SubmittedRecordsOfProblems.sumOfSubmissionCount + 1,
                                sumOfTimeOverCount = SubmittedRecordsOfProblems.sumOfTimeOverCount + 1))
        except Exception as e:
            raise e
            
    def UpdateTable_SubmittedRecordsOfProblems_RunTimeError(self, db_session):
        try:
            db_session.query(SubmittedRecordsOfProblems).\
                    filter_by(problemId = self.problemNum,
                              courseId = self.courseNum).\
                    update(dict(sumOfSubmissionCount = SubmittedRecordsOfProblems.sumOfSubmissionCount + 1,
                                sumOfRuntimeErrorCount = SubmittedRecordsOfProblems.sumOfRuntimeErrorCount + 1))
        except Exception as e:
            raise e
   
    @staticmethod
    def UpdateServerError(stdNum, problemNum, courseNum, submitCount, db_session):
        try :
            db_session.query(Submissions).\
                filter_by(memberId = stdNum,
                          problemId = problemNum,
                          courseId = courseNum,
                          submissionCount = submitCount).\
                update(dict(status = 8,
                            score = 0,
                            runTime = 0,
                            usedMemory = 0))
            db_session.commit()
            print '...server error...'
        except Exception as e:
            raise e