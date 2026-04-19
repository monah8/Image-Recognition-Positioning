import uvicorn 
import threading 
from fastapi import FastAPI, UploadFile, File, Request 
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os 
import tempfile 
from inference_orchestrator import InferenceOrchestrator
import requests

class APIServer: 
    def __init__(self): 
        self.app = FastAPI() 
        self.app.state.engine = InferenceOrchestrator()

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True, 
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        self.setup_routes()
    
    def setup_routes(self):

        @self.app.post("/locate")
        async def search_similar(
            request: Request,
            file: UploadFile = File(...), 
            limit: int = 5 
        ): 
            with tempfile.NamedTemporaryFile(delete=False, suffix = '.jpg') as tmp_file: 
                tmp_file.write(await file.read()) 
                tmp_file_path = tmp_file.name

            try:  
                # query_embedding = ImageEmbedder.get_images_embedded(tmp_file_path)
                search_results = request.app.state.engine.search(
                tmp_file_path, 
                limit = 1 
                ) 

                if not search_results:
                    return {"success": False, "error": "No results found"}
                
                best_match = search_results[0]
                matched_file_name = best_match.payload.get("name")+".jpg"

                dataset_dir = '/home/monah/Project-ComputerVision-AI/py_verse/data'
                full_image_path = os.path.join(dataset_dir, matched_file_name)

                try: 
                    r = requests.get(f"http://localhost:9000/coords/{matched_file_name}", timeout=2)
                    
                    if r.status_code == 200:
                        db_data = r.json()
                        return {"success": True, 
                                "match_score": float(best_match.score),
                                "matched_with": matched_file_name,
                                "coordinates": db_data.get("data")
                                  }
                
                    else:
                        return {"success": False,
                                "error": "Matched file not found", 
                                "matched_file": matched_file_name, 
                                }
                except requests.exceptions.RequestException:
                    return {"success": False, 
                            "error": "Failed to connect to Django API", 
                            } 
        
            finally: 
                if os.path.exists(tmp_file_path): 
                    os.unlink(tmp_file_path)

    def run_fastapi(self, host="0.0.0.0", port = 8000):
        config = uvicorn.Config(app=self.app, host=host, port=port)
        server = uvicorn.Server(config=config)
        thread = threading.Thread(target=server.run)
        thread.daemon = True 
        thread.start()
        print(f"FastAPI runnning on http://{host}:{port}")
        return thread

if __name__ == "__main__":  
    server = APIServer()
    fastapi_thread = server.run_fastapi()
    fastapi_thread.join()

# from IPython.display import display, HTML 
# display(HTML('<a href = "http://127.0.0.1:8000/docs" target="_blank">Open FastAPI Swagger UI</a>'))


