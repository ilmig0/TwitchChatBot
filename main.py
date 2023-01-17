import os
from keep_alive import keep_alive

from twitchAPI import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatCommand
import asyncio

APP_ID = os.environ['APP_ID']
APP_SECRET = os.environ['APP_SECRET']
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
TARGET_CHANNEL = os.environ['TARGET_CHANNEL']


async def on_ready(ready_event: EventData):
    print('Bot is ready for work, joining channels')
    await ready_event.chat.join_room(TARGET_CHANNEL)


async def on_message(msg: ChatMessage):
    print(f'in {msg.room.name}, {msg.user.name} said: {msg.text}')


async def reply_command(cmd: ChatCommand):
    if len(cmd.parameter) == 0:
        await cmd.reply('you did not tell me what to reply with')
    else:
        await cmd.reply(f'{cmd.user.name}: {cmd.parameter}')

async def run():
    twitch = await Twitch(APP_ID, APP_SECRET)
    print('debug')
    await twitch.set_user_authentication('pwummr60esnj9k45yz1kmpa6qgxjjs', USER_SCOPE, 'dpsyq7vwc7mdvfl6fawo4su94ov38ugc3fn2inm3fj8jtg12ty')
    
    chat = await Chat(twitch)

    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)
    chat.register_command('reply', reply_command)
  
    chat.start()

    try:
        input('press ENTER to stop\n')
    finally:
        chat.stop()
        await twitch.close()

keep_alive()
asyncio.run(run())      