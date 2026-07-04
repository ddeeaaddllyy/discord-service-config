FROM python:3.11.9
WORKDIR /dckr

COPY requirements.txt .
RUN start start-config.bat
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "main.pyw"]
