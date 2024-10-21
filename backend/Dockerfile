# Usa una imagen base de Python
FROM python:3.9


WORKDIR /api


COPY requirements.txt ./


RUN pip install --no-cache-dir -r requirements.txt


COPY . .
EXPOSE 8021

# Comando para ejecutar tu aplicación
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8021"]
 