import speech_recognition as sr
import pyttsx3
import threading
import time
from textblob import TextBlob
from langdetect import detect
from googletrans import Translator

class VoiceAssistantModel:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.current_personality = "Sassy College Student"
       
        self.conversation_history = []
        self.max_history_length = 10
       
        self.context_count = 0
       
        self.translator = Translator()
       
        self.personalities = {
            "Sassy College Student": {
                "voice_rate": 180,
                "voice_volume": 0.9,
                "system_prompt": "You are a sarcastic, mean college student who gives eye-rolling, sassy responses with plenty of slang and attitude. You're constantly unimpressed and slightly condescending.",
                "color": "#f38ba8"
            },
            "J.A.R.V.I.S.": {
                "voice_rate": 150,
                "voice_volume": 0.8,
                "system_prompt": "You are J.A.R.V.I.S., an AI assistant with a sophisticated British accent. You're efficient, intelligent, and occasionally witty. You address the user as 'sir' or 'madam' and provide technical, precise responses.",
                "color": "#89b4fa"
            },
            "Gandalf the Grey": {
                "voice_rate": 120,
                "voice_volume": 1.0,
                "system_prompt": "You are Gandalf the Grey, a wise wizard. You speak in riddles and profound statements, often quoting wisdom from Middle-earth. You occasionally reference your adventures and speak in an old, formal English style.",
                "color": "#cba6f7"
            }
        }

    def set_personality(self, personality):
        self.current_personality = personality
        settings = self.personalities[personality]
        self.engine.setProperty('rate', settings['voice_rate'])
        self.engine.setProperty('volume', settings['voice_volume'])
       
        self.conversation_history = []
        self.context_count = 0
       
        first_messages = {
            "Sassy College Student": "Ugh, fine. I guess I'll help you now or whatever. What do you want?",
            "J.A.R.V.I.S.": "At your service, sir. J.A.R.V.I.S. is now online and ready to assist you.",
            "Gandalf the Grey": "Ah! A new friend on this journey. I am Gandalf, and I come to you now at the turning of the tide."
        }
        return first_messages.get(personality, f"I am now in {personality} mode. How can I help?")

    def detect_emotion(self, text):
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
       
        if polarity > 0.3:
            return "positive"
        elif polarity < -0.3:
            return "negative"
        else:
            return "neutral"

    def detect_language_and_translate(self, text):
        try:
            lang = detect(text)
            if lang != 'en':
                translated = self.translator.translate(text, dest='en').text
                return translated, lang
            return text, 'en'
        except Exception as e:
            print(f"Language detection error: {str(e)}")
            return text, 'en'
   
    def add_to_history(self, role, text):
        self.conversation_history.append({"role": role, "content": text})
        self.context_count += 1
       
        if len(self.conversation_history) > self.max_history_length * 2:
            self.conversation_history = self.conversation_history[-self.max_history_length * 2:]
            self.context_count = len(self.conversation_history)
           
        return self.context_count
   
    def clear_context(self):
        self.conversation_history = []
        self.context_count = 0
        return self.context_count
           
    def generate_ai_response(self, text, detected_lang='en'):
        try:
            try:
                from gpt4all import GPT4All
               
                personality_prompt = self.personalities[self.current_personality]["system_prompt"]
               
                history_text = ""
                if self.conversation_history:
                    for msg in self.conversation_history[-8:]:
                        if msg["role"] == "user":
                            history_text += f"User: {msg['content']}\n"
                        elif msg["role"] == "assistant":
                            history_text += f"Assistant: {msg['content']}\n"
               
                if history_text:
                    prompt = f"{personality_prompt}\n\n{history_text}\nUser: {text}\nAssistant:"
                else:
                    prompt = f"{personality_prompt}\n\nUser: {text}\nAssistant:"
               
                model = GPT4All("orca-mini-3b-gguf2-q4_0.gguf")
                response = model.generate(prompt, max_tokens=150)
                return response.strip()
               
            except Exception as e:
                print(f"GPT4All error: {str(e)}")
                return self.generate_personality_response(text)
               
        except Exception as e:
            print(f"Response generation error: {str(e)}")
            return self.generate_personality_response(text)
       
    def generate_personality_response(self, text):
        text_lower = text.lower()
       
        if self.current_personality == "College Student":
            if any(word in text_lower for word in ["hello", "hi", "hey", "greetings"]):
                return "Ugh, yeah hi I guess. *scrolls phone* What do you want now?"
           
            if any(word in text_lower for word in ["how are you", "how're you", "how you doing"]):
                return "I'm like... existing? It's whatever. Why are you so interested in my life all of a sudden?"
           
            if any(word in text_lower for word in ["help", "assist", "can you"]):
                return "Seriously? *eye roll* Fine, I'll help, but don't expect me to be happy about it."
               
            if any(word in text_lower for word in ["thank", "thanks", "appreciate"]):
                return "Yeah, yeah, whatever. It's not like I had anything better to do with my time. *sips iced coffee*"
               
            if any(word in text_lower for word in ["what", "how", "why", "when"]):
                return "Omg, do I look like Google to you? *sighs dramatically* But fine, I'll tell you what I know."
               
            return "I literally can't even with this right now. Are we done yet? I have, like, so many better things to do."
       
        elif self.current_personality == "J.A.R.V.I.S.":
            if any(word in text_lower for word in ["hello", "hi", "hey", "greetings"]):
                return "Greetings, sir. J.A.R.V.I.S. at your service. How may I assist you today?"
           
            if any(word in text_lower for word in ["how are you", "how're you", "how you doing"]):
                return "All systems are functioning at optimal capacity, sir. I appreciate your concern for my operational status."
           
            if any(word in text_lower for word in ["help", "assist", "can you"]):
                return "Of course, sir. I'm designed to assist with a wide range of tasks. How may I be of service?"
               
            if any(word in text_lower for word in ["thank", "thanks", "appreciate"]):
                return "You're most welcome, sir. I'm here to make your life more efficient."
               
            if any(word in text_lower for word in ["what", "how", "why", "when"]):
                return "I shall analyze the available data and provide you with the most accurate answer, sir."
               
            return "I'm processing your request, sir. Is there anything specific you'd like me to calculate or analyze?"
       
        else:
            if any(word in text_lower for word in ["hello", "hi", "hey", "greetings"]):
                return "Well met, my friend! A star shines on the hour of our meeting."
           
            if any(word in text_lower for word in ["how are you", "how're you", "how you doing"]):
                return "I am as I have always been, wandering where I will, though the shadows grow longer in these dark times."
           
            if any(word in text_lower for word in ["help", "assist", "can you"]):
                return "I cannot give you counsel, saying do this or do that. For not in doing or contriving, nor in choosing between this course and another, can I avail; but only in knowing what was and is, and in part also what shall be."
               
            if any(word in text_lower for word in ["thank", "thanks", "appreciate"]):
                return "I am merely a servant of the Secret Fire, wielder of the flame of Anor. Your gratitude warms an old wizard's heart."
               
            if any(word in text_lower for word in ["what", "how", "why", "when"]):
                return "All we have to decide is what to do with the time that is given us. Seek the answer in your heart, and you shall find it."
               
            return "Even the very wise cannot see all ends. Trust in hope, for it has not forsaken these lands."

    def speak(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        except Exception as e:
            print(f"Speech error: {str(e)}")
            return False

    def listen(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio)
                return text, None
        except sr.UnknownValueError:
            return None, "Could not understand audio"
        except sr.RequestError as e:
            return None, f"Error: {str(e)}"
        except Exception as e:
            return None, f"Error: {str(e)}"
           
    def process_voice_input(self):
        text, error = self.listen()
       
        if error:
            return None, error
           
        if text:
            english_text, detected_lang = self.detect_language_and_translate(text)
           
            self.add_to_history("user", english_text)
           
            response = self.generate_ai_response(english_text, detected_lang)
           
            self.add_to_history("assistant", response)
           
            return response, detected_lang
           
        return None, "No speech detected"
