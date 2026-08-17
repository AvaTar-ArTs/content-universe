FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN python -m pip install --no-cache-dir '.[mcp]'

VOLUME ["/data"]
ENTRYPOINT ["content-universe-mcp"]
CMD ["--db", "/data/content-universe.sqlite"]
