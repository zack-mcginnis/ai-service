import uvicorn
import multiprocessing

if __name__ == "__main__":
    # Number of worker processes = CPU cores
    workers = multiprocessing.cpu_count()
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=workers,        # One worker per CPU core
        loop="uvloop",         # Faster event loop implementation
        limit_concurrency=1000 # Max concurrent connections
    ) 