FROM python:3.11

WORKDIR /working

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python"]