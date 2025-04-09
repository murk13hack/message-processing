### aio_pika — это асинхронная библиотека Python для работы с RabbitMQ, основанная на asyncio. Она позволяет эффективно взаимодействовать с очередями сообщений в асинхронном режиме, что особенно полезно для высоконагруженных приложений. ###

## Основные возможности aio_pika ##

* Асинхронный API – работает с async/await, не блокирует event loop.
* Поддержка AMQP – полная реализация протокола RabbitMQ.
* Паттерны работы:
    + Publish/Subscribe (обменники)
    + Очереди (Queues)
    + RPC (Remote Procedure Calls)
    + Интеграция с asyncio – совместима с FastAPI, Quart и другими асинхронными фреймворками.

# Ключевые компоненты #

* Подключение (aio_pika.connect):
```
import aio_pika

async def main():
    connection = await aio_pika.connect("amqp://guest:guest@localhost/")
    channel = await connection.channel()
```

 + более продвинутый способ подключения(connect_robust):
    - Автоматически восстанавливает соединение при разрывах
    - Периодически проверяет соединение (health checks)
    - Лучше для продакшена
    ```
    connection = await aio_pika.connect_robust(RABBITMQ_HOST)  # ← Устойчивое соединение

    # Без контекстного менеджера нужно вручную вызывать connection.close().
    async with connection:  # ← Гарантированное закрытие
    channel = await connection.channel()
    # ... работа с очередью
    # Здесь соединение уже корректно закрыто

    await channel.set_qos(prefetch_count=10)  # ← Обрабатывать не более 10 сообщений одновременно

    # durable=True для очереди
    '''
    - Сохраняет очередь на диске RabbitMQ
    - Переживает перезапуск сервера
    - Гарантирует доставку при сбоях
    '''
    # Без durable
    '''
    - Очередь существует только в памяти
    - Удаляется при рестарте RabbitMQ
    - Потеря сообщений при авариях
    '''
    ```
* Отправка сообщений (publish)
```
await channel.default_exchange.publish(
    aio_pika.Message(body="Hello!".encode()),
    routing_key="queue_name"
)
```
* Получение сообщений (consume) python
```
queue = await channel.declare_queue("queue_name")

async with queue.iterator() as queue_iter:
    async for message in queue_iter:
        print(message.body.decode())
        await message.ack()
```