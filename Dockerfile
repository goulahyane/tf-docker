FROM continuumio/anaconda:4.4.0
COPY sentiment/ /usr/local/python/
EXPOSE 8180
WORKDIR /usr/local/python/
RUN pip install -r requirements.txt
CMD python sentiment_api.py 8180
