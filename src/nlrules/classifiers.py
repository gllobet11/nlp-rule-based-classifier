
import os
import time
import requests
from base import Classifier, Email
from .utils import norm, get_logger

log = get_logger(__name__)

def _env_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, default))
    except Exception:
        return default

def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, default))
    except Exception:
        return default

class ConditionClassifier(Classifier):
    def __init__(self, field: str, operator: str, value: str, category: str):
        self.field = field
        self.operator = operator
        self.value_raw = value
        self.value = norm(value)
        self.category = category.strip()

    def classify(self, email: Email):
        source_map = {
            "subject": email.subject or "",
            "body": email.body or "",
            "sender": email.sender or "",
        }
        text_raw = source_map.get(self.field, "")
        text = norm(text_raw)

        match = False
        if self.operator == "contains":
            match = self.value in text
        elif self.operator == "equals":
            match = self.value == text

        log.debug("Condition(%s %s %r) on [%s] -> %s",
                  self.field, self.operator, self.value_raw, text_raw, match)

        return self.category if match else None


class APIClassifier(Classifier):
    """
    Clasificador por defecto (Parte 1).
    Parametrizable vía variables de entorno:
      - DEFAULT_API_URL      (str)  ej: http://localhost:8000/classify-email
      - DEFAULT_API_TIMEOUT  (float segundos) ej: 6
      - DEFAULT_API_RETRIES  (int)  ej: 2
      - DEFAULT_API_BACKOFF  (float segundos base) ej: 0.4
    """
    def __init__(self, url: str | None = None, timeout: float | None = None,
                 retries: int | None = None, backoff_base: float | None = None):
        self.url = url or os.getenv("DEFAULT_API_URL", "http://localhost:8000/classify-email")
        self.timeout = timeout if timeout is not None else _env_float("DEFAULT_API_TIMEOUT", 6.0)
        self.retries = retries if retries is not None else _env_int("DEFAULT_API_RETRIES", 2)
        self.backoff_base = backoff_base if backoff_base is not None else _env_float("DEFAULT_API_BACKOFF", 0.4)

    def _post(self, payload: dict):
        # Reintentos con backoff exponencial simple
        last_exc = None
        for i in range(self.retries + 1):
            try:
                return requests.post(self.url, json=payload, timeout=self.timeout)
            except Exception as e:
                last_exc = e
                if i == self.retries:
                    break
                sleep_s = self.backoff_base * (2 ** i)
                log.debug("API retry %s/%s in %.2fs due to %r", i + 1, self.retries, sleep_s, e)
                time.sleep(sleep_s)
        raise last_exc

    def classify(self, email: Email):
        payload = {
            "client_id": email.client_id,
            "fecha_envio": email.fecha_envio.isoformat(),
            "email_body": email.body,
        }
        try:
            r = self._post(payload)
            r.raise_for_status()
            data = r.json()
            log.debug("API response: %s", data)

            # Contrato de tu API Parte 1:
            # - exito: bool
            # - prediccion: str (si exito True)
            if data.get("exito") is True:
                pred = data.get("prediccion")
                return pred.lower() if pred else None
            return None
        except Exception as e:
            log.debug("API classify error: %s", e)
            return None


class SequentialClassifier(Classifier):
    def __init__(self, classifiers):
        self.classifiers = classifiers

    def classify(self, email: Email):
        for c in self.classifiers:
            cat = c.classify(email)
            log.debug("Step %s -> %s", c.__class__.__name__, cat)
            if cat is not None:
                return cat
        return None
