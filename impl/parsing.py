
import re
from base import NaturalLanguageConfigParser
from impl.utils import norm, get_logger

# Acepta comillas rectas, tipográficas y simples
_QUOTE = r"['\"“”]"

log = get_logger(__name__)

class NLConfigParserImpl(NaturalLanguageConfigParser):
    def parse(self, natural_language: str) -> dict:
        raw = natural_language or ""
        text_norm = norm(raw)
        log.debug("NL raw: %s", raw)
        log.debug("NL normalized: %s", text_norm)

        field_map = {
            "asunto": "subject", "subject": "subject",
            "cuerpo": "body", "body": "body",
            "remitente": "sender", "from": "sender", "sender": "sender",
        }
        contains_tokens = {"contiene", "contains"}
        equals_tokens   = {"es", "is", "exactly"}

        # --- Patrones (sin DOTALL para no cruzar líneas) ---
        pat_rule_1 = re.compile(
            rf"(?:si|if)\s+(?:el|la|the)?\s*"
            rf"(asunto|subject|cuerpo|body|remitente|from|sender)"
            rf".*?"
            rf"(contiene|contains|es|is|exactly)"
            rf".*?{_QUOTE}([^'\"“”]+?){_QUOTE}"
            rf".*?"
            rf"(?:clasif(?:icar(?:lo)?|ícalo|icalo)\s+como|classif\w*\s+.*?as)"
            rf"\s+{_QUOTE}([^'\"“”]+?){_QUOTE}",
            re.IGNORECASE
        )

        # Variante A: "Asigna la categoría 'Y' si el <campo> es/contiene 'X'"
        pat_rule_2 = re.compile(
            rf"(?:asigna.*categor[ií]a|assign.*category)\s+{_QUOTE}([^'\"“”]+?){_QUOTE}"
            rf".*?(?:si|if)\s+(?:el|la|the)?\s*"
            rf"(asunto|subject|cuerpo|body|remitente|from|sender)"
            rf".*?(es|is|exactly|contiene|contains)\s+{_QUOTE}([^'\"“”]+?){_QUOTE}",
            re.IGNORECASE
        )

        # Variante B: "Si el <campo> es/contiene 'X', asigna la categoría 'Y'"
        pat_rule_2b = re.compile(
            rf"(?:si|if)\s+(?:el|la|the)?\s*"
            rf"(asunto|subject|cuerpo|body|remitente|from|sender)"
            rf".*?(es|is|exactly|contiene|contains)\s+{_QUOTE}([^'\"“”]+?){_QUOTE}"
            rf".*?(?:asigna.*categor[ií]a|assign.*category)\s+{_QUOTE}([^'\"“”]+?){_QUOTE}",
            re.IGNORECASE
        )

        rules = []
        seen = set()

        def add_rule(rule):
            key = (rule["type"], rule.get("field"), rule.get("operator"),
                rule.get("value"), rule.get("category"))
            if key not in seen:
                seen.add(key)
                rules.append(rule)
                log.debug("Parsed rule: %s", rule)

        # --- Analiza por frases, en este orden: pat_rule_2 -> pat_rule_2b -> pat_rule_1
        chunks = [c.strip() for c in re.split(r"(?:\n|;)+", raw) if c.strip()]

        for sent in chunks:
            # 2A) "Asigna la categoría ..."
            m2 = pat_rule_2.search(sent)
            if m2:
                category, field_raw, op_raw, value = m2.groups()
                field_key = norm(field_raw); op_key = norm(op_raw)
                field = field_map.get(field_key, "subject")
                operator = "contains" if op_key in contains_tokens else "equals"
                add_rule({"type":"condition","field":field,"operator":operator,
                        "value":value.strip(),"category":category.strip()})
                continue

            # 2B) "Si ... asigna la categoría ..."
            m2b = pat_rule_2b.search(sent)
            if m2b:
                field_raw, op_raw, value, category = m2b.groups()
                field_key = norm(field_raw); op_key = norm(op_raw)
                field = field_map.get(field_key, "subject")
                operator = "contains" if op_key in contains_tokens else "equals"
                add_rule({"type":"condition","field":field,"operator":operator,
                        "value":value.strip(),"category":category.strip()})
                continue

            # 2C) Regla directa "Si el <campo> ... clasificar(lo) como ..."
            m1 = pat_rule_1.search(sent)
            if m1:
                field_raw, op_raw, value, category = m1.groups()
                field_key = norm(field_raw); op_key = norm(op_raw)
                field = field_map.get(field_key, "subject")
                operator = "contains" if op_key in contains_tokens else "equals"
                add_rule({"type":"condition","field":field,"operator":operator,
                        "value":value.strip(),"category":category.strip()})

        # 3) Default (escaneo sobre el texto normalizado completo)
        default_triggers = [
            "si no, usar el clasificador por defecto",
            "regla por defecto",
            "usa siempre el clasificador por defecto",
            "if not, use the default classifier",
            "always use the default classifier",
        ]
        if any(t in text_norm for t in default_triggers):
            add_rule({"type": "default"})

        cfg = {"rules": rules}
        log.debug("Final JSON config: %s", cfg)
        return cfg
