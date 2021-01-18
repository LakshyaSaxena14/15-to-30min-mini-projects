import pyttsx3
import PyPDF2
from os import path
import warnings

warnings.filterwarnings(action="ignore")

user_input = input("Enter the file name (Tip: enter the whole path of the file name): ")

if not path.isfile(user_input):
	print('Sorry the file does not exist, please check the file again. :(')


pdf_reader = PyPDF2.PdfFileReader(open(user_input, 'rb'))


def speak(audio):
	engine = pyttsx3.init('sapi5')
	voices = engine.getProperty('voices')
	try:
		engine.setProperty('voice', voices[1].id)
	except:
		engine.setProperty('voice', voices[0].id)

	engine.setProperty('rate', 165)
	engine.say(audio)
	engine.runAndWait()


for page in range(pdf_reader.numPages):
	text = pdf_reader.getPage(page).extractText()
	speak(text)

