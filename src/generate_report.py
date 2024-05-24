import os
import yaml
from pdf import PDF


def create_pdf(student_data, questions_data):
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

    for index, row in questions_data.iterrows():
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
        # print(response)
        if response.empty:
            response = 'Unattempted'
        else:
            response = response.values[0]

        awarded_marks = student_data[student_data['QuestionID'] == question_id]['MarksAwarded']
        if awarded_marks.empty:
            awarded_marks = 0
        else:
            awarded_marks = awarded_marks.values[0]

        actual_marks = row['Marks']

        explanation = row['Explanation']

        pdf.set_line_width(0.5)
        pdf.set_fill_color(230, 230, 230)

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
        content += f'Marks Awarded: {awarded_marks}\n'

        pdf.multi_cell(0, 10, content, border=1, ln=1, align='L', fill=True)
        pdf.ln(5)
    
    filename = f'{student_data["StudentID"][0] + student_data["TestID"][0]}.pdf'
    pdf.output(os.path.join("reports", filename))

    return filename



