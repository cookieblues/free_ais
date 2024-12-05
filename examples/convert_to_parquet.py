import os
from pathlib import Path

import polars as pl
from dotenv import load_dotenv

load_dotenv()

file_directory = Path(os.environ["storage_directory"])
files = file_directory.iterdir()

for file in files:
    print(file)
    if file.suffix != ".csv":
        continue
    df = pl.scan_csv(file)
    filename = file.stem + ".parquet"
    df.sink_parquet(
        file_directory / filename, compression="snappy", row_group_size=100_000
    )
