from datetime import datetime
from base import Email
from impl.parsing import NLConfigParserImpl
from impl.deserializer import ClassifierDeserializerImpl

def run():
    nl = """
    Si el cuerpo contiene la frase "devolución de recibo", clasificarlo como "impago".
    Si el cuerpo contiene la palabra "acceso al portal", clasificarlo como "acceso_portal".
    Si no, usar el clasificador por defecto.
    """

    parser = NLConfigParserImpl()
    deser = ClassifierDeserializerImpl()
    cfg = parser.parse(nl)
    print("CONFIG:", cfg)
    clf = deser.deserialize(cfg)

    emails = [
        Email(client_id=1, subject="Urgente", body="Notificación de devolución de recibo de banco", sender="cliente@dominio.com", fecha_envio=datetime.now()),
        Email(client_id=1, subject="No puedo entrar", body="Problema con acceso al portal de clientes", sender="user@dominio.com", fecha_envio=datetime.now()),
        Email(client_id=8, subject="Consulta general", body="Texto neutro", sender="alguien@dominio.com", fecha_envio=datetime.now()),
    ]

    for i, e in enumerate(emails, 1):
        print(f"Email {i} ->", clf.classify(e))

if __name__ == "__main__":
    run()
