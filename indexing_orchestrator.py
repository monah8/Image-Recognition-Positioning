import image_collector
from base_model import ImageEmbedder
from vectors_storing import VectorsStoring
import os
from tqdm import tqdm

class IndexingOrchestrator:
    def __init__(self):
        self.data_dir = '/home/monah/Project-ComputerVision-AI/py_verse/data'
        self.embedder = ImageEmbedder()
        self.storage = VectorsStoring(collection_name="positions_dataset")

    def run_full_indexing(self): 
        # сбор путей к изображениям
        paths = image_collector.get_all_images()

        all_embeddings = {}

        print('Generating embeddings for all images...')

        for path in tqdm(paths, desc="Processing images"):
            try: 
                img_id = os.path.basename(path).split('.')[0]  

                vector = self.embedder.get_embedding(path)

                all_embeddings[img_id] = vector

            except Exception as e:
                print(f'Error processing {path}: {e}')

        self.storage.upload_embeddings(all_embeddings)
    
        print(f'Успешно обработано: {len(all_embeddings)})') 
        return all_embeddings
    
if __name__ == "__main__":
    orchestrator = IndexingOrchestrator()
    orchestrator.run_full_indexing()