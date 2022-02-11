import json
import aiormq
import aiormq.types
from simple_print import sprint


async def pow_chat_message_rpc(message: aiormq.types.DeliveredMessage):
    incoming_message_dict = json.loads(message.body.decode())
    sprint(incoming_message_dict, c="red", b="on_white")

    incoming_message = incoming_message_dict["message"]
    hash_result, calculate_elapsed_time = (1, 1)  # await helpers.PoW(incoming_message, 16).calculate()

    outcoming_message_dict = {}
    outcoming_message_dict["username"] = "internal_worker"
    outcoming_message_dict[
        "message"] = f"POW RPC {incoming_message} hash:{hash_result} elapsed time:{calculate_elapsed_time}"
    outcoming_message_dict["source"] = "internal_worker"

    outcoming_message_bytes = json.dumps(outcoming_message_dict).encode()

    await message.channel.basic_publish(
        outcoming_message_bytes, routing_key=message.header.properties.reply_to,
        properties=aiormq.spec.Basic.Properties(
            correlation_id=message.header.properties.correlation_id
        ),
    )
    await message.channel.basic_ack(message.delivery.delivery_tag)
