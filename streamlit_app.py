import streamlit as st
import pypandoc
import os
import pathlib

# Set page configuration
st.set_page_config(page_title="Word to HTML Converter", page_icon="📄")

# App Title & Description
st.title("📄 Word to HTML Converter")
st.write("""
Upload a Microsoft Word document (**docx**), and this tool will convert it to a **clean HTML file**.
*   ✅ Preserves **Equations** (MathML)
*   ✅ Embeds **Images** (Base64)
""")

# File Uploader
uploaded_file = st.file_uploader("Choose a Word file", type="docx")

if uploaded_file is not None:
    # Create a temporary path to save the uploaded file
    input_path = "temp_input.docx"
    output_path = "converted_document.html"

    # Save uploaded file to disk temporarily
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Button to trigger conversion
    if st.button("🚀 Convert Now"):
        with st.spinner('Converting... This may take a moment.'):
            try:
                # Convert the file
                # CHANGED: Used '--self-contained' instead of '--embed-resources'
                # This ensures compatibility with older Pandoc versions on servers.
                pypandoc.convert_file(
                    input_path,
                    "html",
                    outputfile=output_path,
                    extra_args=["--mathml", "--self-contained"]
                )
                
                # Success Message
                st.success("✅ Conversion Complete!")

                # Read the result to allow download
                with open(output_path, "rb") as file:
                    btn = st.download_button(
                        label="📥 Download HTML File",
                        data=file,
                        file_name=pathlib.Path(uploaded_file.name).with_suffix(".html").name,
                        mime="text/html"
                    )

            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
                st.info("Debugging Info: Ensure 'pandoc' is installed in packages.txt")
