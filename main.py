import json
from dotenv import load_dotenv

from Models.Gemini import Gemini
from Interfaces import IModel

load_dotenv()

if __name__ == '__main__':
    try:
        iamodel: IModel = Gemini()

        result = iamodel.prompt("Bonjour Gemini")

        #print(json.dumps(result.raw, indent=2, ensure_ascii=False))

        print(f"\nRéponse de Gemini : {result.result}")

    except Exception as e:
        print(f"Erreur : {e}")
