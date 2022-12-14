FROM python:3.10-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
# RUN apt install postgresql-dev
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]