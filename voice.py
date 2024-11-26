import streamlit as st
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import io

# Step 2: Define the language and speech recognition function
def language_code(language):
    if language == "Français":
        return "fr"
    elif language == "Anglais":
        return "en"
    elif language == "Espagnol":
        return "es"
    else:
        return "en"  # Par défaut, utiliser l'anglais

def transcribe_speech(api_choice, language, pause_and_resume):
    # Initialisation de la classe de reconnaissance
    r = sr.Recognizer()

    # Si la mise en pause est activée, ne pas écouter
    if pause_and_resume:
        st.info("Enregistrement en pause..")
        return "Enregistrement en pause"

    try:
        # Enregistrement de l'audio avec sounddevice
        st.info("Enregistrement en cours...")
        fs = 16000  # Fréquence d'échantillonnage (16kHz)
        duration = 10  # Durée de l'enregistrement en secondes
        audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()  # Attendre que l'enregistrement soit terminé

        # Convertir l'audio en fichier audio de type WAV
        audio_file = io.BytesIO()
        audio_data_bytes = np.array(audio_data, dtype=np.int16).tobytes()
        audio_file.write(audio_data_bytes)
        audio_file.seek(0)

        # Utiliser l'API de reconnaissance vocale
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)

        # Transcription avec l'API sélectionnée
        if api_choice == "Google":
            return r.recognize_google(audio, language=language_code(language))
        elif api_choice == "Sphinx":
            return r.recognize_sphinx(audio)
        elif api_choice == "Bing Speech (Azure)":
            st.warning("Intégration Bing/Azure Speech API à configurer")
            return "API Bing/Azure Speech non encore implémentée"
        else:
            return "API non reconnue"

    except Exception as e:
        return f"Erreur pendant l'enregistrement ou la transcription : {str(e)}"

# Step 3: Define the main function
def main():
    st.title("Speech Recognition App")
    st.write("Cliquez sur le microphone pour commencer à parler:")

    # Ajouter une option de sélection d'API
    api_choice = st.selectbox(
        "Choisissez l'API de reconnaissance vocale :",
        ("Google", "Sphinx", "Bing Speech (Azure)"))

    # Ajouter une option de sélection de langue
    language = st.selectbox("Choisissez la langue :",
                            ("Français", "Anglais", "Espagnol"))

    # Mettre en pause et de reprendre le processus de reconnaissance vocale
    pause_and_resume = st.checkbox("Mettre en pause et reprendre le processus")

    # Ajouter un bouton pour déclencher la reconnaissance vocale
    if st.button("Start Recording"):
        text = transcribe_speech(api_choice, language, pause_and_resume)
        st.write("Transcription : ", text)

        # Ajouter un bouton pour enregistrer le texte dans un fichier
        if st.button("Enregistrer la Transcription"):
            with open("Transcription.txt", "w") as file:
                file.write(text)
            st.success("Transcription enregistrée dans transcription.txt")

    # Ajouter des boutons pour mettre en pause et reprendre l'enregistrement
    if pause_and_resume:
        if st.button("Mettre en pause"):
            pause_and_resume = False
        if st.button("Reprendre"):
            pause_and_resume = True

if __name__ == "__main__":
    main()
