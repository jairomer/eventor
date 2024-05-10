FROM python:3.12.3-alpine3.18

WORKDIR /app

COPY app /app
COPY requirements.txt /app/

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

RUN pip install -r requirements.txt
# Use dependencies installed for this user.
ENV PATH="${PATH}:/home/appuser/.local/bin"

EXPOSE 8000
#CMD ["uvicorn", "main:app", "--port=8000", "--host=0.0.0.0", "--app-dir", "/app"]
CMD ["fastapi", "run", "/app/main.py", "--proxy-headers", "--port", "8000"]
