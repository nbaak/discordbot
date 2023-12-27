# Just another Discord Bot

## Requirements
* Python 3.10
  * discord.py
  * requests
  * wikipedia
  

## Usage
1. Get your API Key for your Bot Application from the [Developers Page](https://discord.com/developers/applications).
2. CONFIG.py
    1. Add API Key to Config.
    
3. Docker
    1. Build Container docker-compose build
    2. Start Container docker-compose up -d
    3. Stop Container docker-compose down
    
    
## Some Words on AI
This AI is just a very simple Classifier, it trys to match incomming words to known patterns. If you want to use this AI properly, you need a lot of Data and Training. The pre set intents.json is not nearly big enough to be useful.

    