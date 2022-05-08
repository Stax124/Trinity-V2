# Use alpine for smaller size
FROM python:3.10.4-alpine


# Main directory inside the container
WORKDIR /app

# Install dependencies
COPY requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt --no-cache-dir

# Copy the code
COPY cogs ./cogs
COPY core ./core
COPY main.py ./main.py

ENV TRINITY=${TRINITY_KEY}

CMD [ "python", "main.py" ]