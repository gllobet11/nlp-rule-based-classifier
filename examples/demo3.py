# --- Bootstrap de paths para ejecutar ejemplos desde /examples ---
import os, sys
ROOT = os.path.dirname(os.path.dirname(__file__))   # carpeta raíz del repo
SRC  = os.path.join(ROOT, "src")                    # src/nlrules

# Añadir raíz (para importar base.py) y src (para importar nlrules/*)
sys.path.insert(0, SRC)
sys.path.insert(0, ROOT)

from datetime import datetime
from base import Email
from nlrules.parsing import NLConfigParserImpl
from nlrules.deserializer import ClassifierDeserializerImpl


parser = NLConfigParserImpl()
deserializer = ClassifierDeserializerImpl()

nl = """
Si el asunto contiene la palabra “urgente”, clasificarlo como “urgente”.
Si el cuerpo contiene la palabra “oferta”, clasifícalo como “promo”.
Si no, usar el clasificador por defecto.
"""

config = parser.parse(nl)
print("CONFIG:", config)

classifier = deserializer.deserialize(config)

email = Email(
    client_id=1,
    subject="Urgente: revisión",
    body="Hay una oferta nueva disponible",
    sender="ventas@gmail.com",
    fecha_envio=datetime.now()
)

print("RESULT:", classifier.classify(email))
