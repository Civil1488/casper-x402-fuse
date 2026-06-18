import sqlite3
import json
import httpx
from fastapi import FastAPI, Request, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from datetime import datetime, timedelta
import uvicorn

app = FastAPI(title="Casper x402 Fuse Middleware")

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Загружаем конфиг один раз при запуске, чтобы не нагружать диск
def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

CONFIG = load_config()

# Инициализация БД
def init_db():
    conn = sqlite3.connect('ledger.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions 
                      (timestamp DATETIME, amount REAL)''')
    conn.commit()
    conn.close()

init_db()

# Функция отправки алерта в Telegram
async def send_telegram_alert(message: str):
    try:
        url = f"https://api.telegram.org/bot{CONFIG['telegram_bot_token']}/sendMessage"
        async with httpx.AsyncClient() as client:
            await client.post(url, json={"chat_id": CONFIG['telegram_chat_id'], "text": message})
    except Exception as e:
        print(f"Ошибка отправки в ТГ: {e}")

# Основной защищенный роут
@app.post("/proxy/x402")
async def fuse_middleware(request: Request, api_key: str = Security(api_key_header)):
    # Проверка безопасности: валидация API-ключа агента
    if not api_key or api_key != CONFIG["api_secret_token"]:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")

    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    amount = float(data.get("amount", 0))
    
    # Проверка 1: Лимит на одну операцию
    if amount > CONFIG["max_per_call_cspr"]:
        await send_telegram_alert(f"⚠️ Блокировка! Превышен лимит за один вызов: {amount} CSPR")
        return {"status": "BLOCKED", "reason": "Single call limit exceeded"}

    # Проверка 2: Дневной лимит
    conn = sqlite3.connect('ledger.db')
    cursor = conn.cursor()
    one_day_ago = datetime.now() - timedelta(days=1)
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE timestamp > ?", (one_day_ago,))
    row = cursor.fetchone()
    total_spent = row[0] if row[0] is not None else 0
    
    if (total_spent + amount) > CONFIG["daily_budget_cspr"]:
        await send_telegram_alert(f"⚠️ БЛОКИРОВКА! Исчерпан дневной бюджет. Попытка траты: {amount} CSPR")
        conn.close()
        return {"status": "BLOCKED", "reason": "Daily budget depleted"}

    # Запись транзакции в случае успеха
    cursor.execute("INSERT INTO transactions VALUES (?, ?)", (datetime.now(), amount))
    conn.commit()
    conn.close()

    return {"status": "APPROVED", "current_daily_spend": total_spent + amount}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
