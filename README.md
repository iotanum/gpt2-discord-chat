# gpt2-discord-chat

## Description

A work-in-progress AI chatbot/chat prompt gen using bare GPT-2 model.\
Currently trained only with discord chat logs.

## Usage

1. Install Cuda Toolkit [from NVIDIA](https://developer.nvidia.com/cuda-downloads)\
**(current latest supported version by pytorch is 10.7)**
2. Install pyTorch [from pyTorch](https://pytorch.org/get-started/locally/) **(10.7)**
3. ```shell
   pip install -r req
4. Export your Discord chat logs in CSV.\
For example [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter)
5. Prepare your training data with **utils/discord_parser.py**.
6. Run **main.py** and njoy.
