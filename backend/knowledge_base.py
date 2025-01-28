import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import json
from pathlib import Path


class KnowledgeBase:
    def __init__(self, data_path: str = "knowledge_data.json"):
        self.data_path = Path(data_path)
        self.knowledge = self._load_knowledge()
       
    def _load_knowledge(self) -> Dict:
        if self.data_path.exists():
            with open(self.data_path, 'r') as f:
                return json.load(f)
       
        return {
            "documents": [
                {
                    "content": """
                    Project X is a student-run technical community at VJTI Mumbai.
                    It focuses on fostering innovation and technical excellence among students.
                    The community organizes workshops, hackathons, and technical events.
                    Project X emphasizes peer learning and hands-on project development.
                    """,
                    "metadata": {"source": "core_info"}
                },
                {
                    "content": """
                    Community of Coders (CoC) is VJTI's official programming club.
                    CoC organizes coding competitions, workshops, and mentorship programs.
                    The club helps students improve their programming and development skills.
                    They conduct regular events to promote coding culture in VJTI.
                    """,
                    "metadata": {"source": "core_info"}
                }
            ]
        }
   
    def add_document(self, content: str, metadata: Dict = None):
        doc = {
            "content": content,
            "metadata": metadata or {}
        }
        self.knowledge["documents"].append(doc)
        self._save_knowledge()
   
    def _save_knowledge(self):
        with open(self.data_path, 'w') as f:
            json.dump(self.knowledge, f, indent=2)
   
    def search(self, query: str) -> List[str]:
       
        results = []
        query_terms = query.lower().split()
       
        for doc in self.knowledge["documents"]:
            content = doc["content"].lower()
            score = sum(1 for term in query_terms if term in content)
            if score > 0:
                results.append((score, doc["content"]))
       
     
        results.sort(reverse=True)
        return [content for _, content in results[:3]]