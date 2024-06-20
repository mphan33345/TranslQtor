# Imports
# PyQt5 Framework ~ QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QTextEdit
from PyQt5.QtGui import QFont, QFontDatabase
from languages import *
from googletrans import Translator
from gtts import gTTS
import speech_recognition as sr
import os

class TranslatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.click_events()
        self.deskey = None
        
        
    def settings(self):
        self.resize(500,400)
        self.setWindowTitle('TranslQtor')


    
    #Design
    def initUI(self):
        # All Widgets
        self.title = QLabel("TranslQtor")
        self.language1 = QComboBox()
        self.language2 = QComboBox()
        self.micbtn = QPushButton("🎤")
        self.switchbtn = QPushButton("🔄")
        self.speakbtn = QPushButton("🔊")
        self.language1.addItems(values)
        self.language2.addItems(values)
        self.box1 = QTextEdit()
        self.box1.setPlaceholderText("Input your text here...")
        self.box2 = QTextEdit()
        self.box2.setPlaceholderText("Translated text will output here.")
        self.translatebtn = QPushButton("Translate")
        self.resetbtn = QPushButton("Reset")
        
        # Create Layouts
        self.master_layout = QVBoxLayout()
        self.toprow = QHBoxLayout()
        self.textboxes = QHBoxLayout()
        self.bottomrow = QHBoxLayout()

        # Add widgets to Layouts
        self.master_layout.addWidget(self.title, alignment = Qt.AlignCenter)

        self.toprow.addWidget(self.language1)
        self.toprow.addWidget(self.micbtn, alignment = Qt.AlignCenter)
        self.toprow.addWidget(self.switchbtn, alignment = Qt.AlignCenter)
        self.toprow.addWidget(self.speakbtn, alignment = Qt.AlignCenter)
        self.toprow.addWidget(self.language2)

        self.textboxes.addWidget(self.box1)
        self.textboxes.addWidget(self.box2)

        self.bottomrow.addWidget(self.translatebtn)
        self.bottomrow.addWidget(self.resetbtn)

        self.master_layout.addLayout(self.toprow)
        self.master_layout.addLayout(self.textboxes)
        self.master_layout.addLayout(self.bottomrow)
        self.setLayout(self.master_layout)

        self.setStyleSheet("""
                                QWidget{
                                    background-color: #F1F8E8;
                                }

                                QLabel{
                                    color: #08332a;
                                    font-family: "Georgia", serif;
                                    font-size: 30px;
                                    font-weight: bold;
                                    padding: 5px;
                                }
                                QComboBox, QPushButton, QTextEdit{
                                    padding: 5px;
                                    background-color: #D8EFD3;
                                    font-family: "Verdana", sans-serif;
                                    border-radius: 5px;
                                }
                                """)

    #Events
    def click_events(self):
        self.resetbtn.clicked.connect(self.reset)
        self.translatebtn.clicked.connect(self.textonscreen)
        self.switchbtn.clicked.connect(self.reverse)
        self.speakbtn.clicked.connect(self.speak)
        self.micbtn.clicked.connect(self.speech_translate)
    # Google Translation
    def translation(self, text, x, y):
        speaker = Translator()
        translated = speaker.translate(text, dest=x, src=y)
        return translated.text
    # Take Translation & Put it on the Screen
    def textonscreen(self):
        try:
            source = self.language1.currentText()
            destination = self.language2.currentText()
            srckey = [key for key, value in LANGUAGES.items() if value == source] 
            self.destkey = [key for key, value in LANGUAGES.items() if value == destination] 

            self.script = self.translation(self.box1.toPlainText(), self.destkey[0], srckey[0])
            self.box2.setText(self.script)
        except Exception as e:
            print("Error:",e)
            self.box2.setText("You must enter text to translate...")
    # Switch the languages
    def reverse(self):
        temp1 = self.language1.currentText()
        temp2 = self.box1.toPlainText()
        self.language1.setCurrentText(self.language2.currentText())
        self.language2.setCurrentText(temp1)
        self.box1.setText(self.box2.toPlainText())
        self.box2.setText(temp2)
    # Reset the App
    def reset(self):
        self.box1.clear()
        self.box2.clear()
        self.language1.clear()
        self.language2.clear()
        self.language1.addItems(values)
        self.language2.addItems(values)
    # Recognize Speech
    def recognize_speech(self):#this doesnt work
        listener = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                audio = listener.listen(source, timeout=3)
                text = listener.recognize_google(audio)
                return text
            except Exception as e:
                print("Error:",e)
                self.box1.setText("Could not understand you...")
            
    # Listen and translate
    def speech_translate(self):#this doesnt work
        text = self.recognize_speech()
        if text:
            self.box1.setText(text)
            self.textonscreen()
            translatedtext = self.box2.toPlainText()

    # Read out the translated text
    def speak(self):
        try:
            text = self.box2.toPlainText()
            tts = gTTS(text, lang=self.destkey[0])
            tts.save("output.mp3")
            os.system("start output.mp3")
            print("test 1", self.destkey[0],self.box2.toPlainText())
        except Exception as e:
            print("Error:",e)

if __name__ == "__main__":
    app = QApplication([])
    window = TranslatorApp()
    window.show()
    app.exec_()