# Offline Chatbot (Ollama + Streamlit)

This project demonstrates how to run and manage models locally using [Ollama](https://ollama.com/) by creating an interactive UI with [Streamlit](https://streamlit.io).

### Usage
To start the app, run the following command in your terminal:

```bash
conda activate ollama
python -m pip install -r requirements.txt
```


Chat with LLama:8b
```bash
streamlit run chat.py
```

Chat with PDf
```bash
streamlit run chatwithpdf.py
```


### Run with Docker 
Build image.
```bash
docker build -t offline_chatbot .
```
Run the following command;
```bash
docker run -d -p 11434:11434 --name ollama offline_chatbot:latest && docker exec -it ollama streamlit run chat.py
```
