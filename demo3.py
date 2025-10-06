from datetime import datetime
from base import Email
from impl.parsing import NLConfigParserImpl
from impl.deserializer import ClassifierDeserializerImpl

def run():
    nl = """
    Asigna la categoría "regulatorio" si el remitente es "inspecciones@cnmc.es".
    Si el asunto contiene la palabra "reclamación", clasificarlo como "reclamacion".
    If the body contains the word "avería", classify it as "incidencia".
    """

    parser = NLConfigParserImpl()
    deser = ClassifierDeserializerImpl()
    cfg = parser.parse(nl)
    print("CONFIG:", cfg)
    clf = deser.deserialize(cfg)

    emails = [
        Email(client_id=1, subject="Revisión de punto de medida", body="...", sender="inspecciones@cnmc.es", fecha_envio=datetime.now()),
        Email(client_id=1, subject="Reclamación por facturación", body="Adjunto detalle", sender="cliente@dominio.com", fecha_envio=datetime.now()),
        Email(client_id=1, subject="Consulta", body="Detectamos una avería en el contador", sender="soporte@dominio.com", fecha_envio=datetime.now()),
        Email(client_id=1, subject="Consulta normal", body="Nada relevante", sender="cliente@dominio.com", fecha_envio=datetime.now()),
    ]

    for i, e in enumerate(emails, 1):
        print(f"Email {i} ->", clf.classify(e))


    # Sanity checks rápidos
    assert clf.classify(emails[0]) == "regulatorio", "Email 1 debería ser 'regulatorio'"
    assert clf.classify(emails[1]) == "reclamacion", "Email 2 debería ser 'reclamacion'"
    assert clf.classify(emails[2]) == "incidencia",  "Email 3 debería ser 'incidencia'"
    assert clf.classify(emails[3]) is None,          "Email 4 debería ser None"
    print("✔ Sanity checks OK")

if __name__ == "__main__":
    run()
