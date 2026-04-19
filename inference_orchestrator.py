from base_model import ImageEmbedder
from vectors_storing import VectorsStoring

class InferenceOrchestrator:
    def __init__(self): 
        self.embedder = ImageEmbedder()
        self.storage = VectorsStoring(collection_name="positions_dataset")

    def search(self, image_path, limit=5): 
        vector = self.embedder.get_embedding(image_path)

        search_results = self.storage.client.query_points(
            collection_name=self.storage.collection_name,
            query=vector.tolist() if hasattr(vector, 'tolist') else vector,
            limit=limit
        ).points
        
        print(f"Search results for {image_path}: {search_results}")
        return search_results     