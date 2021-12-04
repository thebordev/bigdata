from PIL import Image
import pytesseract
import cv2
from nltk.corpus import stopwords
import re
import os
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from pymorphy2 import MorphAnalyzer

from config import FACE_MODEL, BAD_WORDS, ROOT_DIRECTORY

russian_stopwords = stopwords.words("russian")


def photo_to_text(filepath):
    return pytesseract.image_to_string(Image.open(filepath))


def face_detect(filepath):
    face_cascade = cv2.CascadeClassifier(FACE_MODEL)
    img = cv2.imread(filepath)
    faces = face_cascade.detectMultiScale(img, 1.1, 4)
    if len(faces):
        return True
    else:
        return False


def get_text(text):
    morph = MorphAnalyzer()
    text = re.sub(BAD_WORDS, ' ', text)
    tokens = [word.lower() for sent in sent_tokenize(text) for word in word_tokenize(sent)]
    filtered_tokens = []
    for token in tokens:
        token = token.strip()
        token = morph.normal_forms(token)[0]
        filtered_tokens.append(token)
    return filtered_tokens

def find_files():
    exclude_ext = [".txt", ".htm"]
    str1 = []
    folder = []

    for i in os.walk(ROOT_DIRECTORY):
        folder.append(i)

    for address, dirs, files in folder:
        for file in files:
            if os.path.splitext(file)[1] in exclude_ext:
                my_file = open(address + '/' + file, 'r')
                try:
                    my_string = my_file.read()
                    str1.append({'text': get_text(my_string), 'filepath': address + '/' + file})
                except Exception as e:
                    pass
                my_file.close()

    return str1
