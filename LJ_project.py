import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

st.set_page_config(
    page_title="Pencil Sketch Converter",
    page_icon="✏️",
    layout="wide"
)

st.title("✏️ Pencil Sketch Converter LJ")
st.write("Upload an image and convert it into a pencil sketch.")

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    # Read uploaded image
    image = Image.open(uploaded_file).convert("RGB")
    img_rgb = np.array(image)

    # Convert RGB to BGR for OpenCV
    img = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

    # Sketch settings
    st.sidebar.header("Sketch Settings")

    blur_size = st.sidebar.slider(
        "Blur intensity",
        min_value=3,
        max_value=99,
        value=21,
        step=2
    )

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Invert grayscale
    inverted = 255 - gray

    # Apply Gaussian blur
    blur = cv2.GaussianBlur(
        inverted,
        (blur_size, blur_size),
        0
    )

    # Invert blurred image
    inverted_blur = 255 - blur

    # Create pencil sketch
    sketch = cv2.divide(
        gray,
        inverted_blur,
        scale=256
    )

    # Display images
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(img_rgb, use_container_width=True)

    with col2:
        st.subheader("Pencil Sketch")
        st.image(sketch, clamp=True, use_container_width=True)

    # Convert sketch to downloadable JPG
    success, encoded = cv2.imencode(".jpg", sketch)

    if success:
        st.download_button(
            label="⬇️ Download Pencil Sketch",
            data=encoded.tobytes(),
            file_name="pencil_sketch.jpg",
            mime="image/jpeg"
        )

else:
    st.info("Please upload an image to get started.")

