FROM offline_chatbot:latest

#WORKDIR chatbot
COPY pdfs .
COPY utilities .
COPY .streamlit .
COPY chat.py .
COPY chatwithpdf.py .
COPY chat.spec .
COPY Dockerfile .
COPY README.md .
COPY Global.py .
COPY requirements.txt .

RUN apt update

#CMD [ "streamlit", "run", "chat.py"]
#RUN apt install sudo htop -y
#RUN apt install -y software-properties-common
#RUN add-apt-repository -y ppa:deadsnakes/ppa
#RUN apt update
#RUN apt install -y python3.10
#RUN sudo apt install -y python3-pip


# docker run -d -v ollama:/root/.ollama -p 11434:11434 --gpus all --name ollama offline_chatbot && docker exec -it ollama streamlit run chat.py


