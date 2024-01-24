# IELTS Grading

IELTS Grading is a server where we deploy our models in our app with two main features: Speaking Grading and Writing Grading.

## Architecture

- Writing Grading: We use a model from [GitHub](https://github.com/Logisx/DeepEssay) and utilize __BardAPI__ for giving two answers for more detail. With __DeepEssay__, we use the examinee essay as input and the score as output. With __BardAPI__, we use the prompt to get the score and explanation.
- Speaking Grading: We utilize _pydub_ and _ffmpeg_ to convert MP3 to WAV and __DeepSpeech__ for __Speech-to-Text__. Afterward, we use __BardAPI__ again to grade the candidate's work.
- We also support __Tesseract OCR__ for converting PDF or images to text for Writing Grading.

## API Endpoint

### OCR

- __Request__: 
    ```
    POST: '/api/ocr'`.  
    Content-Type: multipart/form-data
    Body:
   {
       "file": file (type binary file))
    }. 
    ```
- __Response__: 
    ```
    {"text": text-after-ocr (string)}
    ```

### Writing Grading

- __Request__: 
    ```
    POST: '/api/writting/grade'`. 
    Content-Type: application/json
    Body:
    {
        "question": question-of-test (string),
        "answer"  : answer-of-candidate (string).
    }
    ```

- __Response__: 
    ```
    {
        "model_grade": score-from-deepessay-model (double),
        "warnings"    : warnings (array of strings), 
        "bard_grade"  : score-from-bard-model (double), 
        "explanation" : explanation-from-bard (string)
    }
    ```
### Speaking Grading

- __Request__: 
```

    POST: '/api/speaking/grade' 
    Content-Type: multipart/form-data
    Body: 
    {
        "file"   : answer-file (binary file), 
        "question": question-of-test (string)
    } 
 ```
- __Response__: 
```
  {
    "grade"      : score-from-bard-model (double), 
    "explanation": explanation-from-bard (string)
  }
```
##  Installing 

### Prerequisites (only Windows)

- ffmpeg: https://ffmpeg.org/download.html
- Tesseract OCR model: https://github.com/tesseract-ocr/tesseract
- DeepSpeech model: https://github.com/mozilla/DeepSpeech
- Writing model: after training, follow the instruction: https://github.com/Logisx/DeepEssay
- BardAPI: not having original API, use cookie approach: https://github.com/dsdanielpark/Bard-API


Ensure your **Tesseract** in path : 
    **C:\Program Files\Tesseract-OCR\tesseract.exe**
      ,  
  **ffmpeg** in path : **C:\ffmpeg\bin\ffmpeg.exe**, and your cookies should be valid or you should change it in **config.py**
### Steps

- Clone the repository: 

```bash
    git clone https://github.com/lokissdo/ielts-grading
```

- Place the writing model in ML folder:

```
	\---models
|   |       +---training_bert_num
|   |       |
|   |       +---training_bert_num_bin
|   |       |
|   |       \---training_bert_text

```

- Place the DeepSpeech model in app folder:
```
	\---speechtotext
|   |       +---deepspeech-0.9.3-models.pbmm
|   |       |
|   |       +---deepspeech-0.9.3-models.scorer
|   |       |
```

- Install the requirements:

```bash
    pip install -r requirements.txt
```
- Run the app: 

```bash
    pip app/main.py
```



Make sure to follow the provided links for downloading and setting up the required models and libraries.


## ⚖️ License

[MIT](https://github.com/Logisx/DeepEssay/blob/main/LICENSE)


## 🔗 Links
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/do-khai-hung-3b5a18231/)
[![facebook](http://i.imgur.com/P3YfQoD.png)](https://www.facebook.com/hung.khai.982292/)


