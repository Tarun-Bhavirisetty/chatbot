import streamlit as st
import os
import shutil

st.title("Admin Upload Panel")

password = st.text_input("Enter Admin Password", type="password")

if password != "admin123":
    st.warning("Admin access only")
    st.stop()

os.makedirs("data/uploads", exist_ok=True)

uploaded_file = st.file_uploader(
    "Upload Dataset",
    type=["xlsx","csv","pdf","docx"]
)

if uploaded_file:

    save_path = os.path.join(
        "data/uploads",
        uploaded_file.name
    )

    with open(save_path,"wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File uploaded successfully")

st.subheader("Uploaded Files")

files = os.listdir("data/uploads")

for file in files:
    st.write(file)

st.subheader("Delete File")

if files:

    file_to_delete = st.selectbox("Select file", files)

    if st.button("Delete File"):
        os.remove(f"data/uploads/{file_to_delete}")
        st.success("File deleted")

if st.button("🔄 Rebuild Knowledge Base"):

    if os.path.exists("faiss_index"):
        shutil.rmtree("faiss_index")

    st.success("Vector database deleted. It will rebuild automatically.")

st.subheader("📊 Question Analytics")

log_file = "data/logs/questions.log"

if os.path.exists(log_file):

    with open(log_file) as f:
        logs = f.readlines()

    st.write("Total Questions:", len(logs))

    for log in logs[-10:]:
        st.write(log)