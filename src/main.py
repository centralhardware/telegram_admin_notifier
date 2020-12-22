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
    logging.info("receive !admin")
    admins = ""
    async for user in client.iter_participants(event.chat):
        try:
            if user.participant.admin_rights.delete_messages:
                admins += str(" @" + user.username)
        except AttributeError:
            pass

    m = await event.respond(admins)
    await asyncio.sleep(5)
    await client.delete_messages(event.chat_id, [event.id])


client.connect()
client.start(phone=telephone)
client.run_until_disconnected()
