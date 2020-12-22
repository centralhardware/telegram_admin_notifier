import asyncio
import logging
import os

from telethon import events, TelegramClient

logging.basicConfig(level=logging.INFO)
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
telephone = os.getenv('TELEPHONE')
client = TelegramClient('alex', api_id, api_hash)


@client.on(events.NewMessage(outgoing=True, pattern='!admin', forwards=False))
async def handler(event):
    try:
        logging.info("triggered on %s", event.chat.title)
        admins = ""
        async for user in client.iter_participants(event.chat):
            if user.participant.admin_rights.delete_messages:
                admins += str(" @" + user.username)

        if admins:
            logging.info("fount admins: %s ", admins)
            await event.respond(admins)
        await client.delete_messages(event.chat_id, [event.id])
    except AttributeError:
        pass


client.connect()
client.start(phone=telephone)
client.run_until_disconnected()
