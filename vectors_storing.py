from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

class VectorsStoring:
    def __init__(self, collection_name="positions_dataset"): 
        self.collection_name = collection_name

        self.client = QdrantClient(path="./qdrant_db")

    def upload_embeddings(self, embeddings_dicts, batch_size=10):
        vector_size = next(iter(embeddings_dicts.values())).shape[0]

        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        ) 

        points = []  
    
        for idx, (img_id, vector) in enumerate(embeddings_dicts.items(), start=1): 
            points.append(PointStruct( 
                id = idx, 
                vector = vector.tolist(),
                payload = {"name": img_id},
            )) 
    
        for i in range(0, len(points), batch_size): 
            self.client.upsert(
                collection_name=self.collection_name,
                points=points[i:i+batch_size]
            )

        print(f'Uploaded {len(points)} embeddings to Qdrant collection "{self.collection_name}".')