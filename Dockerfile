FROM python:3.7.10-slim-stretch
COPY . /home/chakresh/{Projects}/Recipe_Recommendation_System
EXPOSE 5000
WORKDIR ./home/chakresh/{Projects}/Recipe_Recommendation_System
RUN pip install --default-timeout=100 -r requirements.txt
CMD python3 app.py
