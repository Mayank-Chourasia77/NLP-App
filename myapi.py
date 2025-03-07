import requests


class api:
    def __init__(self):
        self.api_key = "ba00f7a6ad8a1c83d3877c8a607bc442ac88a88a9fbbb54303a60e3c"
        self.endpoint = "http://api.textrazor.com/"
        self.last_result = None

    def analyze_text(self, text):
        headers = {"x-textrazor-key": self.api_key}
        data = {
            "text": text,
            "extractors": "entities,sentiment,relations",
            "cleanup.mode": "raw"
        }

        try:
            response = requests.post(self.endpoint, headers=headers, data=data)
            response.raise_for_status()
            self.last_result = response.json()
            return True
        except Exception as e:
            print(f"API Error: {str(e)}")
            self.last_result = None
            return False

    def get_entities(self):
        if not self.last_result or not self.last_result.get("ok"):
            return []

        entities = []
        for entity in self.last_result.get("response", {}).get("entities", []):
            # Safe extraction with fallbacks
            name = entity.get("entityEnglishId") or entity.get("matchedText", "Unknown Entity")
            entity_type = ", ".join(entity.get("type", ["Unknown Type"]))

            # Return as tuple (name, type)
            entities.append((name, entity_type))

        return entities

    def get_sentiment(self):
        if not self.last_result or not self.last_result.get("ok"):
            return "Unknown"

        # Handle missing sentiment data gracefully
        return self.last_result.get("response", {}).get("sentiment", {}).get("type", "Neutral")

    def get_relationships(self):
        if not self.last_result or not self.last_result.get("ok"):
            return []

        relations = []
        response_data = self.last_result.get("response", {})
        words = [word for sentence in response_data.get("sentences", [])
                 for word in sentence.get("words", [])]

        for relation in response_data.get("relations", []):
            subject = obj = predicate = "Unknown"
            for param in relation.get("params", []):
                if param.get("relation") == "SUBJECT":
                    subject = " ".join([words[pos]["token"] for pos in param.get("wordPositions", [])])
                elif param.get("relation") == "OBJECT":
                    obj = " ".join([words[pos]["token"] for pos in param.get("wordPositions", [])])
            relations.append(f"{subject} → {predicate} → {obj}")
        return relations