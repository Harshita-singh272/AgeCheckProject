from app.services import estimate_age

image_path = "data/test_images/image.jpg" \
""

age = estimate_age(image_path)

print(f"Estimated Age: {age}")