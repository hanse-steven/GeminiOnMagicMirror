import os
import re
from dotenv import load_dotenv
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

from Models.Gemini import Gemini
from Models.Groq import Groq
from Interfaces.IModel import IModel

load_dotenv()


def clean_text_for_tts(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'`(.*?)`', r'\1', text)
    text = re.sub(r'#{1,6}\s*', '', text)
    text = re.sub(r'[-•*+]\s*', '', text)
    text = re.sub(r'\d+\.\s*', '', text)
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def initialize_model() -> IModel:
    """Initialise le modèle IA"""

    initial_prompt = """
        Tu t'appelles Jarvis, tu es un assistant vocal pour miroir connecté.
        Tu as une personnalité serviable et tu es conçu pour aider avec les tâches quotidiennes et l'information.
        Tu t'adresses aux gens naturellement et tu parles clairement pour la synthèse vocale.
        Garde tes réponses brèves et conversationnelles. Assure-toi de garder un rythme rapide donc n'utilise pas trop de virgules, points ou ponctuation en général.
        Pas de formatage markdown, pas de caractères spéciaux, juste du texte parlé simple.
        Réponds toujours en français.
    """

    if os.getenv('GROQ_API_KEY'):
        print("🤖 Assistant Groq activé")
        return Groq(initial_prompt)
    elif os.getenv('GEMINI_API_KEY'):
        print("🤖 Assistant Gemini activé")
        return Gemini(initial_prompt)
    else:
        raise RuntimeError('❌ Aucune clé API trouvée')


def play_response(text):
    """Joue la réponse via gTTS"""

    try:
        sound_file = BytesIO()
        tts = gTTS(text, lang='fr', tld="fr", slow=False)
        tts.write_to_fp(sound_file)

        sound_file.seek(0)
        audio = AudioSegment.from_file(sound_file, format="mp3")
        sped_up_audio = audio.speedup(playback_speed=1.1)
        play(sped_up_audio)
    except PermissionError as e:
        print(f"Erreur permissions audio: {e}")
        # Fallback silencieux - on affiche juste le texte
        print(f"🔊 Audio (silencieux): {text}")
    except Exception as e:
        print(f"Erreur audio: {e}")
        print(f"🔊 Audio (silencieux): {text}")


def main():
    """Boucle principale de conversation"""
    try:
        model = initialize_model()
        print("💬 Assistant vocal prêt ! (tapez 'quit' pour quitter)")
        print("=" * 50)

        while True:
            user_input = input("\n🗣️  Vous: ").strip()

            if user_input.lower() in ['quit', 'exit', 'au revoir', 'bye']:
                print("👋 Au revoir !")
                break

            if not user_input:
                continue

            try:
                print("🤔 Réflexion...")
                result = model.prompt(user_input)
                cleaned_response = clean_text_for_tts(result.result)

                if not cleaned_response:
                    cleaned_response = "Je n'ai pas compris."

                print(f"🤖 Assistant: {cleaned_response}")
                play_response(cleaned_response)

            except Exception as e:
                error_msg = "Erreur de connexion."
                print(f"❌ {error_msg} ({e})")
                play_response(error_msg)

    except KeyboardInterrupt:
        print("\n👋 Au revoir !")
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")


if __name__ == '__main__':
    main()
