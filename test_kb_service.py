import requests
import json
from pprint import pprint as pp



def test_create_endpoint():
    text = input("Enter the text for the new KB article: ")
    payload = {"input": text}
    response = requests.post("http://localhost:999/create", json=payload)
    print('\n\n\n', response.json())



def test_search_endpoint():
    query = input("Enter the search query: ")
    payload = {"query": query}
    response = requests.post("http://localhost:999/search", json=payload)
    print('\n\n\n')
    pp(response.json())



def test_update_endpoint():
    title = input("Enter the title of the KB article to update: ")
    text = input("Enter the new text for the KB article: ")
    payload = {"title": title, "input": text}
    response = requests.post("http://localhost:999/update", json=payload)
    print('\n\n\n', response.json())



def main():
    while True:
        print("\n\n\n1. Create KB article")
        print("2. Search KB articles")
        print("3. Update KB article")
        print("4. Exit")
        choice = input("\n\nEnter your choice: ")
        if choice == '1':
            test_create_endpoint()
        elif choice == '2':
            test_search_endpoint()
        elif choice == '3':
            test_update_endpoint()
        elif choice == '4':
            break
        else:
            print("\n\n\nInvalid choice. Please enter a number between 1 and 4.")




if __name__ == "__main__":
    main()