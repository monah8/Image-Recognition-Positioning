from base_model import ImageEmbedder, embeddings
from vectors_storing import VectorsStoring
from api_finder import APIServer
from image_collector import image_paths, image_dir 

def run_pipeline(): 
    collection = VectorsStoring()
    paths = image_paths

    embedder = ImageEmbedder() 
    embeddings = [embedder.get_images_embedded(path) for path in paths]

    db = VectorsStoring()
    db.upload_embeddings(embeddings, image_dir)

if __name__ == "__main__": 
    run_pipeline() 
    APIServer.run_fastapi()