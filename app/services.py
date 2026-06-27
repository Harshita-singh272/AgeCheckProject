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
    preprocess_image(image_path)
    return predict_age(image_path)
def check_threshold(age, threshold):
    is_above_threshold = age >= threshold

    decision = "PASS" if is_above_threshold else "FAIL"

    confidence = min(
        round(abs(age - threshold) / max(threshold, 1), 2),
        1.0
    )

    return {
        "decision": decision,
        "is_above_threshold": is_above_threshold,
        "confidence": confidence
    }