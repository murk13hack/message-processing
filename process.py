from pymongo import MongoClient
from access_token import get_access_token
from response_from_model import gigachat_request
from parse_cfg import CONFIG
from bd_connection import get_motor_collection
import gigachat
import yaml
import requests
import json
import aio_pika
import asyncio

# Основная функция потребителя
async def consume():
    connection = await aio_pika.connect_robust(CONFIG["rebbitMQ_host"])
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)
        queue = await channel.declare_queue(CONFIG["rebbitMQ_queue_name"], durable=True)
        await queue.consume(process_message) # подписка на очередь
        print("Ожидание сообщений...")
        await asyncio.Future()  # Бесконечное ожидание сообщений

# Читаем промпт из файла
async def get_prompt(prompt_file):
    async with open(prompt_file, "r") as f:
        return await f.read()

# Функция обработки сообщений
async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        msg_body = message.body.decode() # message.body - это байты!
        print(f"Получено сообщение: {msg_body}")
        prompt = await get_prompt(CONFIG["prompt_file"])
        access_token = get_access_token(CONFIG["client_id"], CONFIG["client_secret"])
        giga_answer = await gigachat_request(prompt, msg_body, access_token)
        await save_processed_message(giga_answer)

# Сохранение в монгу
async def save_processed_message(processed_text: str):
    collection = get_motor_collection()
    await collection.insert_one({"message": processed_text})

def main():
    asyncio.run(consume())

if __name__ == "__main__":
    main()