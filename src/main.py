from utils import *

def main(TEST_ID = "PHY101", STUDENT_ID = "S1"):

    # Load the data
    '''
    Modify the MongoDB data to a df of the format in data/questions.xlsx and data/responses.xlsx
    '''
    question_data = pd.read_excel('data/questions.xlsx')
    response_data = pd.read_excel('data/responses.xlsx')

    testwise_question_data = question_data[question_data['TestID'] == TEST_ID].reset_index(drop=True)
    testwise_response_data = response_data[response_data['TestID'] == TEST_ID].reset_index(drop=True)
    
    '''
    For each student, generate prompt, get grade and fill
    it in responses
    '''

    ## Load the feedback instructions
    with open("instructions.txt", "r") as f:
        instructions = f.read()

    student_response_data = testwise_response_data[testwise_response_data['StudentID'] == STUDENT_ID].reset_index(drop=True)
    partially_answered_topics = []
    unattempted_topics = []

    if 'Feedback' not in response_data.columns:
        response_data['Feedback'] = ""

    # for index, row in student_response_data.iterrows():
    for index, row in tqdm(student_response_data.iterrows(), total=len(student_response_data)):

        question_id = row['QuestionID']
        question_details = testwise_question_data[testwise_question_data['QuestionID'] == question_id]

        # Generate the appropriate prompt
        prompt = get_prompt(question_details, row)
        marks = student_response_data.at[index, 'MarksAwarded']

        # Use LLMs to get the marks and feedback
        marks = get_grade(prompt)
        total_marks = question_details['Marks'].values[0]

        '''
        If marks were somehow wrongly calculated, correct them
        '''
        if marks > total_marks:
            marks = total_marks
        elif marks < 0:
            marks = 0

        if marks < total_marks and marks > 0:
            partially_answered_topics.append(question_details['Topics'].values[0])
        elif marks == 0:
            unattempted_topics.append(question_details['Topics'].values[0])

        ## feedback from LLM
        if question_details['QuestionType'].values[0] == 'MCQ':
            feedback = "None"

        elif question_details['QuestionType'].values[0] == 'Subjective':
            prompt = get_feedback_prompt(question_details, row)
            messages = [
                {
                    "role": "system",
                    "content": instructions
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            feedback = call_feedback_llama(messages)
            feedback = feedback.replace("**Feedback:**", "").replace("**", "").replace("\n", "")
        
        # Fill the obtained marks and feedback in the response_data
        student_response_data.at[index, 'MarksAwarded'] = marks
        student_response_data.at[index, 'Feedback'] = feedback

        response_index = response_data[(response_data['TestID'] == TEST_ID) & (response_data['StudentID'] == STUDENT_ID) & (response_data['QuestionID'] == question_id)].index[0]
        response_data.at[response_index, 'MarksAwarded'] = marks
        response_data.at[response_index, 'Feedback'] = feedback

    response_data.to_excel('data/responses.xlsx', index=False)

    # Generate Feedback Report
    output_path = create_pdf(student_response_data, testwise_question_data)
    print(f"Report generated at {output_path}")

if __name__ == "__main__":
    TEST_ID = "PHY101"
    STUDENT_ID = ["S1"]

    for student_id in STUDENT_ID:
        print(f"Processing for student {student_id}")
        main(TEST_ID, student_id)
    


