FROM testproject/builder

COPY . /app

RUN cd /app && pip install -r ./requirements.txt

WORKDIR /app

CMD ["gunicorn","main:app","-c","config/config.py"]