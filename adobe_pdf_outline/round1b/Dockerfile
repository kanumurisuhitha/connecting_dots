FROM python:3.9-slim

WORKDIR /app

# Copy requirements first to use Docker cache effectively
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install CPU-only version of PyTorch first to avoid unnecessary CUDA downloads
RUN pip install torch==2.2.2+cpu -f https://download.pytorch.org/whl/torch_stable.html

# Install other dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Pre-download and cache the sentence-transformers model
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2').save('./cached_model')"

# Copy your source code
COPY src ./src

# CMD: Use the preloaded model from cached_model path in your Python code
CMD ["python", "./src/engine.py"]
