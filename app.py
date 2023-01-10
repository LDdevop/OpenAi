import os
import openai
import dotenv

from flask import Flask, request

app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')
dotenv.load_dotenv()


@app.route('/get_answer/<question>', methods=['POST'])
def get_answer_from_openai(question):
    """Make request to Open Ai and return response"""
    if request.method == 'POST':
        response = openai.Completion.create(
            model='text-davinci-003',
            prompt=generate_prompt(question),
            temperature=0,
            max_tokens=256,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return {"success": True,
                "message": response.choices[0].text.strip()}


@app.errorhandler(405)
def page_not_found(e):
    """Error handler for not allowed methods"""
    return {"success": False,
            "message": str(e)}


def generate_prompt(question):
    """Helper for Open Ai for answering on questions"""
    return f"""
            question: How are you?
            answer: I'm good
            question: Are you good in generation?
            answer: Yes, I'm
            question: {question.capitalize()}
            answer:
            """
