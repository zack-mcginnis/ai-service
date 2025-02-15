import uvicorn

if __name__ == "__main__":
    # Using host 0.0.0.0 is important for Docker
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 