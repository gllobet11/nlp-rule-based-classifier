from base import NaturalLanguageConfigParser, ClassifierDeserializer
from impl.parsing import NLConfigParserImpl
from impl.deserializer import ClassifierDeserializerImpl

def get_nl_config_parser() -> NaturalLanguageConfigParser:
    return NLConfigParserImpl()

def get_classifier_deserializer() -> ClassifierDeserializer:
    return ClassifierDeserializerImpl()
