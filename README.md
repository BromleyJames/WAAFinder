# WAAFinder
WAAFinder stands for Where Are Aussies? Finder. 

A geolocation library for Australian addresses, based on the GNAF dataset

This project uses `uv` https://github.com/astral-sh/uv to manage the project, including handling dependencies and assumes you have `uv` installed.

set the environment variables file by creating a `.env` file with the following contents:


```
GNAF_URL="https://data.gov.au/data/dataset/19432f89-dc3a-4ef3-b943-5326ef1dbecc/resource/33b7d2a1-a246-4853-beb9-167699bfa91c/download/g-naf_feb25_allstates_gda2020_psv_1018.zip"

TARGET_FOLDER="gnaf-data"

```
NOTE: if you choose a diffrent target folder name, make sure to add it to your gitignore file.

and then running:


```
source set_env.sh
```

After this, you should be able to run

```
uv run main.py
```