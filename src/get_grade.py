import os
import requests
from dotenv import load_dotenv
from groq import Groq
import pandas as pd
import re
import json

'''
Create a groq api key and put it in .env file
'''
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

'''
Add new models here
'''
models = ['llama3-8b-8192', 'gemma-7b-it', 'mixtral-8x7b-32768']


def get_grade(prompt):
    '''
    Given a prompt, call few llms and get marks.
    '''

    grades = []
    marks = []

    for model in models:
        if model == 'llama3-8b-8192':
            grade = call_llama(prompt)
        elif model == 'gemma-7b-it':
            grade = call_gemma(prompt)
        elif model == 'mixtral-8x7b-32768':
            grade = call_mixtral(prompt)
        try:
            '''
            grade will be of the format : "Sure, the marks is {'marks': 0}"
            So extract just the content in between {} and convert to dict 
            and then extract the marks from it
            '''
            start_index = grade.find('{')
            end_index = grade.rfind('}')
            mark = grade[start_index:end_index + 1]
            mark = mark.replace('\'', '\"')
            mark = json.dumps(mark)
            # print(mark)
            mark = json.loads(json.loads(mark))['marks']

            marks.append(mark)
        except:
            continue
        grades.append(grade)

    '''
    Calculate the mean marks and round it to nearest 0.5
    If all models fail, return -1 (Change this logic)
    If some llm fail, ignore it.
    '''
    total = 0
    cnt = 0
    for mark in marks:
        if type(mark) == int or type(mark) == float:
            total = total + mark
            cnt += 1
        else:
            continue
    if cnt == 0:
        mean_marks = -1
    else:
        mean_marks = total/cnt

    rounded_mark = round(mean_marks * 2) / 2

    return rounded_mark

'''
Functions to call specific models. Adjust temperature
to vary creativity of the models
'''
def call_llama(prompt):
    client = Groq(api_key=groq_api_key)
    chat_completion = client.chat.completions.create(
    messages=[{"role": "user", "content": prompt,}], model = "llama3-8b-8192", temperature =0)
    grade = chat_completion.choices[0].message.content
    return grade

def call_gemma(prompt):
    client = Groq(api_key=groq_api_key)
    chat_completion = client.chat.completions.create(
    messages=[{"role": "user", "content": prompt,}], model = "gemma-7b-it", temperature =0)
    grade = chat_completion.choices[0].message.content
    return grade

def call_mixtral(prompt):
    client = Groq(api_key=groq_api_key)
    chat_completion = client.chat.completions.create(
    messages=[{"role": "user", "content": prompt,}], model = "mixtral-8x7b-32768", temperature =0)
    grade = chat_completion.choices[0].message.content
    return grade

def call_feedback_llama(messages):
    client = Groq(api_key=groq_api_key)
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192",
        temperature=0.0
    )
    feedback = chat_completion.choices[0].message.content
    return feedback

if __name__ == "__main__":

    ''' Wrong Answer'''
    print("Wrong Answer MCQ")
    prompt = "For a MCQ question, the correct answer is option B, whereas the student selected option A. The marking scheme is 2 marks for a correct answer and 0 marks for an incorrect answer. How much did the student get for this MCQ? Return the answer as a python dictionary. No need any filler text other than dictionary. Example: {\"marks\": 0}"

    print(get_grade(prompt))



    ''' Correct Answer MCQ'''
    print("Correct Answer MCQ")
    prompt = "For a MCQ question, the correct answer is option B, whereas the student selected option B. The marking scheme is 2 marks for a correct answer and 0 marks for an incorrect answer. How much did the student get for this MCQ? Return the answer as a python dictionary. No need any filler text other than dictionary. Example: {\"marks\": 2}"

    print(get_grade(prompt))



    ''' Correct Answer'''
    print("Correct Answer Subjective")
    prompt = "For a Subjective answer type question, the correct answer is: \"Velocity at t=2 is v(2) = ds/dt = 6t + 2, so v(2) = 6(2) + 2 = 14 ms\". The student's response is: \"Velocity at t=2 is v(2) = ds/dt = 6t + 2, so v(2) = 6(2) + 2 = 14 m/s\". The marking scheme is 10 marks for a correct answer. Grade the student based on this: \"3 marks for Creativity, 3 marks for Clarity, 4 marks for Relevance\". How much did the student score for this question? Return the answer as a python dictionary. No need any filler text other than dictionary. Example: {\"marks\": 0}"
    print(get_grade(prompt))



    ''' Partially correct Answer'''
    print("Partially correct Answer Subjective")
    prompt = "For a Subjective answer type question, the correct answer is: \"Velocity at t=2 is v(2) = ds/dt = 6t + 2, so v(2) = 6(2) + 2 = 14 ms\". The student's response is: \"Velocity at t=2 is v(2) = ds/dt = 6t + 2, so v(2) = 6(2) + 2 = 10 m/s\". The marking scheme is 10 marks for a correct answer. Grade the student based on this: \"3 marks for Creativity, 3 marks for Clarity, 4 marks for Relevance\". How much did the student score for this question? Return the answer as a python dictionary. No need any filler text other than dictionary. Example: {\"marks\": 0}"
    print(get_grade(prompt))

