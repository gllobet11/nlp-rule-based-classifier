import logging
import os
import unicodedata

def norm(s: str) -> str:
    """
    Normaliza texto: lower, strip, sin tildes (NFKD) y comillas tipográficas → rectas.
    No quita caracteres internos importantes para equals/contains.
    """
    if s is None:
        return ""
    s = s.replace("“", "\"").replace("”", "\"").replace("’", "'")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))  # quita acentos
    return s.strip().lower()

def get_logger(name: str) -> logging.Logger:
    """
    Logger que se activa con:
    - DEBUG_PART4=1  → nivel DEBUG
    - DEBUG_PART4=0  → nivel WARNING (por defecto)
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # ya configurado

    level = logging.DEBUG if os.getenv("DEBUG_PART4") == "1" else logging.WARNING
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    fmt = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
    ch.setFormatter(fmt)
    logger.addHandler(ch)
    return logger
