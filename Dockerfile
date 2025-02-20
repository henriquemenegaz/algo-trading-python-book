# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10.16-bookworm
# A versão 3.10 do pytho é compatível com o openbb.


# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN pip install --upgrade pip && \
    python -m pip install -r requirements.txt

EXPOSE 6900

WORKDIR /code
COPY ./src ./src

ENTRYPOINT ["openbb-api", "--host", "0.0.0.0", "--login"]

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
#CMD ["python", "src\main.py"]
