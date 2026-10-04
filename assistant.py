import gradio as gr
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import tempfile
import os
import time
import webbrowser

def process_audio(audio_path):
    if not audio_path:
        return "No audio provided", None

    recognizer = sr.Recognizer()
    try:
        # Load the audio file that Gradio saved from the microphone
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
        # Recognize speech
        query = recognizer.recognize_google(audio, language='en-in').lower()
    except sr.UnknownValueError:
        return "Could not understand audio. Please try again.", None
    except Exception as e:
        return f"Error recognizing audio: {str(e)}", None

    response_text = ""

    # Process Commands
    if 'time' in query:
        strTime = datetime.datetime.now().strftime("%I:%M %p")
        response_text = f"The time is {strTime}"
        
    elif 'open google' in query:
        response_text = "Opening Google in the server's browser."
        webbrowser.open("https://google.com")
        
    elif 'open youtube' in query:
        response_text = "Opening YouTube in the server's browser."
        webbrowser.open("https://youtube.com")
        
    elif 'open' in query:
        website = query.replace('open', '').strip()
        response_text = f"Opening {website} in the server's browser."
        url = f"https://www.{website.replace(' ', '')}.com"
        webbrowser.open(url)
        
    elif 'wikipedia' in query or 'who is' in query or 'what is' in query:
        search_query = query.replace("wikipedia", "").replace("who is", "").replace("what is", "")
        try:
            results = wikipedia.summary(search_query, sentences=2)
            response_text = f"According to Wikipedia: {results}"
        except wikipedia.exceptions.DisambiguationError:
            response_text = "There are multiple results for this. Please be more specific."
        except Exception:
            response_text = "I couldn't find any results for that on Wikipedia."
            
    elif 'exit' in query or 'stop' in query or 'quit' in query or 'bye' in query:
        response_text = "Goodbye! Have a great day."
    else:
        response_text = f"You said: '{query}'. I don't have a specific command for this."

    # Convert response_text to audio using pyttsx3
    engine = pyttsx3.init()
    # Ensure temporary file is created safely
    output_audio_path = os.path.join(tempfile.gettempdir(), f"output_{int(time.time())}.wav")
    engine.save_to_file(response_text, output_audio_path)
    engine.runAndWait()

    return response_text, output_audio_path

# Build the Gradio Web Interface
with gr.Blocks() as demo:
    gr.Markdown("# 🎙️ Python Voice Assistant Web App")
    gr.Markdown("Speak into your microphone and submit to interact with the assistant.")
    
    with gr.Row():
        audio_input = gr.Audio(sources=["microphone"], type="filepath", label="Your Voice Input")
        
    with gr.Row():
        text_output = gr.Textbox(label="Assistant Text Response")
        audio_output = gr.Audio(label="Assistant Voice Response")
    
    btn = gr.Button("Submit", variant="primary")
    
    # When button is clicked, send audio input to function and output text and audio
    btn.click(fn=process_audio, inputs=audio_input, outputs=[text_output, audio_output])

if __name__ == "__main__":
    # share=True creates a public web URL (e.g., https://xxxxx.gradio.live)
    demo.launch(share=True)
