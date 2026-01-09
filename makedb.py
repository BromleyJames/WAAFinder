import os
import shutil
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


def index_files(folder, regex):
    """Recursively iterates over a directory to index the files according to their name"""
    print(f"Folder: {folder}")
    print(f"Regex: {regex}")


def load_data(cursor, file, table):
    pass


def main():
    load_dotenv()

    gnaf_url = os.getenv("GNAF_URL")
    target_folder = os.getenv("TARGET_FOLDER")
    database_type = os.getenv("DATABASE")

    conn = sqlite3.connect("gnaf.db")
    cursor = conn.cursor()
    print("Connected to sqlite db")

    local_folder = get_foldername(target_folder, gnaf_url)

    if database_type == "sqlserver":
        # TODO - implement the connection to MS sql server

        print("Creating tables...")
        create_tables_scripts = (
            local_folder
            / "G-NAF/Extras/GNAF_TableCreation_Scripts/create_tables_sqlserver.sql"
        )
        run_ddl(create_tables_scripts, cursor)

        print("Adding FK constraints...")
        create_fk_constraints = (
            local_folder
            / "G-NAF/Extras/GNAF_TableCreation_Scripts/add_fk_constraints.sql"
        )
        run_ddl(create_fk_constraints, cursor)

        print("Creating views...")
        create_views_scripts = (
            local_folder / "G-NAF/Extras/GNAF_View_Scripts/address_view.sql"
        )
        run_ddl(create_views_scripts, cursor)

    else:
        print("Creating tables...")
        create_tables_scripts = (
            local_folder
            / "G-NAF/Extras/GNAF_TableCreation_Scripts/create_tables_sqlserver.sql"
        )
        run_ddl(create_tables_scripts, cursor)

        print("Creating views...")
        create_views_scripts = (
            local_folder / "G-NAF/Extras/GNAF_View_Scripts/address_view.sql"
        )

        copy_suffix = "ansi"
        copy_path = create_views_scripts.with_stem(
            create_views_scripts.stem + copy_suffix
        )

        shutil.copy2(create_views_scripts, copy_path)

        content = copy_path.read_text(encoding="utf-8")

        print(f"File copied to: {copy_path}")

        # sqllite doesn't understand this syntax
        modified_content = content.replace("OR REPLACE", "")

        copy_path.write_text(modified_content, encoding="utf-8")

        run_ddl(copy_path, cursor)


    authority_regex = "^Authority_Code_(?<table>.*?)_psv.psv$"
    state_regex = "^[^_]*_(?<table>.*?)_psv.psv$"

    print("\nIndexing Authority Code data...")

    # Use regex to find folder that starts with "G-NAF" the name of this folder can change
    # It includes the month and year of the release

    data_folder = (local_folder / "G-NAF")
    data_folder = list(data_folder.rglob("G-NAF*"))[0]
    print(list(data_folder.iterdir()))

    index_files(data_folder, authority_regex)


if __name__ == "__main__":
    main()