FROM python:3.10.6
ADD app.py .
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python","/home/shady/app.py"]