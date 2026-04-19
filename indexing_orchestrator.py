from base_model import ImageEmbedder
from vectors_storing import VectorsStoring
import os
from tqdm import tqdm
import sys

print(f"--- DIAGNOSTICS ---")
print(f"Current Working Directory: {os.getcwd()}")
print(f"Script Location: {os.path.abspath(__file__)}")
print(f"Python Executable: {sys.executable}")
print(f"--- --- ---")

class IndexingOrchestrator:
    def __init__(self):

        # Выходим на уровень выше 
        self.curr_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_project_dir = os.path.dirname(self.curr_dir)
        
        # Пути к джанго 
        self.django_dir = os.path.join(self.base_project_dir, 'Image-Recognition-Postioning-DB-main')
        self.db_path = os.path.join(self.django_dir, "db.sqlite3")
        self.media_dir = os.path.join(self.django_dir, "media")

        # Инициализация компонентов ядра
        self.embedder = ImageEmbedder()
        self.storage = VectorsStoring(collection_name="positions_dataset")

    def get_django_photos(self):
        sql_lib = __import__('sqlite3')

        if not os.path.exists(self.media_dir):
            print(f'Media not found in {self.db_path}')

        try:
            conn = sql_lib.connect(self.db_path)
            cursor = conn.cursor() 
            
            cursor.execute("SELECT image FROM core_referencephoto")
            
            paths = [row[0] for row in cursor.fetchall()]
            conn.close()
            return paths
        
        except Exception as e:
            print(f"Error reading tables: {e}")
            return []

    def run_full_indexing(self): 
        # сбор путей к изображениям
        relative_paths = self.get_django_photos()

        if not relative_paths:
            print("No photos found in the database.")
            return

        all_embeddings = {}

        print(f'Found in Django DB: {len(relative_paths)}')
        print('Generating embeddings for all images...')

        for rel_path in tqdm(relative_paths, desc="Processing images"):
            full_path = os.path.join(self.media_dir, rel_path)
            
            if not os.path.exists(full_path):
                print(f'File not found: {full_path}')
                continue
            
            try: 
                img_id = os.path.basename(rel_path).split('.')[0]  

                vector = self.embedder.get_embedding(full_path)

                all_embeddings[img_id] = {"vector" : vector, 
                                         "payload" : {"name": img_id}
                                        }

            except Exception as e:
                print(f'Error processing {img_id}: {e}')

        self.storage.upload_embeddings(all_embeddings)
    
        print(f'Successfully processed: {len(all_embeddings)})') 
        return all_embeddings
    
if __name__ == "__main__":
    orchestrator = IndexingOrchestrator()
    orchestrator.run_full_indexing()