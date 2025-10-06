from datetime import datetime
from base import Email
from impl.parsing import NLConfigParserImpl
from impl.deserializer import ClassifierDeserializerImpl

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
