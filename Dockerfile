FROM python:3.12-alpine

# Set the working directory to /app
WORKDIR /app

# Copy requirement and install then
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy rest of the files and run the app
COPY . .
CMD ["python", "main.py"]