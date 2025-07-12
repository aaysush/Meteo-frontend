FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use exec form for CMD with environment expansion via shell
ENTRYPOINT ["streamlit", "run"]
CMD ["page/page2.py", "--server.enableCORS=false", "--server.port=8501"]
