from typing import Dict
import requests
import os
import json

from Interfaces.IModel import IModel
from Interfaces.IModelResponse import IModelResponse


class Gemini (IModel):
    def prompt(self, prompt: str) -> IModelResponse:
        """
            Appelle l'API Gemini avec un prompt donné

            Args:
                prompt (str): Le texte à envoyer à Gemini

            Returns:
                Dict: Réponse JSON de l'API
        """
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        api_key = os.getenv('GEMINI_API_KEY')

        if not api_key:
            raise ValueError("Clé API manquante. Définissez GEMINI_API_KEY dans le fichier .env")

        headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': api_key
        }

        data = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        if self.first_prompt is not None:
            data["system_instruction"] = {
                "parts": [
                    {"text": self.first_prompt}
                ]
            }

        try:
            response = requests.post(url, headers=headers, json=data)

            response.raise_for_status()

            return GeminiResponse.build(response.json())

        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur lors de la requête : {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"Erreur lors du décodage JSON : {e}")

class GeminiResponse(IModelResponse):
    @staticmethod
    def build(response: any):
        geminiresponse: GeminiResponse = GeminiResponse()

        geminiresponse.raw = response
        if 'candidates' in response and response['candidates']:
            geminiresponse.result = response['candidates'][0]['content']['parts'][0]['text']

        return geminiresponse
