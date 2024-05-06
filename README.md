# AI-Voice-Assistant
AI Voice Assistant for my final year project title 'Natural Language Generation'

This repository contains the source code for a voice-activated assistant built in Python. This assistant leverages several libraries, including OpenAI's Whisper and GPT models, to perform tasks like opening websites, taking screenshots, responding to user queries with spoken feedback, and much more.

Features

    Voice Commands: Interact with your computer using voice commands.
    Text-to-Speech: Converts text responses into audible speech.
    Task Automation: Perform tasks such as opening websites and applications, taking screenshots, etc.
    Real-time Interaction: Uses threading to handle real-time audio playback and command processing efficiently.

Configuration

Before running the assistant, you need to configure a few settings:

    Obtain an API key from OpenAI and set it in the code where the OpenAI client is initialized.
    Install required packages (see imports at the top of the assistant.py file)
    Ensure your audio device is properly set up and recognized by the speech_recognition library.
    Install Cuda toolkit to get the fastest transcription time possible.

Usage

To start the assistant, run the assistant.py file

Once running, the assistant listens for the wake word "nova" (this can be changed). Upon recognizing the wake word, it will process the following spoken commands and perform actions based on predefined commands. If the words following the wake word are not a command, it will prompt ChatGPT and generate a response.

Example Commands

    "nova open youtube" - Opens YouTube in the default web browser.
    "nova take a screenshot" - Takes a screenshot and saves it to the local directory.
    Additional commands can be added by modifying the listening() function.

Future Plans

    Add Spotify API for voice-controlled music playback.



    


License

This project is licensed under the MIT License - see the LICENSE file for details.
