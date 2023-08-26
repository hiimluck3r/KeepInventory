FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR ~/KeepInventory

COPY . ./bot
RUN pip install --no-cache-dir -r ./bot/requirements.txt

CMD ["python", "-m", "bot"]