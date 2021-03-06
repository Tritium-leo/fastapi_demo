FROM 192.168.3.7:8081/fastapi_demo/builder

COPY . /app

RUN cd /app && pip install -r ./requirements.txt

WORKDIR /app

CMD ["gunicorn","main:app","-c","config/config.py"]