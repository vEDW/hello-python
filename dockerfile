FROM python:2
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY hello.py ./
EXPOSE 5000
CMD ["python","./hello.py"]
