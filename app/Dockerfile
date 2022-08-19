FROM python:3.9-slim
RUN apt-get update
# RUN apt-get --assume-yes 
#--------------------------------------------------
# GitHub Action ignores WORKDIR, ENTRYPOINT and CMD
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd coda-cli
USER coda-cli

# Use CMD if you want to replace the default command, e.g Docker run coda-cli python coda.py --version
# Use ENTRYPOINT if you want to pass arguments to the default command, e.g. Docker run coda-cli --version 
ENTRYPOINT ["python3", "coda.py"]