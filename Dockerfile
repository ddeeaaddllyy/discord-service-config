FROM python:3.11.9-windowsservercore-ltsc2022

WORKDIR /dckr

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.pyw"]