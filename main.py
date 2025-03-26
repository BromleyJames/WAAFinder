from dotenv import load_dotenv
import os

def main():
    print("Hello from waafinder!")

    load_dotenv()

    gnaf_url = os.getenv('GNAF_URL')

    print(gnaf_url)


if __name__ == "__main__":
    main()