from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from base_model import embeddings
from image_collector import image_paths, image_dir

class VectorsStoring:
    collection_name = "positions_dataset"

    def __init__(self, client=None):
        if not client:
            self.client = QdrantClient(path="./qdrant_data")
        else:
            self.client = client

    def upload_embeddings(self, embeddings, image_dir, batch_size=10):
        vector_size = next(iter(embeddings.values())).shape[0]

        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        ) 

        embedded_images = []
        current_id = 1  
    
        for img_id, embedding in embeddings.items(): 
            embedded_images.append(PointStruct( 
                id = current_id, 
                vector = embedding.tolist(),
                payload = {"image_path": str(image_dir / f"{img_id}.jpg"), "name": img_id},
            ))
            current_id += 1 
    
        for i in range(0, len(embedded_images), batch_size): 
            self.client.upsert(
                collection_name=self.collection_name,
                points=embedded_images[i:i+batch_size]
            )

        print(f'Uploaded {len(embedded_images)} embeddings to Qdrant collection "{self.collection_name}".')