import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/check_age"

st.title("Age Verification System")

st.header("Upload Image")

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    st.subheader("Selected Image")
    st.image(uploaded_file)

st.header("Age Threshold")

threshold = st.number_input(
    "Age Threshold",
    min_value=1,
    max_value=100,
    value=18
)

check_button = st.button("Check Age")

st.header("Result")

if check_button:

    if uploaded_file is None:
        st.warning("Please upload an image.")

    else:

        files = {
            "image": (
                uploaded_file.name,
                uploaded_file,
                uploaded_file.type
            )
        }

        data = {
            "threshold": str(threshold)
        }

        try:

            response = requests.post(
                API_URL,
                files=files,
                data=data
            )

            result = response.json()

            decision = result["decision"]
            confidence = result["confidence"]

            st.subheader("Verification Result")

            if decision == "PASS":
                st.success("✅ PASS")
            else:
                st.error("❌ FAIL")

            st.metric(
                label="Confidence",
                value=f"{confidence}%"
            )

        except Exception as e:
            st.error(f"Error: {e}")