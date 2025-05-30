import datetime
import os
from pathlib import Path

def say_hi(msg:str = "Hi!", file_directory:str = "/app/data/") -> None:
    Path(file_directory).mkdir(parents=True, exist_ok=True)
    # Generate timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")

    # Define filename with timestamp
    file_name = f"outputfile_nrposner_timestamp_{timestamp}.txt"
    file_path = os.path.join(file_directory, file_name)

    # Write the timestamp inside the file
    with open(file_path, "w") as file:
        file.write(msg)

    print(f"File '{file_path}' created successfully.")

def add_numbers(a:int, b:int) -> int:
    return a + b

if __name__ == "__main__":
    say_hi()
