![](https://developer-blogs.nvidia.com/wp-content/uploads/2024/10/image1.jpg)

# OCR to Tabular Data with Llama3.2 Vision Model

## Overview
This project leverages the powerful capabilities of the Llama3.2 Vision Model to extract textual data from images, specifically tailored for **invoice processing**. Designed with accountants in mind, this tool converts invoices into structured, machine-readable tabular data, enabling seamless integration with accounting ERP systems.

As a former accountant, I deeply understand the challenges of manually processing invoices—it's time-consuming, error-prone, and repetitive. This project is my effort to bridge the gap between manual invoice entry and efficient automation, improving productivity and accuracy for accountants and finance professionals.

## Features

![](https://raw.githubusercontent.com/yYorky/LlamaOCR/refs/heads/main/static/app_v6-GoogleChrome2024-12-1011-23-35-ezgif.com-crop.gif)

- **Highly Accurate OCR**: Optimized for extracting text from invoices, including handwritten notes.
- **Table Formatting**: Automatically formats extracted data into structured tables.
- **ERP Integration Ready**: Outputs data in tabular format, ideal for integration with ERP systems.
- **Interactive Interface**: Simple and intuitive Streamlit-based web application with a sidebar for image uploads.
- **Progress Updates**: Real-time progress updates during OCR processing.
- **Supports Overlapping Image Stripes**: Splits images into overlapping sections for improved accuracy on large invoices.

## Sources and Inspiration
This project draws inspiration and insights from:
- **[Llama-OCR](https://llamaocr.com/):** A tool that processes documents such as receipts and PDFs containing tables and charts, converting them into Markdown while preserving structure and formatting.
- **[LlamaOCR - Building your Own Private OCR System](https://www.youtube.com/watch?v=5vScHI8F_xo)** by Sam Witteveen:  
  A comprehensive video demonstrating the use of LlamaOCR and its capabilities. It highlights how the Llama 3.2 visual model can convert images and scanned documents into structured Markdown, retaining the formatting of elements like tables, lists, and spreadsheets. Practical tutorials and code snippets are provided in JavaScript and Python, including hands-on examples in a Colab environment.

## How It Works
1. **Upload Invoice**: Users upload an invoice (JPEG or PNG format) via the sidebar.
2. **Image Preprocessing**: The tool splits the image into overlapping horizontal stripes for better accuracy.
3. **Text Extraction**: Leverages Llama3.2 Vision Model to process each stripe and extract text.
4. **Tabular Conversion**: Aggregates and formats the extracted text into a structured table.
5. **Downloadable Output**: Users can download the table in CSV format for easy integration with ERP systems.

## Motivation
During my career as an accountant, I spent countless hours manually processing invoices, reconciling numbers, and ensuring data accuracy in ERP systems. While these tasks were critical, they were also tedious and repetitive. This experience inspired me to create a solution that could automate these processes, enabling accountants to focus on more strategic work. It is truly amazing in the open-source world we live in today that I can have the opportunity to work on this directly to solve for a problem I use to face!

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- [Streamlit](https://streamlit.io/)
- An active API key for the [Llama3.2 Vision Model] from Groq(https://console.groq.com/docs/overview)

### Installation Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yYorky/LlamaOCR.git
   cd llamaocr
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up API Key**:
   Create a `.env` file in the root directory and add your GROQ API key:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

4. **Run the Application**:
   ```bash
   streamlit run app_v6.py
   ```

5. **Access the App**:
   Open [http://localhost:8501](http://localhost:8501) in your browser.

## Usage
1. **Upload Invoice**:
   - Use the sidebar to upload an image of an invoice (JPEG or PNG).
   - The uploaded image will be displayed in the sidebar for review.

2. **OCR Processing**:
   - The main screen will show the processing progress with real-time updates for each section of the invoice.

3. **Download Results**:
   - Once processing is complete, the extracted data will be displayed as a table.
   - Use the "Download Table Output" button to download the data file.

## Testing
To test the application:
1. Use sample invoice images, including those with:
   - Printed text
   - Handwritten notes
   - Complex layouts (e.g., multi-column or detailed itemizations)
2. Verify that the output table matches the original invoice details.
3. Test the download functionality.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for suggestions or improvements.
