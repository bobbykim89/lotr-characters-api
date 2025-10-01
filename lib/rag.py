from qdrant_client import QdrantClient
import requests
from openai import OpenAI
from dotenv import load_dotenv
import json
from pathlib import Path
from os import environ

load_dotenv()

class LotrCharactersRag:
    opanai_client: OpenAI
    qd_client: QdrantClient
    prompt_path: Path
    COLLECTION_NAME: str
    EMBEDDING_DIMENSION: int
    JINA_EMBEDDING_MODEL: str
    JINA_URL: str
    JINA_API_KEY: str
    QUERYING_TASK: str
    OPENAI_MODEL: str
    OPENAI_TEMPERATURE: float

    def __init__(self):
        self.opanai_client = OpenAI()
        QDRANT_URL = environ.get('QDRANT_CLOUD_URL')
        QDRANT_API_KEY = environ.get('QDRANT_API_KEY')
        self.qd_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        self.COLLECTION_NAME = "lotr-characters"
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent
        self.prompt_path = project_root / "lib" / "assets"
        self.JINA_URL = "https://api.jina.ai/v1/embeddings"
        self.JINA_API_KEY = environ.get('JINA_API_KEY')
        self.JINA_EMBEDDING_MODEL = "jina-embeddings-v4"
        self.EMBEDDING_DIMENSION = 512
        self.QUERYING_TASK = "retrieval.query"
        self.OPENAI_MODEL = "gpt-4o-mini"
        self.OPENAI_TEMPERATURE = 0.5
    
    def __get_jina_embedding(self, query: str)-> list:
        """
        Create embedding using Jina API
        Returns a single embedding vector (list of floats)
        """
        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {self.JINA_API_KEY}",
        }
        data = {
            "input": [query],
            "model": self.JINA_EMBEDDING_MODEL,
            "dimensions": self.EMBEDDING_DIMENSION,
            "task": self.QUERYING_TASK,
            "late_chunking": True,
        }
        try:
            res = requests.post(url=self.JINA_URL, headers=headers, json=data, timeout=30)
            if res.status_code == 200:
                embedding = res.json()["data"][0]["embedding"]
                return embedding
            else:
                raise Exception(f"Jina API error: {res.status_code} - {res.text}")
        except requests.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
        
    def __search(self, query: str, limit: int = 5):
        """
        Updated search function to use Jina API for query embedding
        """
        try:
            # Create embedding for the search query using Jina API
            query_embedding = self.__get_jina_embedding(query=query)

            query_points = self.qd_client.query_points(
                collection_name=self.COLLECTION_NAME,
                query=query_embedding,
                limit=limit,
                with_payload=True
            )
            results = [point.payload for point in query_points.points]

            return results
        except Exception as e:
            print(f"Error during search: {str(e)}")
            return None
    
    def __load_prompts(self)-> tuple[str,str]:
        """
        Load the txt files with the user|system prompts
        """
        user_prompt_path = self.prompt_path / "user_prompt.txt"
        system_prompt_path = self.prompt_path / "system_prompt.txt"
        with open(user_prompt_path, "r") as file:
            user_prompt = file.read()
        with open(system_prompt_path, "r") as file:
            system_prompt = file.read()
        return user_prompt, system_prompt
    
    def __format_prompt(self, query: str, search_results: list[dict[str,str]])-> tuple[str, str]:
        raw_user_prompt, system_prompt = self.__load_prompts()
        user_prompt = raw_user_prompt.format(retrieved_context=search_results, user_question=query).strip()
        return user_prompt, system_prompt
    
    def __format_hits_response(self, hits: list[dict[str, str|None]]):
        """
        Format the results into text to plug into chatGPT
        """
        character_data = []
        for hit in hits:
            basic_fields = ['race', 'gender', 'realm', 'culture', 'birth', 'death', 'spouse', 'hair', 'height', 'biography', 'history']
            character = {}
            character.update([(field, hit[field]) for field in basic_fields if hit.get(field)])
            character_data.append(character)
        
        return json.dumps(character_data, indent=2)
    
    def __llm(self, user_prompt: str, system_prompt: str)-> str:
        """
        llm function to call openAI with our specific prompts
        """
        res = self.opanai_client.chat.completions.create(
            model=self.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=self.OPENAI_TEMPERATURE
        )
        return res.choices[0].message.content
    
    def answer_lotr(self, query: str)-> str:
        hits = self.__search(query=query, limit=6)
        formatted_hits = self.__format_hits_response(hits=hits)
        user_prompt,system_prompt = self.__format_prompt(query=query, search_results=formatted_hits)
        res = self.__llm(user_prompt=user_prompt, system_prompt=system_prompt)
        return res