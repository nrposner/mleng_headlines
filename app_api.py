"""
An API for submitting newspaper headlines and getting back the sentiment
classifications of those headlines.
"""

# NOTE: This API only returns the labels, not the headlines themselves.
# This is done to save bandwidth.
# While this certainly does save on bandwidth, the benefits are likely to
# be negligible unless the user is processing an enormous number of headlines.
# Even assuming very long headlines encoded entirely in 4-byte utf-8 characters,
# any single headline is still <<1kb, compared to a heavily-compressed frame
# of HD video at ~30kb, or an uncompressed frame of >10 mb.
# The user would need to be processing a large fraction of all headlines in
# the world in a single command, and they wouldn't be doing that more than a
# couple times a day at most. It's probably unnecessary.

import logging
from flask import Flask, request, jsonify

import joblib
import sentence_transformers

app = Flask(__name__)

# Configure Flask for faster JSON responses
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False

# Load models only once
model = sentence_transformers.SentenceTransformer("all-MiniLM-L6-v2")
classifier = joblib.load("svm.joblib")


# function status, GET type
@app.get("/status")
def status():
    """
    A status checker to determine whether the server is up.
    """
    logging.info("User checked our status")
    return jsonify({"status": "Ok"})


# type POST
@app.post("/score_headlines")
def score_headlines():
    """
    A pipeline that takes in a json request containing newspaper headlines and
    returns a JSON object containing the sentiment classifications of those
    headlines
    """
    try:
        data = request.json
        headlines = data.get("headlines", [])

        if not isinstance(headlines, list) or not all(
            isinstance(h, str) for h in headlines
        ):
            logging.error("Error processing non-list input")
            return jsonify({"error": "Invalid input, expected list of strings"}), 400

        if not headlines:
            logging.error("Error processing empty list")
            return (
                jsonify({"error": "Input is empty, expected at least one headline"}),
                422,
            )

        # transform the headlines into vectors using this model
        embeddings = model.encode(
            headlines
        )  # assuming this is the necessary vector form

        # predict the labels using the new embeddings
        y_pred = classifier.predict(embeddings)  # do they get returned as a list?
        labels = list(y_pred)

        return jsonify({"labels": labels})

    except ValueError as ve:
        logging.exception("Error processing request")
        return jsonify({"error": str(ve)}), 500
    except TypeError as te:
        logging.exception("Error processing request")
        return jsonify({"error": str(te)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8083)
