import streamlit as st
from PIL import Image, ImageOps
import requests
from io import BytesIO
import io

# Function to process product image to 1200x800 with a white background
def process_product_image(image_url):
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code != 200:
            return None, "Error: Unable to fetch the image from the provided URL."

        img = Image.open(BytesIO(response.content)).convert("RGBA")

        # Check if image resolution is sufficient
        if img.size[0] < 500 or img.size[1] < 500:
            return None, "Error: Image resolution is too low. Minimum required: 500x500 pixels."

        # Create white background
        base_width, base_height = 1200, 800
        white_canvas = Image.new("RGB", (base_width, base_height), (255, 255, 255))

        # Resize image while maintaining aspect ratio
        img.thumbnail((base_width - 100, base_height - 100), Image.LANCZOS)

        # Center the resized image on the white background
        x_offset = (base_width - img.size[0]) // 2
        y_offset = (base_height - img.size[1]) // 2
        white_canvas.paste(img.convert("RGB"), (x_offset, y_offset))

        return white_canvas, None

    except Exception as e:
        return None, f"Error processing image: {str(e)}"

# Streamlit Web App UI
def main():
    st.title("Deliveroo Image Processor")
    st.write("Paste an image URL to process it into a Deliveroo-compatible format (1200x800 pixels).")

    image_url = st.text_input("Paste Image URL:")

    if st.button("Process Image"):
        if image_url:
            processed_img, error_msg = process_product_image(image_url)

            if error_msg:
                st.error(error_msg)
            else:
                st.subheader("Processed Product Image:")
                st.image(processed_img, caption="Formatted Image", use_column_width=True)

                # Convert image to bytes for download
                img_byte_arr = io.BytesIO()
                processed_img.save(img_byte_arr, format="JPEG", quality=100)
                img_byte_arr = img_byte_arr.getvalue()

                st.download_button(
                    label="Download Processed Image",
                    data=img_byte_arr,
                    file_name="formatted_product.jpg",
                    mime="image/jpeg"
                )
        else:
            st.error("Please enter a valid image URL.")

if __name__ == "__main__":
    main()
