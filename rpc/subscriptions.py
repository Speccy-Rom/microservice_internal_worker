import aiormq
from termcolor import cprint

from consumer import methods
from settings import AMQP_URI
from settings import UNIQUE_PREFIX
from rpc import methods


async def rpc_subscriptions():
    connection = await aiormq.connect(AMQP_URI)
    channel = await connection.channel()
    cprint(f"AMQP CONSUMER:     ready [yes] PREFIX={UNIQUE_PREFIX}", "green")

    pow_chat_message_rpc_queue__declared = await channel.queue_declare(f"{UNIQUE_PREFIX}:internal_worker:pow_chat_message_rpc", durable=False)

    await channel.basic_consume(pow_chat_message_rpc_queue__declared.queue, methods.pow_chat_message_rpc, no_ack=False)
