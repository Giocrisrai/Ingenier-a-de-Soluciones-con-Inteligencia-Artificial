# Frontend Streamlit — imagen slim, usuario no-root.
FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app_frontend.py ./

RUN useradd --create-home --uid 10002 appuser
USER appuser

EXPOSE 8501
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request,sys; urllib.request.urlopen('http://127.0.0.1:8501/_stcore/health'); sys.exit(0)" || exit 1

CMD ["streamlit", "run", "app_frontend.py", \
     "--server.port=8501", "--server.address=0.0.0.0", \
     "--server.headless=true", "--browser.gatherUsageStats=false"]
