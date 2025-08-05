from jose import jwt

def main():
    print("Hello from 10xdevs-final!")


if __name__ == "__main__":
    token = jwt.encode({'key': 'value'}, 'tajny_klucz', algorithm='HS256')
    data = jwt.decode(token, 'tajny_klucz', algorithms=['HS256'])
    print(data)
    print(token)
    main()
