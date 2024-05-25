import os
import yaml
from pdf import PDF
import matplotlib.pyplot as plt


def create_pdf(student_data, questions_data):
    '''
    Header Formating
    '''
    pdf = PDF('P', 'mm', 'A4')
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('helvetica', '', 12)
    
    pdf.cell(0, 10, f'Name: {student_data["Name"][0]}', 0, 0, 'L')
    pdf.cell(0, 10, 'Date: 22/05/2024', 0, 1, 'R')

    pdf.cell(0, 10, f'Test ID: {student_data["TestID"][0]}', 0, 0, 'L')
    marks_obtained = sum(student_data['MarksAwarded'])
    total_marks = sum(questions_data['Marks'])
    pdf.cell(0, 10, f'Marks Obtained: {marks_obtained}/{total_marks}', 0, 1, 'R')
    
    pdf.ln(5)
    pdf.set_line_width(1)
    pdf.line(pdf.get_x(), pdf.get_y(), 210 - pdf.r_margin, pdf.get_y())
    pdf.ln(5)

    '''
    For Mark Distribution Pie Chart
    '''
    correct_marks = 0
    partial_marks_obtained = 0
    partial_marks_missed = 0
    unattempted_marks = 0

    for index, row in questions_data.iterrows():
        '''
        Iterate through all questions to display questions, correct answer,
        marks awarded etc
        '''
        question_id = row['QuestionID']
        question = row['Question']
        question_type = row['QuestionType']

        if question_type == 'MCQ':
            optionA = row['OptionA']
            optionB = row['OptionB']
            optionC = row['OptionC']
            optionD = row['OptionD']

        correct_answer = row['CorrectAnswer']
        response = student_data[student_data['QuestionID'] == question_id]['Student_Response']

        if response.empty:
            response = 'Unattempted'
            feedback = str(" ")
        else:
            response = response.values[0]
            feedback = str(student_data[student_data['QuestionID'] == question_id]['Feedback'].values[0])

        awarded_marks = student_data[student_data['QuestionID'] == question_id]['MarksAwarded']
        if awarded_marks.empty:
            awarded_marks = 0
        else:
            awarded_marks = awarded_marks.values[0]

        actual_marks = row['Marks']

        '''
        Set the fill color based on the marks awarded
        '''
        if awarded_marks == actual_marks:
            correct_marks += actual_marks
            pdf.set_fill_color(198, 245, 204)

        elif awarded_marks == 0:
            unattempted_marks += actual_marks
            pdf.set_fill_color(252, 210, 204)

        else:
            partial_marks_obtained += awarded_marks
            partial_marks_missed += actual_marks - awarded_marks
            pdf.set_fill_color(237, 230, 192)

        
        explanation = row['Explanation']

        pdf.set_line_width(0.5)

        content = ""
        content += f'{question_id}: {question} [{actual_marks} marks]\n'

        if question_type == 'MCQ':
            content += f'A: {optionA}\n'
            content += f'B: {optionB}\n'
            content += f'C: {optionC}\n'
            content += f'D: {optionD}\n'
        
        content += f'Student Response: {response}\n'
        content += f'Correct Answer: {correct_answer}\n'
        content += f'Explanation: {explanation}\n'
        content += f'Feedback: {feedback}\n' 
        content += f'Marks Awarded: {awarded_marks}\n'

        pdf.multi_cell(0, 10, content, border=1, ln=1, align='L', fill=True)
        pdf.ln(5)

    '''
    Create Pie Chart Visualization
    '''
    labels = ['Correct', 'Partial Correct', 'Partial Incorrect', 'Unattempted']
    sizes = [(correct_marks/total_marks)*100, (partial_marks_obtained/total_marks)*100, (partial_marks_missed/total_marks)*100, (unattempted_marks/total_marks)*100]  # Percentages for each slice
    colors = ['green', 'yellow', 'orange', 'red']
    explode = (0, 0, 0, 0) 

    # Plot and save figure
    plt.figure(figsize=(6,6))  # Aspect ratio 1:1
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Title
    plt.title("Mark Distribution")
    plt.savefig('assets/mark_distribution.png')

    # Load the saved image and add it to the pdf
    img_width , img_height = 100, 100
    if pdf.get_y() > 297 - pdf.b_margin-img_height-10:
        pdf.add_page()
    pdf.image('assets/mark_distribution.png', pdf.get_x() + 50, pdf.get_y() + 10, w = img_width, h = img_height)


    filename = f'{student_data["StudentID"][0] + student_data["TestID"][0]}.pdf'
    pdf.output(os.path.join("reports", filename))

    return filename



