import requests

from config import Config


class AIServiceError(Exception):
    """Yapay zekâ servisi hatalarını temsil eder."""


class AIService:
    """Groq yapay zekâ servisiyle iletişim kurar."""

    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = "llama-3.1-8b-instant"

    def _business_context(self):
        """İşletmeye özel sistem talimatını döndürür."""
        return Config.BUSINESS_CONTEXT

    def yanit_uret(self, mesaj, gecmis=None):
        """Kullanıcı mesajını Groq'a gönderir ve yanıtı döndürür."""
        if not self.api_key:
            raise AIServiceError("GROQ_API_KEY bulunamadı.")

        messages = [
            {
                "role": "system",
                "content": self._business_context(),
            }
        ]

        if gecmis:
            messages.extend(gecmis)

        messages.append(
            {
                "role": "user",
                "content": mesaj,
            }
        )

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.7,
                },
                timeout=30,
            )

            response.raise_for_status()

            data = response.json()

            return data["choices"][0]["message"]["content"]

        except requests.RequestException as exc:
            raise AIServiceError(
                "Yapay zekâ servisine bağlanırken hata oluştu."
            ) from exc

        except (KeyError, IndexError, TypeError) as exc:
            raise AIServiceError(
                "Yapay zekâ servisinden beklenmeyen yanıt geldi."
            ) from exc


ai_service = AIService()