# Just another Discord Bot

## Requirements
* Python 3.6
  * discord.py >= 1.7
  * requests
  * wikipedia
  * nltk
  * tensorflow

## Usage
1. Get your API Key for your Bot Application from the [Developers Page](https://discord.com/developers/applications).
2. CONFIG.py
    1. Add API Key to Config.
    2. Set your AI response channel.
3. Edit the intents.json to your needs. (It's just a default file in german atm).
4. Docker
    1. Build Docker Container with build-container.sh.
    2. Learn AI with learn-ai-containered.sh
    3. Start the Container with start-bot-container.sh