import gemini as gni
import whatsweb as wb
import time
import os

driver = wb.start_whatsapp_web()
k=wb.search_contact_name(driver)
# k = "test"
ok=wb.save_text(driver,k)
text= wb.detect_new_chat(driver,k,ok)
wb.save_new_text(driver,k)
directory_path = "./chats"  # Save in the 'chats' folder within the project directory
file_path = os.path.join(directory_path, f"{k}.txt")

    # Ensure the directory exists
os.makedirs(directory_path, exist_ok=True)
while True:
    with open(file_path, 'r', encoding='utf-8') as file:
        chat_history = file.read()

    response = gni.ai(chat_history)
    print(response)
    wb.send_text(driver,response)
    time.sleep(2)
    wb.save_new_text(driver,k)
    text= wb.detect_new_chat(driver,k,text)
    print(text)
    wb.save_new_text(driver,k)
