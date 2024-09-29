#FaceRecognition
import socket
import webbrowser
import requests

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def auto_fill_login(url, username, password):
    # Initialize the WebDriver (assuming Chrome here)
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Open the webpage
        driver.get(url)
        # Find the username and password fields and fill them
        username_field = driver.find_element(By.NAME, 'username')
        username_field.send_keys(username)
        password_field = driver.find_element(By.ID, 'password')
        password_field.send_keys(password)

        # Find and click the login button
        login_button = driver.find_element(By.ID, 'loginbtn')
        login_button.click()
        # Do not submit the form

    finally:

    # Close the browser window

        print("fim")

def receiver():
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to an IP address and port
    host = '192.168.88.252'  # Listen on localhost
    port = 12345  # Choose the same port number as the sender
    s.bind((host, port))

    # Listen for incoming connections
    s.listen(1)
    print("Waiting for incoming connections...")

    # Accept a connection
    conn, addr = s.accept()
    print(f"Connected to {addr[0]}:{addr[1]}")

    # Receive the name from the sender
    received_data = conn.recv(8192)
    if received_data:
        decoded_data = received_data.decode('utf-8')
        time.sleep(7)  # Delay for 5 seconds
        print("Face recognized. Logging in...")
        # Print the received name
        print("Received:", decoded_data)
        credentials = decoded_data.split()
        url = "https://ead.ipleiria.pt/2023-24/"  # Replace with the actual file path
        auto_fill_login(url, credentials[0], credentials[1])




    else:
        print("No data received.")

    # Close the connection
    conn.close()

if __name__ == "__main__":
    receiver()


