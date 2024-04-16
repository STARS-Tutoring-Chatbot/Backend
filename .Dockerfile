FROM python:3.12-bullseye

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=10000

EXPOSE 10000

CMD [ "python3", "main.py" ]