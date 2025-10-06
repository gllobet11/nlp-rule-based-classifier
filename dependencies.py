import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from base import NaturalLanguageConfigParser, ClassifierDeserializer
from nlrules.parsing import NLConfigParserImpl
from nlrules.deserializer import ClassifierDeserializerImpl


def get_nl_config_parser() -> NaturalLanguageConfigParser:
    return NLConfigParserImpl()


def get_classifier_deserializer() -> ClassifierDeserializer:
    return ClassifierDeserializerImpl()
