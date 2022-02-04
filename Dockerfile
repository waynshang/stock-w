# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim as base
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

FROM base
ENV FLASK_ENV="docker"
ENV FLASK_APP=app.py
EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

RUN pip install gunicorn
RUN chmod 0700 gunicorn.sh

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["gunicorn", "--bind", "8000:8000", "app:app"]
ENTRYPOINT ["./gunicorn.sh"]
