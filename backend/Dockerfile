FROM python:3.9-slim

WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create directory for temporary PDFs
RUN mkdir -p temp_pdfs && chmod 777 temp_pdfs

# Set environment variables
ENV PORT=8080

# Command to run the application
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT}
