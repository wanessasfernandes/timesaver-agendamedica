FROM python:3.12-slim 

ENV PYTHONDONTWRITEBYCODE=1 
ENV PYTHONUNBUFFERED=1 

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

RUN mkdir -p instance 

EXPOSE 5000 

CMD ["sh", "-c", "python seed.py && python run.py"]