import json
from producer import methods as producer_methods
from consumer import helpers


async def pow_chat_message(message):
    incoming_message_dict = json.loads(message.body.decode())
    incoming_message = incoming_message_dict["message"]
    hash_result, calculate_elapsed_time = await helpers.PoW(incoming_message).calculate()

    outcoming_message_dict = {
        "username": "internal_messager",
        "message": f"POW {incoming_message} hash:{hash_result} elapsed time:{calculate_elapsed_time}",
    }

    await producer_methods.send_message_to_internal_messager(outcoming_message_dict)
    await message.channel.basic_ack(message.delivery.delivery_tag)
