import uvicorn


def main():
    print("Hello from payment-api-py!")

    uvicorn.run("src.api.app:app", port=7000, host="0.0.0.0")


if __name__ == "__main__":
    main()
