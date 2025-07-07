from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
from bs4 import BeautifulSoup
import os
from selenium.webdriver.chrome.options import Options
import re

# Set up Chrome options with a persistent user data directory
def start_whatsapp_web():

    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=C:/chrome-whatsapp-profile")  # Use a specific path

    # Initialize WebDriver with the specified profile
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://web.whatsapp.com')

    input("Press Enter after logging in successfully...")
    return driver

def search_contact_name(driver):

    while True:
        contact_name = input("Enter the name of the contact you wish to get the chat of (or type 'quit' to exit): ")
        if contact_name.lower() == 'quit':
            driver.quit()
            exit()

        try:
            # Search for the contact
            search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
            search_box.send_keys(Keys.CONTROL + "a")  # Select all
            search_box.send_keys(Keys.BACKSPACE)       # Delete
            search_box.send_keys(contact_name)
            time.sleep(1)

            # Wait for the contact to appear and click on it
            contact = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, f'//div[@tabindex="-1"][@aria-selected="false"]'))
            )
            contact.click()
            time.sleep(1.5)
            break  # Exit the loop if the contact is found and clicked

        except:
            print(f"Contact '{contact_name}' not found. Please re-enter or type 'quit' to exit.")
            time.sleep(4)
    return contact_name

def save_text(driver, contact_name):
    chat_page = driver.find_element(By.XPATH, "//div[@data-tab='8']")
    chat_page.send_keys(Keys.END)
    time.sleep(1.5)

    messages = driver.find_elements(By.XPATH, '//div[contains(@class,"message-in")] | //div[contains(@class,"message-out")]')
    chat_text = []

    for message in messages:
        try:
            # Determine the sender
            sender = "Me" if "message-out" in message.get_attribute("class") else contact_name

            # Check if this message is a reply to another message
            reply_context = ""
            try:
                # Locate the quoted text inside the `_aju3` div, if it exists
                reply_element = message.find_element(By.XPATH, './/div[contains(@class, "_aju3")]//span[@class="quoted-mention _ao3e"]')
                inner_html = reply_element.get_attribute("innerHTML")
                soup_r = BeautifulSoup(inner_html, "html.parser")
                reply_content = []

                for element in soup_r.contents:
                    if element.name == "img":
                        # Get the alt attribute for the img tag
                        alt_text = element.get("alt")
                        if alt_text:
                            reply_content.append(alt_text)
                    else:
                        # Add direct text nodes
                        reply_content.append(element.string.strip() if element.string else "")

                # Join all parts into the final result
                reply_context = ' '.join(reply_content).strip()                
            except:
                pass  # No reply context
            message_data = message.find_element(By.XPATH, './/div[@class="_akbu"]/span/span')
            inner_html = message_data.get_attribute("innerHTML")
            soup = BeautifulSoup(inner_html, "html.parser")
            text_content = []

            for element in soup.contents:
                if element.name == "img":
                    # Get the alt attribute for the img tag
                    alt_text = element.get("alt")
                    if alt_text:
                        text_content.append(alt_text)
                else:
                    # Add direct text nodes
                    text_content.append(element.string.strip() if element.string else "")

            # Join all parts into the final result
            message_text = ' '.join(text_content).strip()
            timestamp = ""
            try:
                # New XPath selector to locate timestamp more accurately
                timestamp_element = message.find_element(By.XPATH, './/span[@class="x1rg5ohu x16dsc37"]')
                timestamp = timestamp_element.text  # Print timestamp to confirm
            except Exception as e:
                print("Debug: Timestamp not found for this message:", e)
                timestamp = "Unknown"  # Fallback if no timestamp found

            # Format message with reply context if available
            if reply_context:
                formatted_message = f'{sender} (replied to "{reply_context}") at {timestamp}: {message_text}'
            else:
                formatted_message = f'{sender} at {timestamp}: {message_text}'

            chat_text.append(formatted_message)

        except Exception as e:
            print("Debug: Error extracting message text", e)
            continue

    # Prepare the directory and file path using contact's name
    directory_path = "./chats"  # Save in the 'chats' folder within the project directory
    file_path = os.path.join(directory_path, f"{contact_name}.txt")

    # Ensure the directory exists
    os.makedirs(directory_path, exist_ok=True)

    last_me_text=""
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in chat_text:
            file.write(line + "\n")
            if line.startswith(contact_name):
                last_me_text = line
    print(f"Chat saved to {file_path}")
    st = re.sub(r'^.*? at \d{1,2}:\d{2} [ap]m: ', '', last_me_text)
    return st



def detect_new_chat(driver, contact_name,last_message_text):
    chat_page = driver.find_element(By.XPATH, "//div[@data-tab='8']")
    chat_page.send_keys(Keys.END)

    max_attempts = 100  # Limit attempts to prevent an infinite loop
    attempts = 0
    
    while attempts < max_attempts:
        try:
            # Get the latest message from Kashu
            message_data = driver.find_elements(By.XPATH, '//div[contains(@class,"message-in")][last()]//span[@class="_ao3e selectable-text copyable-text"]//span')
            inner_html = message_data[-1].get_attribute("innerHTML")
            soup = BeautifulSoup(inner_html, "html.parser")
            new_text_content = []

            for element in soup.contents:
                if element.name == "img":
                    # Get the alt attribute for the img tag
                    alt_text = element.get("alt")
                    if alt_text:
                        new_text_content.append(alt_text)
                else:
                    # Add direct text nodes
                    new_text_content.append(element.string.strip() if element.string else "")

            # Join all parts into the final result
            latest_message = ' '.join(new_text_content).strip()
            if latest_message:
                new_text = latest_message

                # If the latest message is different from the last tracked message, return it
                if new_text != last_message_text:
                    print("New message detected:", new_text)
                    last_message_text = new_text

                    return new_text  # Return the new message text

        except Exception as e:
            print("Error detecting new message:", e)
            return e

        time.sleep(2)  # Brief pause to reduce CPU usage
        attempts += 1
    
    return None  # Return None if no new message is found after max_attempts

    
def quit_whatsapp_web():

    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=C:/chrome-whatsapp-profile")
    driver = webdriver.Chrome(options=chrome_options)
    driver.quit()


def escape_js_string(message):
    """
    Escapes special characters in a string for use in JavaScript.
    """
    return message.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"').replace("\n", "\\n")

def send_text(driver, message):
    """
    Sends a message to the currently open chat in WhatsApp Web.
    """
    try:
        # Escape the message for JavaScript
        escaped_message = escape_js_string(message)

        # JavaScript code to insert the message into the chat box and send it
        js_script = f"""
            let messageBox = document.querySelector('div[contenteditable="true"][data-tab="10"]');
            if (messageBox) {{
                messageBox.focus();
                
                // Clear any existing content
                messageBox.innerHTML = "";
                
                // Insert the escaped message
                let messageText = '{escaped_message}';
                
                let range = document.createRange();
                let selection = window.getSelection();
                selection.removeAllRanges();
                
                range.selectNodeContents(messageBox);
                selection.addRange(range);
                
                document.execCommand('insertText', false, messageText);
                
                // Trigger input event to register the new message
                messageBox.dispatchEvent(new Event('input', {{ bubbles: true }}));
                
                // Wait for 1 second, then send the message
                setTimeout(() => {{
                    let sendButton = document.querySelector('button[aria-label="Send"]');
                    if (sendButton) {{
                        sendButton.click();
                    }} else {{
                        console.log("Send button not found.");
                    }}
                }}, 1000);
            }} else {{
                console.log("Message box not found.");
            }}
        """

        # Log the JavaScript for debugging
        print("Executing JavaScript, sending text:", escaped_message)

        # Execute the JavaScript in the context of the page
        wpr = 40
        time_taken_type = 60 / (wpr * 5) * len(escaped_message)
        time.sleep(int(time_taken_type))  # Optional, adds a delay to ensure the message is sent

        driver.execute_script(js_script)

    except Exception as e:
        print(f"An error occurred: {e}")


def save_new_text(driver, contact_name):

    message = driver.find_elements(By.XPATH, '//div[contains(@class,"message-in")] | //div[contains(@class,"message-out")]')[-1]
    try:
        # Determine the sender
        sender = "Me" if "message-out" in message.get_attribute("class") else contact_name

            # Check if this message is a reply to another message
        reply_context = ""
        try:
            # Locate the quoted text inside the `_aju3` div, if it exists
            reply_element = message.find_element(By.XPATH, './/div[contains(@class, "_aju3")]//span[@class="quoted-mention _ao3e"]')
            inner_html = reply_element.get_attribute("innerHTML")
            soup_r = BeautifulSoup(inner_html, "html.parser")
            reply_content = []

            for element in soup_r.contents:
                    if element.name == "img":
                        # Get the alt attribute for the img tag
                        alt_text = element.get("alt")
                        if alt_text:
                            reply_content.append(alt_text)
                    else:
                        # Add direct text nodes
                        reply_content.append(element.string.strip() if element.string else "")

                # Join all parts into the final result
            reply_context = ' '.join(reply_content).strip()                
        except:
                pass  # No reply context
        message_data = message.find_element(By.XPATH, './/div[@class="_akbu"]/span/span')
        inner_html = message_data.get_attribute("innerHTML")
        soup = BeautifulSoup(inner_html, "html.parser")
        text_content = []

        for element in soup.contents:
                if element.name == "img":
                    # Get the alt attribute for the img tag
                    alt_text = element.get("alt")
                    if alt_text:
                        text_content.append(alt_text)
                else:
                    # Add direct text nodes
                    text_content.append(element.string.strip() if element.string else "")

            # Join all parts into the final result
        message_text = ' '.join(text_content).strip()
        timestamp = ""
        try:
                # New XPath selector to locate timestamp more accurately
                timestamp_element = message.find_element(By.XPATH, './/span[@class="x1rg5ohu x16dsc37"]')
                timestamp = timestamp_element.text  # Print timestamp to confirm
        except Exception as e:
                print("Debug: Timestamp not found for this message:", e)
                timestamp = "Unknown"  # Fallback if no timestamp found

            # Format message with reply context if available
        if reply_context:
                formatted_message = f'{sender} (replied to "{reply_context}") at {timestamp}: {message_text}'
        else:
                formatted_message = f'{sender} at {timestamp}: {message_text}'

    except Exception as e:
            print("Debug: Error extracting message text", e)

    # Prepare the directory and file path using contact's name
    directory_path = "./chats"  # Save in the 'chats' folder within the project directory
    file_path = os.path.join(directory_path, f"{contact_name}.txt")

    # Ensure the directory exists
    os.makedirs(directory_path, exist_ok=True)

    last_me_text=""
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(formatted_message + "\n")
        if formatted_message.startswith(contact_name):
            last_me_text = formatted_message
    print(f"new text saved to {file_path}")
    st = re.sub(r'^.*? at \d{1,2}:\d{2} [ap]m: ', '', last_me_text)
    return st

if __name__ == "__main__":
        
    driver = start_whatsapp_web()
    k=search_contact_name(driver)
    print(k)
    ok=save_text(driver,k)
    text= detect_new_chat(driver,k,ok)
    print(text)