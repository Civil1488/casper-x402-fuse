import httpx

url = "http://127.0.0.1:8000/proxy/x402"

# Добавляем наш секретный ключ в заголовки запроса
headers = {
    "X-API-Key": "CasperFuseSecureToken2026_x402"
}

# Тест 1: Валидная транзакция (5 CSPR)
print("Отправка транзакции 5 CSPR...")
response = httpx.post(url, json={"amount": 5.0}, headers=headers)
print("Ответ сервера:", response.json())

# Тест 2: Превышение лимита за один вызов (15 CSPR при лимите 10)
print("\nОтправка транзакции 15 CSPR (должна заблокироваться)...")
response = httpx.post(url, json={"amount": 15.0}, headers=headers)
print("Ответ сервера:", response.json())
