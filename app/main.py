# Description: Main file for the Flask app.
# app/main.py

import sys

from pathlib import Path


project_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(project_dir))


import wave
from bardapi import Bard
from bardapi import BardCookies
from flask import Flask, render_template, request,jsonify
from app.ML.pipeline import Pipeline
from app.text_validation import Validator
from flask_cors import CORS 

import numpy as np
import os
import pytesseract
from PIL import Image
from utils import *
from pdf2image import convert_from_path
from config import *

# Need to download FFmpeg from "https://www.ffmpeg.org/download.html" 
# Need to download Tesseract.exe from "https://github.com/tesseract-ocr/tesseract" 


pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
cookie_dict = {
            "__Secure-1PSID": Secure_1PSID_COOKIE,
            "__Secure-1PSIDTS": Secure_1PSIDTS_COOKIE,
            "__Secure-1PSIDCC": Secure_1PSIDCC_COOKIE,
    # Any cookie values you want to pass session object.
            # Any cookie values you want to pass session object.
        }



app = Flask(__name__)
CORS(app)

pipeline = Pipeline()
validator = Validator()



bard = BardCookies(cookie_dict=cookie_dict)



@app.route("/api/writting/grade", methods=["POST"])
def writting_grade() -> str:
    """
    API endpoint to receive text data and return grade and warnings.
    """
    try:
        # Get JSON data from the request.
        data = request.get_json()
        # Extract essay text from JSON data.
        essay_text = data.get("answer_data", "")
        question_text = data.get("question_data", "")



        prompt = f"""Give me score for this IELTS essay with question. Score must be specify in [1.0->9.0]: 

        question: "{question_text}".
        essay: "{essay_text}"

       Your response is REQUIRED to FOLLOW FORMAT :
        "Overall score": ..
        "Explaination":... 
        The explaination MUST be at most 5 sentences
        """
        print(prompt)
        bardAns = bard.get_answer(prompt)['content']    

        # Check the input text for warnings.
        warnings = validator.run(essay_text)

        bardGrade = extract_grade(bardAns)


        # bardGrade =10
        # bardAns =""


        # Run the pipeline on the essay text and get the essay grade.
        essay_grade = pipeline.run([essay_text])

        # Prepare response data.
        response_data = {
            "model_grade": essay_grade,
            "warnings": warnings,
            "bard_grade":bardGrade,
            "explanation":bardAns
        }

        # Return the response as JSON.
        return jsonify(response_data)

    except Exception as e:
        # Handle exceptions and return an error response.
        return jsonify({"error": str(e)}), 500
    


# Load audio file




@app.route('/api/speaking/grade', methods=['POST'])
def speaking_grade():
    try:
        print(request)

        if 'file' not in request.files:
            return 'No file part'
        print("get file")
        
        file = request.files['file']
        print("file here:",file)
        question = request.form['question']
        print("question here:",question)

        if file.filename == '':
            return 'No selected file'
        

        answer = transcribe(file)
        print("done transcribe",answer)
        prompt = f"""You MUST give me score for this IELTS SPEAKING with question and text answer. Score must be specify in [1.0->9.0]: 

        question: "{question}".
        answer: "{answer}"

        Your response is REQUIRED to FOLLOW FORMAT :
        "Overall score": ..
        "Explaination":... 
        The explaination MUST be at most 5 sentences 
        """

        bardAns = bard.get_answer(prompt)['content']
        bardGrade = extract_grade(bardAns)

        # essay_grade = pipeline.run([answer])
        # bardGrade = 1
        # bardAns = " "
        # Save the result
        return {'grade':bardGrade,
                'explanation':bardAns}

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)})




@app.route('/api/ocr', methods=['POST'])
def ocr():
    if request.method == 'POST':
        try:
            # Get the image file from the request
            file = request.files['file']

            if file.filename.endswith('.pdf'):
                # Convert PDF to images
                pdf_path = 'temp.pdf'
                file.save(pdf_path)
                pages = convert_from_path(pdf_path)

                # Extract text from each page
                text = ''
                for page in pages:
                    text += pytesseract.image_to_string(page) + '\n'
                os.remove(pdf_path)
            else:
                # Read the image using PIL
                img = Image.open(file)

                # Extract text using Tesseract
                text = pytesseract.image_to_string(img)

            return jsonify({'text': text}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 400
        



if __name__ == "__main__":
    print("Running the app...")
    app.run(host='0.0.0.0', port=5000, debug=False)

