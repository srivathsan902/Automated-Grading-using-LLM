from utils import *

def main(TEST_ID = "PHY101", STUDENT_ID = "S1"):
    # Load the data
    question_data = pd.read_excel('data/questions.xlsx')
    response_data = pd.read_excel('data/responses.xlsx')

    testwise_question_data = question_data[question_data['TestID'] == TEST_ID]
    testwise_response_data = response_data[response_data['TestID'] == TEST_ID]
    
    # For each student, generate prompt, get grade and fill
    # it in responses

    student_response_data = testwise_response_data[testwise_response_data['StudentID'] == STUDENT_ID]

    for index, row in student_response_data.iterrows():
        question_id = row['QuestionID']
        question_details = testwise_question_data[testwise_question_data['QuestionID'] == question_id]

        # Generate the appropriate prompt
        prompt = get_prompt(question_details, row)

        marks = student_response_data.at[index, 'MarksAwarded']
        feedback = student_response_data.at[index, 'Feedback']

        if marks == np.nan or feedback == "":
            continue

        # Use LLMs to get the marks and feedback
        marks = get_grade(prompt)

        # Fill the obtained marks and feedback in the response_data
        student_response_data.at[index, 'MarksAwarded'] = marks

        # Fill the obtained marks and feedback in the response_data
        response_index = response_data[(response_data['TestID'] == TEST_ID) & (response_data['StudentID'] == STUDENT_ID) & (response_data['QuestionID'] == question_id)].index[0]
        response_data.at[response_index, 'MarksAwarded'] = marks

    response_data.to_excel('data/responses.xlsx', index=False)

    # Generate Feedback Report
    output_path = create_pdf(student_response_data, testwise_question_data)
    print(f"Report generated at {output_path}")

if __name__ == "__main__":
    TEST_ID = "PHY101"
    STUDENT_ID = "S1"
    
    main()


