FROM python:3.9

WORKDIR /usr/src/app

COPY backend/ .

RUN pip install pipenv && pipenv install --system --deploy

EXPOSE 8000

CMD ["pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]