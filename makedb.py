import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv


def get_foldername(target_folder, gnaf_url):
    """
    Checks if the target url has been unzipped to a folder with the same name
    """
    p = Path(f"./{target_folder}")
    full_path = p.resolve()
    local_folder = full_path / gnaf_url.split("/")[-1].split(".")[0]

    if local_folder.exists():
        print(f"Local folder: {local_folder} exists!")
        return local_folder
    else:
        print(f"Local folder: {local_folder} doesn't exist, donwload it first")


def run_ddl(file, cursor):
    """
    Generic function to run DDL from a sql file.
    """
    with file.open("r") as sql_file:
        sql_script = sql_file.read()
        try:
            cursor.executescript(sql_script)
        except sqlite3.OperationalError:
            print(f"Error in exectuing DDL, possibly run previously, skipping: {file}")


def main():
    load_dotenv()

    gnaf_url = os.getenv("GNAF_URL")
    target_folder = os.getenv("TARGET_FOLDER")

    conn = sqlite3.connect("gnaf.db")
    cursor = conn.cursor()
    print(f"Connected to sqlite db")

    local_folder = get_foldername(target_folder, gnaf_url)

    print("Creating tables...")
    create_tables_scripts = (
        local_folder / "G-NAF/Extras/GNAF_TableCreation_Scripts/create_tables_ansi.sql"
    )
    run_ddl(create_tables_scripts, cursor)

    print("Adding FK constraints...")
    create_fk_constraints = (
        local_folder / "G-NAF/Extras/GNAF_TableCreation_Scripts/add_fk_constraints.sql"
    )
    run_ddl(create_fk_constraints, cursor)

    print("Creating views...")
    create_views_scripts = (
        local_folder / "G-NAF/Extras/GNAF_View_Scripts/address_view.sql"
    )
    run_ddl(create_views_scripts, cursor)


if __name__ == "__main__":
    main()
