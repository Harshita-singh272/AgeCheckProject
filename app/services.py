import cv2
import os
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



def load_image(image_path):

    if not os.path.exists(image_path):
        raise FileNotFoundError(
            f"File not found: {image_path}"
        )

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(
            "Invalid or corrupted image"
        )

    return image

def get_image_info(image):
    if len(image.shape) == 2:
        height, width = image.shape
        channels = 1
    else:
        height, width, channels = image.shape

    return {
        "width": width,
        "height": height,
        "channels": channels
    }

def convert_to_rgb(image):

    if len(image.shape) == 2:
        return cv2.cvtColor(
            image,
            cv2.COLOR_GRAY2RGB
        )

    return cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

def resize_image(
    image,
    width=224,
    height=224
):
    return cv2.resize(
        image,
        (width, height)
    )

def normalize_image(image):
    return image / 255.0

def preprocess_image(image_path):

    image = load_image(image_path)

    image = convert_to_rgb(image)

    image = resize_image(image)

    image = normalize_image(image)

    return image

def estimate_age(image_path):
    processed_image = preprocess_image(image_path)
    return predict_age(processed_image)

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