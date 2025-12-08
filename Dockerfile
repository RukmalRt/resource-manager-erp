# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port for Azure Container Apps
EXPOSE 8080

# Streamlit run command
CMD ["streamlit", "run", "Dashboard.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.headless=true"]
