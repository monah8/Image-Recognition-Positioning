from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import hashlib
import os

class VectorsStoring:
    def __init__(self, collection_name="positions_dataset"): 
        self.collection_name = collection_name

        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        qdrant_db_path = os.path.join(current_file_dir, "qdrant_db") 

        self.client = QdrantClient(path=qdrant_db_path)
        print(f"Initialized Qdrant client with local storage at: {qdrant_db_path}")
    def _generate_int_id(self, key):
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16) % (10 ** 8)
    
    def upload_embeddings(self, embeddings_dicts, batch_size=10):
        if not embeddings_dicts:
            return 
        
        first_item = next(iter(embeddings_dicts.values()))
        vector_size = first_item['vector'].shape[0]

        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        ) 

        points = []  
    
        for image_id, data in embeddings_dicts.items(): 
            points.append(PointStruct( 
                id = self._generate_int_id(image_id), 
                vector = data['vector'].tolist(),
                payload = data['payload'],
            )) 
    
        for i in range(0, len(points), batch_size): 
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )

        print(f'Uploaded {len(points)} embeddings to Qdrant collection "{self.collection_name}".')