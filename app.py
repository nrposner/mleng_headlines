"""
A simple pipeline to deploy a sentiment analysis model on daily newspaper headlines
and write them to a file with a standardized, daily name
"""

import os
from datetime import datetime

import joblib
import sentence_transformers

# Please customize the following variables
USER_NAME = "nicoposner"
VERSION = "1.0.0"


def sentiment_deployment_pipeline(headlines_txt, source):
    """
    A pipeline that takes in a file of daily headlines, and the source of the headlines,
    and runs a pretrained sentiment analysis model on them, writing the results to a file
    with a standardized name unique for each day and source.

    Arguments:
        headlines_txt: utf-8 encoded txt file where each row is a headline from a given source.
        source: the name of the source, such as 'nyt' or 'la_times'

    Other requirements:
        There must be a dumped sentiment model, svm.joblib, in the local directory.

    Returns:
        A utf-8 encouded txt file where each row is the sentiment (Optimistic,
        Pessimistic, or Neutral), a comma, and the original headline.
    """
    if headlines_txt is None or source is None:
        raise ValueError("Both 'headlines_txt' and 'source' arguments are required.")

    # Load the headlines
    with open(headlines_txt, "r", encoding="utf-8") as file:
        headlines = file.readlines()

    # instantiate the same kind of model used in training
    model = sentence_transformers.SentenceTransformer("all-MiniLM-L6-v2")

    # transform the headlines into vectors using this model
    embeddings = model.encode(headlines)  # assuming this is the necessary vector form

    # load the pretrained SVM classifier model in the local directory
    classifier = joblib.load("svm.joblib")

    # predict the labels using the new embeddings
    y_pred = classifier.predict(embeddings)

    # get the date component of the file name
    date_str = os.path.basename(headlines_txt).split("_")[-1].split(".")[0]

    # create a datetime object containing the year, month, and day of the headlines
    date = datetime.strptime(date_str, "%Y-%m-%d")

    # create the name of the file for output
    output_filename = (
        f"nrposner_headline_scores_{source}_{date.year}_{date.month}_{date.day}.txt"
    )

    # write the output file
    with open(output_filename, "w", encoding="utf-8") as output_file:
        for output, head in zip(y_pred, headlines):
            output_file.write(f"{output}, {head}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process headlines from a text file.")
    parser.add_argument(
        "headlines_txt", type=str, help="The path to the headlines text file."
    )
    parser.add_argument("source", type=str, help="The source of the headlines.")
    args = parser.parse_args()

    if not args.headlines_txt or not args.source:
        raise ValueError("Both 'headlines_txt' and 'source' arguments are required.")

    sentiment_deployment_pipeline(args.headlines_txt, args.source)


# def say_hi(msg:str = "Hi!", file_directory:str = "/app/data/") -> None:
#     # Generate timestamp
#     timestamp = datetime.now().strftime("%Y%m%d%H%M")
#
#     # Define filename with timestamp
#     file_name = f"outputfile_{USER_NAME}_{VERSION}_timestamp_{timestamp}.txt"
#     file_path = os.join(file_directory, file_name)
#
#     # Write the timestamp inside the file
#     with open(file_path, "w") as file:
#         file.write(msg)
#
#     print(f"File '{file_path}' created successfully.")
#
# def add_numbers(a:int, b:int) -> int:
#     return a + b
#
# if __name__ == "__main__":
#     say_hi()
