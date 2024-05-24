from langchain.prompts import PromptTemplate

'''
The variable inside {} will be replaced by the values of
the input variables passed while calling the prompt.
'''
def get_prompt(question_details, student_response):
    '''
    question_details is one row of question_data
    student_response is one row of response_data
    '''
    prompt = ''
    
    mcq_prompt = PromptTemplate(
                    input_variables = ["correct_answer", "student_answer", "marks"],
                    template = r"For a MCQ question, the correct answer is option {correct_answer}, whereas the student selected option {student_answer}. The marking scheme is {marks} marks for a correct answer and 0 marks for an incorrect answer. How much did the student get for this MCQ? Return the answer as a python dictionary. No need any filler text other than dictionary. Example: {{'marks': 2}}"
                )

    subjective_prompt = PromptTemplate(
                        input_variables = ["correct_answer", "student_answer", "marks", "criterion"],
                        template = r"For a Subjective answer type question, the correct answer is: \"{correct_answer}\". The student's response is: \"{student_answer}\". The marking scheme is {marks} marks for a correct answer. Grade the student based on this: \"{criterion}\". How much did the student score for this question? Return the answer as a python dictionary. No need any filler text other than dictionary. Example: {{'marks': 0}}"
                    )
    
    if question_details['QuestionType'].values[0] == 'MCQ':
        prompt = mcq_prompt.format(correct_answer = question_details['CorrectAnswer'].values[0], student_answer = student_response['Student_Response'], marks = question_details['Marks'].values[0])
        
    elif question_details['QuestionType'].values[0] == 'Subjective':
        prompt = subjective_prompt.format(correct_answer = question_details['CorrectAnswer'].values[0], student_answer = student_response['Student_Response'], marks = question_details['Marks'].values[0], criterion = question_details['MarkingCriterion'].values[0])

    return prompt