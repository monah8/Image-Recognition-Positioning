import nest_asyncio 
import uvicorn 
import threading 
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os 
import tempfile 
from base_model import ImagerEmbedder
from vectors_storing import VectorsStoring


class APIServer: 
    # nest_asyncio.apply() #applying nest_asyncio to allow nested event loops

    app = FastAPI() 

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True, 
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.post("/search")
    async def search_similar(
        file: UploadFile = File(...), 
        limit: int = 5 
    ): 

        with tempfile.NamedTemporaryFile(delete=False, sfx = '.jpg') as tmp_file: 
            tmp_file.write(await file.read()) 
            tmp_file_path = tmp_file.name

        try:  
            query_embedding = ImagerEmbedder.get_images_embedded(tmp_file_path)

            search_results = VectorsStoring.client.search(
                collection_name="product_images", 
                query_vector = query_embedding.tolist(), 
                limit = limit 
            ) 

            result = [] 
            for res in search_results: 
                result.append({
                    "image_path": res.payload["image_path"],
                    "name": res.payload["name"],
                    "score": res.score
                }) 
            
            return {"success": result}
        
        finally: 
            os.unlink(tmp_file_path) 

    def run_fastapi(host="127.0.0.1", port = 8000):
        server = uvicorn.Server(config = uvicorn.Config(app=app, host=host, port=port))

        thread = threading.Thread(target=server.run)
        thread.daemon = True 
        thread.start()

        print(f"FastAPI runnning on http://{host}:{port}")
        return thread
    
from IPython.display import display, HTML 
display(HTML('<a href = "http://127.0.0.1:8000/docs" target="_blank">Open FastAPI Swagger UI</a>'))


