FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR ~/KeepInventory

COPY . ./app
RUN pip install --no-cache-dir -r ./app/requirements.txt

CMD ["python", "-m", "app"]