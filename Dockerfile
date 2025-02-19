# Dockerfile.streamlit

# Use the same Python base image for consistency
FROM python:3.12-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the Streamlit app file (and any other files it might need)
COPY streamlit_app.py .

# Expose port 8501 (default for Streamlit)
EXPOSE 8501

# Run the Streamlit app. The flag disables CORS if you’re calling APIs from other containers.
CMD ["streamlit", "run", "streamlit_app.py", "--server.enableCORS", "false", "--server.port", "8501"]
