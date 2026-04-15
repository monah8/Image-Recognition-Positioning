import uvicorn 
import threading 
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os 
import tempfile 
from inference_orchestrator import InferenceOrchestrator

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

        @self.app.post("/search")
        async def search_similar(
            file: UploadFile = File(...), 
            limit: int = 5 
        ): 
            with tempfile.NamedTemporaryFile(delete=False, suffix = '.jpg') as tmp_file: 
                tmp_file.write(await file.read()) 
                tmp_file_path = tmp_file.name

            try:  
                # query_embedding = ImageEmbedder.get_images_embedded(tmp_file_path)
                search_results = self.engine.search(
                tmp_file_path, 
                limit = limit 
                ) 
                result = [] 
                for res in search_results: 
                    result.append({
                        # "image_path": res.payload["image_path"],
                        "name": res.payload["name"],
                        "score": res.score
                    }) 
                return {"success": result}
        
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


