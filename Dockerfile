FROM python:2.7

RUN pip install --upgrade pip && \
    pip install flask

ENV FLASK_APP /root/fl.py

# Ideally some installation method should be used
ADD fl.py /root/fl.py

CMD ["flask", "run", "--port=80", "--host=0.0.0.0"]

EXPOSE 80
