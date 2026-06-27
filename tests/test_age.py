from app.services import predict_age

image_path = "data/test_images/image.jpg"

age = predict_age(image_path)

print(f"Predicted Age: {age}")