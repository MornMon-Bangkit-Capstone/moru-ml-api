FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install fastapi==0.95.2 keras==2.11.0 pickle5==0.0.11 scikit-learn==1.2.1 sklearn==0.0.post1 tensorflow==2.11.1 uvicorn==0.22.0 nltk==4.64.0 numpy==1.23.1
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
