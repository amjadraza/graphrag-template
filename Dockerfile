# Use the official Python image as the base image
FROM python:3.11.5-slim

# Set the working directory in the container
WORKDIR /home/appuser/app/

COPY requirements.txt /home/appuser/app/

# Copy the whole project to the container
COPY ./geo_tl_src/ /home/appuser/app/geo_tl_src
# Copy the whole project to the container
COPY .streamlit/ /home/appuser/app/.streamlit

# Install project dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

WORKDIR /home/appuser/app/

EXPOSE 80

# Specify the command to run your application with uvicorn

ENTRYPOINT ["streamlit", "run", "geo_tl_src/main.py", "--server.port=80"]