from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import uvicorn
from main import index
from queue import Queue
import threading

# "dev" - для разработки, "prod" - для продакшена
type_server = "prod"

app = FastAPI()

# Добавляем middleware для поддержки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Замените "*" на нужные вам домены
    allow_methods=["*"],
    allow_headers=["*"],
)

# Очередь для управления подключениями
connection_queue = Queue()
queue_lock = threading.Lock()

# Семафор для ограничения количества одновременных подключений
concurrency_limit = 3
concurrency_semaphore = threading.Semaphore(concurrency_limit)

def process_request(city, name, direction, design):
    # Отправить сообщение о том, что пользователь в очереди и указать его позицию
    yield f"data: Пожалуйста подождите, Вы в очереди\n\n"
    
    # Дождитесь, пока будет освобождено место в очереди и начнется обработка
    while not concurrency_semaphore.acquire(blocking=False):
        pass

    # Если семафор был захвачен, пользователь выполняет работу
    try:
        for step in index(city, name, direction, 'GPT', design, type_server):
            yield f"data: {step}\n\n"
    finally:
        # Освобождаем семафор
        concurrency_semaphore.release()

@app.get('/data_stream')
def data_stream(city: str, name: str, direction: str, design: str):
    return StreamingResponse(process_request(city, name, direction, design), media_type="text/event-stream")

if __name__ == '__main__':
    if type_server == "prod":
        uvicorn.run(app, host='server.monocreator.ru', port=5000, workers=1, ssl_keyfile="/etc/letsencrypt/live/server.monocreator.ru/privkey.pem", ssl_certfile="/etc/letsencrypt/live/server.monocreator.ru/cert.pem") #ssl_context=('/etc/letsencrypt/live/server.monocreator.ru/fullchain.pem', '/etc/letsencrypt/live/server.monocreator.ru/privkey.pem'), threaded=True
        # uvicorn.run(app, host="", port=5000, workers=1)
    else:
        uvicorn.run(app, host="45.9.40.47", port=5000, workers=1)