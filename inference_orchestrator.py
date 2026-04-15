from base_model import ImageEmbedder
from vectors_storing import VectorsStoring

class InferenceOrchestrator:
    def __init__(self): 
        self.embedder = ImageEmbedder()
        self.storage = VectorsStoring(collection_name="positions_dataset")

    def search(self, image_path, limit=5): 
        vector = self.embedder.get_embedding(image_path)

        search_results = self.storage.client.search(
            collection_name=self.storage.collection_name,
            query_vector=vector.tolist(),
            limit=limit
        )
        
        return search_results     