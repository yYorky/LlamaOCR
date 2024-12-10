import os
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from langchain_groq import ChatGroq
import base64
import io
from time import sleep

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def encode_image_pil(image: Image.Image) -> str:
    buffered = io.BytesIO()
    image = image.convert("RGB")
    image.save(buffered, format="JPEG", quality=85)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def split_image_into_horizontal_stripes(image: Image.Image, stripe_count: int = 5, overlap: float = 0.1):
    width, height = image.size
    stripe_height = height // stripe_count
    overlap_height = int(stripe_height * overlap)

    stripes = []
    for i in range(stripe_count):
        upper = max(i * stripe_height - overlap_height, 0)
        lower = min((i + 1) * stripe_height + overlap_height, height)
        stripe = image.crop((0, upper, width, lower))
        stripes.append(stripe)
    return stripes

def ocr(image: Image.Image, model: str = "llama-3.2-90b-vision-preview") -> str:
    groq_llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=model,
        temperature=0
    )

    image_data_url = f"data:image/jpeg;base64,{encode_image_pil(image)}"

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": (
                    "The uploaded image contains both printed text and handwritten notes. "
                    "Your task is to carefully extract all textual content, including handwritten elements."
                )},
                {"type": "image_url", "image_url": {"url": image_data_url}}
            ]
        }
    ]

    response = groq_llm.invoke(messages)
    return response.content.strip()

def format_to_table(markdown_runs: list, model: str = "llama-3.3-70b-versatile") -> str:
    groq_llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=model,
        temperature=0
    )

    combined_markdown = "\n\n".join(markdown_runs)

    messages = [
        {
            "role": "user",
            "content": (
                "You are provided with multiple markdown outputs extracted from overlapping sections of an image."
                "Some sections may contain duplicate or conflicting information due to overlaps. "
                "Your task is to:"
                "\n\n1. Identify and consolidate rows of data that are related, ensuring that the most complete version of the information is retained."
                "\n2. For rows with conflicting information (e.g., different values for a field), prioritize the more detailed entry."
                "\n3. If a field is missing in one row but present in another, combine the information into a single row."
                "\n4. Output the consolidated data in a clean tabular format using Markdown syntax, suitable for direct rendering."
                "\n5. Output Only Markdown: Return solely the Markdown content without any additional explanations or comments."
                "\n\nHere is the data to process:\n\n"
                + combined_markdown
            )
        }
    ]

    response = groq_llm.invoke(messages)
    return response.content.strip()

# Streamlit Application
st.title("OCR to Tabular Data with Llama3.2 Vision Model")
st.markdown("Convert uploaded image content into a structured table format.")

# Sidebar for Upload and Display
with st.sidebar:
    st.markdown("#### Upload Image")
    uploaded_file = st.file_uploader("Upload an image (JPEG, PNG)", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        # Resize image for better display
        width, height = image.size
        new_width, new_height = int(width * 1.2), int(height * 1.2)
        image = image.resize((new_width, new_height))
        
        # Display the image in the sidebar
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        # Preprocess the image
        stripes = split_image_into_horizontal_stripes(image)

# Main Section for Processing and Results
if uploaded_file is not None:
    st.markdown("#### OCR and Results")
    progress_bar = st.progress(0)
    n = 1
    markdown_runs = []
    total_steps = len(stripes) * n
    step = 0

    # Dynamic status box
    status_box = st.empty()

    for run in range(1, n + 1):
        for i, stripe in enumerate(stripes, start=1):
            step += 1
            progress = step / total_steps
            progress_bar.progress(progress)
            status_box.markdown(f"**Processing Stripe {i}, Run {run} ({int(progress * 100)}%)...**")
            sleep(0.1)  # Simulating processing time

            stripe_markdown = ocr(stripe, model="llama-3.2-90b-vision-preview")
            markdown_runs.append(stripe_markdown)

    progress_bar.progress(1.0)
    status_box.markdown("**Processing complete.**")

    # Displaying Results
    table_output = format_to_table(markdown_runs, model="llama-3.3-70b-versatile")
    st.markdown(table_output, unsafe_allow_html=True)

    # Download Button
    st.download_button(
        label="Download Table Output",
        data=table_output.encode('utf-8'),
        file_name="consensus_table.txt",
        mime="text/plain"
    )
else:
    st.markdown("Output will be displayed here after uploading an image.")
