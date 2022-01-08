import aiormq
from termcolor import cprint

from consumer import methods
from settings import AMQP_URI
from settings import UNIQUE_PREFIX


async def consumer_subscriptions():
    connection = await aiormq.connect(AMQP_URI)
    channel = await connection.channel()
    cprint(f"AMQP CONSUMER:     ready [yes] PREFIX={UNIQUE_PREFIX}", "green")

    pow_chat_message_queue__declared = await channel.queue_declare(f"{UNIQUE_PREFIX}:internal__worker:pow_chat_message", durable=False)

    # no_ack=False - поведение по умолчанию, отвечаем принудительно в самом обработчике по мере выполнения
    # (предпочитаемый вариант)
    await channel.basic_consume(pow_chat_message_queue__declared.queue, methods.pow_chat_message, no_ack=False)
