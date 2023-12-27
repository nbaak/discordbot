FROM python:3.10

RUN mkdir /bot

RUN chown -R 1000:1000 /bot
RUN chmod +s /bot

RUN pip install numpy duden pronouncing discord.py wikipedia

CMD ["python","-u","/bot/main.py"]
# or ENTRYPOINT?


WORKDIR /bot