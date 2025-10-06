
from base import Classifier
from impl.classifiers import ConditionClassifier, APIClassifier, SequentialClassifier

class ClassifierDeserializerImpl:
    def deserialize(self, config: dict) -> Classifier:
        rules = config.get("rules", [])
        classifiers = []
        for rule in rules:
            t = (rule.get("type") or "").lower()
            if t == "condition":
                classifiers.append(
                    ConditionClassifier(
                        field=rule["field"],
                        operator=rule["operator"],
                        value=rule["value"],
                        category=rule["category"],
                    )
                )
            elif t == "default":
                classifiers.append(APIClassifier())  # ← coge URL/timeout de ENV
        return SequentialClassifier(classifiers)
