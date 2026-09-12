FROM python:3.13.7-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY reservalab ./reservalab
COPY tests ./tests
COPY scripts ./scripts
RUN mkdir -p /app/data /app/evidence && useradd --uid 10001 --no-create-home app && chown -R app:app /app
USER app
EXPOSE 8000
CMD ["python", "-m", "reservalab", "--host", "0.0.0.0", "--port", "8000", "--db", "data/reservalab.db"]
