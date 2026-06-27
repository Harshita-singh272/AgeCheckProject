from deepface import DeepFace


def predict_age(image_path):
    """
    Predict age from an image using DeepFace.
    """

    result = DeepFace.analyze(
        img_path=image_path,
        actions=["age"],
        enforce_detection=False
    )

    age = result[0]["age"]

    return age