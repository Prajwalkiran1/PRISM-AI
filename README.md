# PRISM AI Voice Assistant

PRISM AI is an advanced desktop voice assistant with customizable AI personalities and multi-language support. Built with Python and CustomTkinter for a modern, responsive UI.

![PRISM AI Interface]

## Features

- **Multiple AI Personalities**: Switch between different assistant personas like "Sassy College Student," "J.A.R.V.I.S.," and "Gandalf the Grey"
- **Voice Recognition**: Hands-free interaction through speech recognition
- **Text-to-Speech**: Listen to AI responses with voice synthesis
- **Multi-language Support**: Automatic language detection and translation
- **Sentiment Analysis**: Detects emotion in user messages
- **Modern UI**: Sleek, customizable dark-themed interface
- **Conversation History**: Maintains context for more natural interactions
- **Real-time Animation**: Visual feedback during voice recording and processing

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Prajwalkiran1/prism-ai.git
cd prism-ai
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Dependencies

- customtkinter
- speech_recognition
- pyttsx3
- textblob
- langdetect
- googletrans==4.0.0-rc1
- pillow
- gpt4all 

## Project Structure

- `voice_assistant_ui.py`: Main UI implementation with CustomTkinter
- `voice_assistant_model.py`: Core functionality for speech processing and AI responses
- `main.py`: Entry point that launches the application

## Usage

### Text Input
1. Type your message in the input field
2. Press Enter or click the Send button
3. View the AI's response in the chat window

### Voice Input
1. Click the microphone button to start listening
2. Speak your message clearly
3. The assistant will process your speech, respond in text, and read the response aloud
4. Click the stop button to end the listening session

### Personality Selection
Use the dropdown menu in the header to switch between different AI personalities:
- **Sassy College Student**: Casual, sarcastic responses with attitude
- **J.A.R.V.I.S.**: Formal, technical assistant inspired by Iron Man's AI
- **Gandalf the Grey**: Wise, philosophical responses with a fantasy flair

### Additional Controls
- **Clear Context**: Erases conversation memory while maintaining chat history
- **Clear Chat**: Wipes the chat display but retains context memory

## Customization

### Adding New Personalities
Modify the `personalities` dictionary in `voice_assistant_model.py` to add new personalities:

```python
self.personalities = {
    "New Personality": {
        "voice_rate": 150,
        "voice_volume": 0.8,
        "system_prompt": "Your system prompt here",
        "color": "#HEX_COLOR_CODE"
    },
    # Other personalities...
}
```

### UI Customization
The color scheme can be modified in the `colors` dictionary in `voice_assistant_ui.py`.

## Offline LLM Support

The assistant attempts to use the GPT4All library with the "orca-mini-3b-gguf2-q4_0.gguf" model for enhanced responses. If unavailable, it falls back to pre-defined responses based on the current personality.

To enable advanced AI responses:
1. Install GPT4All: `pip install gpt4all`
2. Download the model file (it will be downloaded automatically on first use)


## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

- CustomTkinter for the modern UI components
- Speech Recognition libraries for voice processing capabilities
- GPT4All for local language model inference
