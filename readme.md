Markdown
# Casper x402 Fuse 🛡️🤖

[![Casper Network](https://img.shields.io/badge/Network-Casper-red)](https://casper.network/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

An autonomous, lightweight **Middleware Fuse (API Gateway)** designed to protect Web3 AI Agents and automated scripts operating within the Casper Network ecosystem. 

By intercepting transactions before they hit the blockchain, **Casper x402 Fuse** acts as a circuit breaker, preventing unauthorized draining of wallets due to prompt injections, smart contract logic flaws, or rogue AI behavior.

---

## 🔥 The Problem & The Solution

* **The Risk:** Autonomous AI Agents manage real crypto-wallets. If an AI gets compromised, tricked, or loops due to an error, it can drain its entire balance on gas fees or bad trades in seconds.
* **The Shield:** This middleware introduces a local security perimeter. The AI Agent cannot sign or broadcast transactions without passing the real-time threshold and budget checks enforced by the Fuse.

---

## 🛠️ Key Features

* **Single-Call Thresholds:** Instantly drops any transaction requesting funds above the defined `max_per_call_cspr` limit.
* **Rolling 24-Hour Budget:** Tracks cumulative expenditures using an ultra-light SQLite database (`ledger.db`) and blocks requests if the daily limit (`daily_budget_cspr`) is exceeded.
* **Secure Agent-to-Proxy Auth:** Implements secure header validation via `X-API-Key` to block unauthorized internal or external requests.
* **Instant Telegram Alerts:** Real-time push notifications sent directly to the agent's owner when a security threshold is triggered or an attack is deflected.
* **Zero Overhead:** Built using asynchronous Python (FastAPI + HTTPX), ensuring sub-millisecond local processing latency.

---

## 🏗️ Architecture Flow

[ AI Agent / Script ]
│
▼ (Sends Transaction Request with X-API-Key)
[ Casper x402 Fuse (Middleware) ]
│
├──► [ Check 1: Single Limit? ] ──► Exceeded? ──► [ Block & Telegram Alert ⚠️ ]
│
├──► [ Check 2: 24h Budget? ]   ──► Exceeded? ──► [ Block & Telegram Alert ⚠️ ]
│
└──► [ Approved ✅ ] ──► Record to SQLite ──► Return "Go Ahead" to Agent ──► (Casper Network)


---

## ⚙️ Configuration (`config.json`)

Securely adjust your thresholds and bot settings in the local JSON file:

```json
{
  "max_per_call_cspr": 10.0,
  "daily_budget_cspr": 500.0,
  "telegram_bot_token": "YOUR_TG_BOT_TOKEN",
  "telegram_chat_id": "YOUR_TG_CHAT_ID",
  "api_secret_token": "YOUR_SECRET_INTERNAL_KEY"
}
🚀 Quick Start
1. Install Dependencies
Ensure you have Python 3.10+ installed, then run:

Bash
pip install fastapi uvicorn httpx
2. Run the Security Gateway
Launch the local middleware server:

Bash
python main.py
The server will boot locally at http://127.0.0.1:8000.

3. Test the Safeguards
Run the verification script to simulate normal and malicious transaction flows:

Bash
python check.py
🔮 Future Roadmap
[ ] Integration with native Casper SDK to simulate transactions gas cost before approving.

[ ] Multi-agent management (different limits for different agent sub-routines).

[ ] Front-end dashboard for adjusting limits on the fly without changing config files.