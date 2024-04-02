# Discord Chegg Bot

## Description
This Discord bot helps users retrieve answers from various educational platforms such as Chegg, Bartleby, SolutionInn, and more. Users can simply share the URL of the question they need help with, and the bot will provide them with the answer.

## Features
- Scrapes answers from supported educational platforms
- Uploads answers to AWS S3 for easy access
- Sends answer links to users via Discord messages
- Supports multiple educational platforms including Chegg, Bartleby, SolutionInn, and more

## How to Use
1. Invite the bot to your Discord server using the provided invite link.
2. Ensure the bot has necessary permissions to read messages and send messages in the desired channels.
3. Share the URL of the question you need help with in a channel where the bot is active.
4. The bot will process the request and send you a direct message with the answer link.

## Supported Platforms
- Chegg
- Bartleby
- SolutionInn
- Numerade
- Zookal
- Study.com
- GauthMath
- Transtutors
- Brainly.in
- Slideshare
- Scribd

## Setup
1. Clone this repository.
2. Install the required dependencies listed in `requirements.txt`.
3. Create a `.env` file and add your Discord bot token as `DISCORD_TOKEN`.
4. Run the bot using `python bot.py`.

## Contributors
- [Your Name](link_to_your_profile) - Bot Developer

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

