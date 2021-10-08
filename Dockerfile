FROM python:3.8

RUN mkdir /bot

RUN chown -R 1000:1000 /bot
RUN chmod +s /bot

RUN pip install nltk numpy tflearn tensorflow duden pronouncing discord wikipedia

# for now as root.. even if this is not a good solution,
#USER 1000:1000


WORKDIR /bot