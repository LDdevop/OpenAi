import os
import openai
import dotenv

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')
dotenv.load_dotenv()


@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        question = request.form['question']
        response = openai.Completion.create(
            model='text-davinci-003',
            prompt=generate_prompt(question),
            temperature=0,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return redirect(url_for('index', result=response.choices[0].text))

    result = request.args.get('result')
    return render_template('index.html', result=result)


def generate_prompt(question):
    return f"""
            question: How are you?
            answer: I'm good
            question: Are you good in generation?
            answer: Yes, I am
            question: {question.capitalize()}
            answer:"""
