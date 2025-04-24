from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
from typing import List, Dict
import uuid
import os


class VectorDBManager:
    """
    A class to manage interactions with Pinecone and OpenAI for embedding-based searches and knowledge base management.

    Attributes:
    - pc (Pinecone): An instance of the Pinecone client for managing the index.
    - openai_api (OpenAI): An instance of OpenAI for generating text embeddings.
    - index_name (str): The name of the Pinecone index.
    - index (Pinecone.Index): The Pinecone index object for querying and upserting data.
    """
    
    def __init__(self, pinecone_api: str, openai_api: str, index_name: str, namespace: str=None):
        """
        Initializes the VectorDBManager with the provided Pinecone API key, OpenAI API key, and the desired index name.

        Args:
        - pinecone_api (str): The Pinecone API key.
        - openai_api (str): The OpenAI API key.
        - index_name (str): The name of the Pinecone index to be used.
        """
        self.pc = Pinecone(pinecone_api)
        self.index_name = index_name
        self.openai_api = OpenAI(api_key=openai_api)
        self.create_index_if_not_exists(index_name)
        self.index = self.pc.Index(index_name)
        self.namespace = namespace

    def search_kb(self, question: str, top_k: int = 1, filters: dict = None):
        """
        Searches the knowledge base for the most similar documents to the given question.

        Args:
        - question (str): The question to search for.
        - top_k (int, optional): The number of results to return. Defaults to 1.
        - filters (dict, optional): A dictionary of filters to narrow down the search. Defaults to None.

        Returns:
        - dict: The search results from Pinecone.
        """
        result = self.index.query(
            vector=self._get_embedding(question),
            top_k=top_k,
            filter=filters,
            include_values=False,
            include_metadata=True,
            namespace=self.namespace
        )
        return result

    def add_data(self, data: List[Dict]):
        """
        Adds the provided data to the Pinecone knowledge base.

        Args:
        - data (List[Dict]): A list of dictionaries, each containing "to_embedd" (the text to be embedded) and "metadata"
          (a dictionary of metadata for each document).

        Returns:
        - dict: The response from the Pinecone upsert operation.
        """
        to_insert = []

        for item in data:
            embedding = self._get_embedding(item["to_embedd"])
            metadata = item["metadata"]
            to_insert.append((str(uuid.uuid4()), embedding, metadata))

        print("VectorDBManager: Adding data to the index...", self.namespace)
        response = self.index.upsert(vectors=to_insert, namespace=self.namespace)
        return response

    def _get_embedding(self, text: str):
        """
        Retrieves the embedding of the given text from OpenAI.

        Args:
        - text (str): The text to embed.

        Returns:
        - list: The embedding of the text.

        Raises:
        - Exception: If there is an error during the embedding retrieval.
        """
        try:
            response = self.openai_api.embeddings.create(model=os.getenv("EMBEDDING_MODEL"), input=text)
            return response.data[0].embedding
        except Exception as e:
            print(f"Error getting embedding: {e}")
            raise

    def create_index_if_not_exists(self, index_name: str):
        """
        Creates a Pinecone index if it does not already exist.

        Args:
        - index_name (str): The name of the index to check or create.
        """
        print(f"Checking if Index with name '{index_name}' exists...")
        existing_indexes = self.pc.list_indexes()

        if index_name in [x["name"] for x in existing_indexes.to_dict()["indexes"]]:
            print(f"Index '{index_name}' already exists.")
            return
        
        self.pc.create_index(
            name=index_name,
            dimension=1536,  # Dependent on embedding model size (1536 for ada-002)
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
        print(f"Index '{index_name}' created")

    def delete_chunks_by_metadata(self, filter_condition: Dict):
        """
        Deletes chunks (documents) that match the given metadata filter condition.

        Args:
        - filter_condition (Dict): The filter condition to match documents to delete.

        Returns:
        - dict: A dictionary with the total count of deleted chunks.
        """
        print(f"Deleting chunks with metadata: {filter_condition}")
        
        try:
            dummy_vector = [0.0] * 1536  # Use your embedding dimension
            query_response = self.index.query(
                vector=dummy_vector,
                filter=filter_condition,
                top_k=10000,
                include_metadata=True,
                namespace=self.namespace
            )

            if not query_response.matches:
                print("No vectors found matching the filter criteria")
                return {"deleted": 0}

            vector_ids = [match.id for match in query_response.matches]
            print(f"Found {len(vector_ids)} vectors matching the filter")

            batch_size = 1000
            deleted_count = 0

            for i in range(0, len(vector_ids), batch_size):
                batch = vector_ids[i:i + batch_size]
                delete_response = self.index.delete(ids=batch, namespace=self.namespace)
                print("delete_response", delete_response)
                deleted_count += len(batch)
                print(f"Deleted batch of {len(batch)} vectors")

            result = {"deleted": deleted_count}
            print(f"Total chunks deleted: {deleted_count}")
            return result

        except Exception as e:
            print(f"Error during delete operation: {str(e)}")
            raise
