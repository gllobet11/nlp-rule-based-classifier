from datetime import datetime
from base import Email
from impl.parsing import NLConfigParserImpl
from impl.deserializer import ClassifierDeserializerImpl

def run():
    nl = """
    Si el remitente contiene la palabra "ventas", clasificarlo como "promo".
    Si el asunto es "Su teléfono está infectado", clasificarlo como "spam".
    Si no, usar el clasificador por defecto.
    """

    parser = NLConfigParserImpl()
    deser = ClassifierDeserializerImpl()

    config = parser.parse(nl)
    print("CONFIG:", config)
    clf = deser.deserialize(config)

    emails = [
        Email(client_id=1, subject="Hola", body="Info", sender="ventas@acme.com", fecha_envio=datetime.now()),
        Email(client_id=1, subject="Su teléfono está infectado", body="...", sender="alert@scam.com", fecha_envio=datetime.now()),
        # Este no matchea reglas => va a default. Si tu API devuelve exito=False para client_id=8, saldrá None
        Email(client_id=8, subject="Nada especial", body="Lorem", sender="user@mail.com", fecha_envio=datetime.now()),
    ]

    for i, e in enumerate(emails, 1):
        print(f"Email {i} ->", clf.classify(e))

if __name__ == "__main__":
    run()
