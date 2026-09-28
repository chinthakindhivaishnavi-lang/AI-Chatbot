import json
import re
import math
from collections import Counter


class Chatbot:
    def __init__(self, data_file):
        self.data = self.load_data(data_file)

    def load_data(self, data_file):
        with open(data_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def clean_text(self, text):
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        return text.split()

    def cosine_similarity(self, text1, text2):
        words1 = self.clean_text(text1)
        words2 = self.clean_text(text2)

        if not words1 or not words2:
            return 0

        counter1 = Counter(words1)
        counter2 = Counter(words2)

        all_words = set(counter1.keys()).union(counter2.keys())

        vector1 = [counter1[word] for word in all_words]
        vector2 = [counter2[word] for word in all_words]

        dot_product = sum(
            a * b for a, b in zip(vector1, vector2)
        )

        magnitude1 = math.sqrt(
            sum(a * a for a in vector1)
        )

        magnitude2 = math.sqrt(
            sum(b * b for b in vector2)
        )

        if magnitude1 == 0 or magnitude2 == 0:
            return 0

        return dot_product / (magnitude1 * magnitude2)

    def get_response(self, user_input):
        best_score = 0
        best_answer = None

        for item in self.data:
            score = self.cosine_similarity(
                user_input,
                item["question"]
            )

            if score > best_score:
                best_score = score
                best_answer = item["answer"]

        # Minimum similarity required
        if best_score >= 0.25:
            return best_answer

        return (
            "Sorry, I don't have an answer for that question yet. "
            "Please try asking something related to our services, "
            "courses or support."
        )