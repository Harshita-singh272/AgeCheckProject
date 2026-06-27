# from app.services import (
#     load_image,
#     get_image_info,
#     preprocess_image
# )

# image = load_image("data/test_images/image.png")


# print("Image Info:")
# print(get_image_info(image))

# processed = preprocess_image(
#     "data/test_images/image.png"
# )

# print("\nProcessed Image Shape:")
# print(processed.shape)
# print(processed.dtype)
# print(processed.min())
# print(processed.max())

from app.services import (
    load_image,
    get_image_info,
    preprocess_image
)

test_images = [
    "data/test_images/image.png",
    "data/test_images/image.jpg",
    "data/test_images/grayscale.jpg",
    "data/test_images/grayscale2.jpg",
    "data/test_images/fake.jpg"
]

for image_path in test_images:
    print(f"\nTesting: {image_path}")

    try:
        image = load_image(image_path)

        print("Image Info:")
        print(get_image_info(image))

        processed = preprocess_image(image_path)

        print("Processed Image Shape:")
        print(processed.shape)

        print("Data Type:")
        print(processed.dtype)

        print("Min Pixel Value:")
        print(processed.min())

        print("Max Pixel Value:")
        print(processed.max())

        print("PASS")

    except Exception as e:
        print(f"FAIL: {e}")