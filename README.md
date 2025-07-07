# 📱 WhatsApp Chat Automation Tool

A Python-based automation tool that uses **Selenium WebDriver** to interact with **WhatsApp Web**. This script allows you to:

- Search and open a chat with a specific contact  
- Extract and save messages with timestamp and reply context  
- Detect new incoming messages  
- Send automated messages back  
- Retain login sessions using persistent Chrome profiles  

---

## 🚀 Features

- ✅ Load WhatsApp Web with persistent login (no repeated QR scans)
- 🔍 Search and select any contact or group by name
- 💬 Extract messages (incoming & outgoing) with timestamps and reply context
- 📂 Save messages to `.txt` files (by contact name)
- 🔄 Detect newly received messages from the selected chat
- 📤 Send automated responses
- 🧠 Auto-format messages with rich text and emoji parsing (via `alt` tags)

---

## 📦 Requirements

- Python 3.7+
- Google Chrome (latest recommended)
- [ChromeDriver](https://chromedriver.chromium.org/downloads) matching your Chrome version
- Gemini AI api key
- Dependencies:
  ```bash
  pip install selenium beautifulsoup4
  ```


---

## ⚙️ How to Use

1. **Clone the repository** and install dependencies.
2. **Run the script**:
   ```bash
   python main.py
   ```
3. **Log in to WhatsApp Web** when prompted. The login will be saved.
4. **Search** for a contact name when asked.
5. The chat history will be scraped and saved.
6. Script can **detect new incoming messages** and optionally **send responses**.

---

## 🔐 Privacy Notice

This tool **runs locally on your machine** and does not store or transmit any chat data externally. It only accesses WhatsApp Web using your authenticated session via a persistent Chrome profile.

---

## ❗Disclaimer

- This tool is for **educational and personal use only**.
- Use responsibly and respect WhatsApp's [Terms of Service](https://www.whatsapp.com/legal/terms-of-service/).
- Automation may violate WhatsApp usage policies and could result in account limitations.

---

## 📬 Future Improvements (Ideas)

- Export to `.csv` or `.json` for analysis
- Full chat history scroll automation
- GUI interface for easy usage
- make code more readable and maintainable
- support for images, videos and audios.
  
---

## 🧠 Author

**Aditya**  
Python & Automation Enthusiast  
Feel free to fork, improve, and share!

---
