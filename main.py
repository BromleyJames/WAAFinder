import os
from pathlib import Path
from zipfile import ZipFile

import requests
from dotenv import load_dotenv


def check_unzipped(target_folder, gnaf_url):
    """
    Checks if the target url has been unzipped to a folder with the same name
    """
    p = Path(f"./{target_folder}")
    full_path = p.resolve()
    local_folder = full_path / gnaf_url.split("/")[-1].split(".")[0]

    if local_folder.exists():
        print(f"Local folder: {local_folder} exists!")
    else:
        print(f"Local folder: {local_folder} doesn't exist, checking downloads for zip")
        check_downloads(target_folder, gnaf_url)


def unzip_file(zip_path, local_filename):
    print("Unzipping file...")
    print(zip_path)

    with ZipFile(zip_path, "r") as zip_object:
        # Get total number of files
        total_files = len(zip_object.namelist())

        # Extract with progress tracking
        for index, file in enumerate(zip_object.namelist(), 1):
            zip_object.extract(file, local_filename)

            # Calculate and display progress
            progress = (index / total_files) * 100
            print(f"Progress: {progress:.2f}% ({index}/{total_files} files)", end="\r")

        print("\nUnzip completed!")


def check_downloads(target_folder, gnaf_url):
    """
    Check if the target folder is empty or doesn't exist.
    """
    p = Path(f"./{target_folder}")
    full_path = p.resolve()

    print(f"Checking the local folder: {full_path}")

    try:
        is_empty = not any(full_path.iterdir())

        if is_empty:
            download_data(p, gnaf_url)
        else:
            print(f"Data found at {full_path}\nSkipping download...")

    except FileNotFoundError:
        print("Folder doesn't exist, creating it...")
        full_path.mkdir(parents=True, exist_ok=True)
        download_data(p, gnaf_url)

    zip_path = full_path / gnaf_url.split("/")[-1]
    local_filename = full_path / gnaf_url.split("/")[-1].split(".")[0]
    unzip_file(zip_path, local_filename)


def download_data(target_folder, gnaf_url):
    """
    Donwloads the G-NAF zip file into the target folder
    """
    print("Downloading data from url:")
    print(gnaf_url)

    local_filename = target_folder / gnaf_url.split("/")[-1]
    print(f"Downloading to target file: {local_filename}")

    with requests.get(gnaf_url, stream=True) as response:
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024 * 1024  # 1 MB chunks

        print(f"Size to download: {total_size / (1000_000_000):.2f} GB")
        with open(local_filename, "wb") as file:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    file.write(chunk)
                    downloaded += len(chunk)
                    progress = (downloaded / total_size) * 100 if total_size > 0 else 0
                    print(f"Download progress: {progress:.2f}%", end="\r")
            print("\n")


def main():
    print("Hello from waafinder!")

    load_dotenv()

    gnaf_url = os.getenv("GNAF_URL")
    target_folder = os.getenv("TARGET_FOLDER")

    check_unzipped(target_folder, gnaf_url)


if __name__ == "__main__":
    main()
