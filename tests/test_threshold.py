from app.services import estimate_age, check_threshold

image_path = "data/test_images/image.png"

age = estimate_age(image_path)

print("Predicted Age:", age)

result = check_threshold(age, 18)

assert "decision" in result
assert "is_above_threshold" in result
assert "confidence" in result

print("Integration Test Passed")

result = check_threshold(25, 18)
assert result["decision"] == "PASS"
assert result["is_above_threshold"] == True

result = check_threshold(15, 18)
assert result["decision"] == "FAIL"
assert result["is_above_threshold"] == False

result = check_threshold(60, 21)
assert result["decision"] == "PASS"
assert result["is_above_threshold"] == True

result = check_threshold(12, 18)
assert result["decision"] == "FAIL"
assert result["is_above_threshold"] == False

print("All Unit Tests Passed")