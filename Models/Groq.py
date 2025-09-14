from typing import Dict
import requests
import os
import json

from Interfaces.IModel import IModel
from Interfaces.IModelResponse import IModelResponse


class Groq(IModel):
    def prompt(self, prompt: str) -> IModelResponse:
        """
            Appelle l'API Grok avec un prompt donné

            Args:
                prompt (str): Le texte à envoyer à Gemini

            Returns:
                Dict: Réponse JSON de l'API
        """
        url = "https://api.groq.com/openai/v1/chat/completions"
        api_key = os.getenv('GROQ_API_KEY')

        if not api_key:
            raise ValueError("Clé API manquante. Définissez GROQ_API_KEY dans le fichier .env")

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

        messages = []
        if self.first_prompt is not None:
            messages.append({
                "role": "system",
                "content": self.first_prompt
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        data = {
            "model": "openai/gpt-oss-20b",  # Nouveau modèle Groq
            "messages": messages,
            "temperature": 0.3,
            "top_p": 1,
            "stream": False,
            "reasoning_effort": "low",
            "stop": None
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return GroqResponse.build(response.json())

        except requests.exceptions.RequestException as e:
            raise Exception(f"Erreur lors de la requête Groq : {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"Erreur lors du décodage JSON : {e}")


class GroqResponse(IModelResponse):
    @staticmethod
    def build(response: any):
        groq_response: GroqResponse = GroqResponse()
        groq_response.raw = response

        if 'choices' in response and response['choices']:
            groq_response.result = response['choices'][0]['message']['content'].strip()

        return groq_response
