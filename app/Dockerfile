FROM python:3.9.6

WORKDIR .

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001"]
