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

    if isinstance(result, list):
        return result[0]["age"]

    return result["age"]

def estimate_age(image_path):
    return predict_age(image_path)

def check_threshold(age, threshold):
    difference = abs(age - threshold)

    if difference <= 2:
        decision = "INCONCLUSIVE"
    elif age >= threshold:
        decision = "PASS"
    else:
        decision = "FAIL"

    confidence = min(50 + difference * 5, 100)

    return {
        "decision": decision,
        "is_above_threshold": age >= threshold,
        "confidence": confidence
    }