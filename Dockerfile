FROM python:3.12

RUN mkdir /bot

RUN chown -R 1000:1000 /bot
RUN chmod +s /bot

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

#numpy duden pronouncing discord.py wikipedia pytz

CMD ["python","-u","/bot/main.py"]
# or ENTRYPOINT?


WORKDIR /bot
