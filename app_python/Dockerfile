FROM python:3.13-slim
RUN useradd -m devopsuser
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER devopsuser
EXPOSE 5000
CMD ["python", "app.py"]
