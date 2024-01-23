import re
from pydub import AudioSegment
import deepspeech
import wave
import numpy as np


STT_MODEL_PATH = "./app/speech2text/deepspeech-0.9.3-models.pbmm"
LM_PATH = "./app/speech2text/deepspeech-0.9.3-models.scorer"
BEAM_WIDTH = 500





sttModel = deepspeech.Model(STT_MODEL_PATH)
sttModel.enableExternalScorer(LM_PATH)
# sttModel.setScorerBeamWidth(BEAM_WIDTH)


def extract_grade(text):
    # Find the first occurrence of a number in the text
    # start_index = None
    # end_index = None
    # for i, char in enumerate(text):
    #     if char.isdigit() or char == '.':
    #         if start_index is None:
    #             start_index = i
    #         end_index = i
    #     elif start_index is not None:
    #         break

    # # Extract the grade
    # if start_index is not None:
    #     grade = float(text[start_index:end_index + 1])
    #     return grade
    match = re.search(r'[0-9]+((\.|,)[0-9]*)?', text)
    if match:
        return float(match.group())
    else:
        return None
    
AudioSegment.converter  = "C://ffmpeg/bin/ffmpeg.exe" 
def convert_audio(file):
    # Load audio file
    audio = AudioSegment.from_mp3(file)

    # Convert stereo to mono
    audio = audio.set_channels(1)

    # Change sample rate to 16000Hz
    audio = audio.set_frame_rate(16000)

    return audio

def transcribe(file):
        audio = convert_audio(file)

        # Save the result
        buffer = audio.get_array_of_samples()
        # Not 64-bit RIFF file
        # Convert buffer to 16-bit int array for DeepSpeech
        data16 = np.frombuffer(buffer, dtype=np.int16)

        # Perform transcription
        text = sttModel.stt(data16)

        return text

