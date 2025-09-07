import streamlit as st
import zipfile
import io

def extract_accounts(lines, keywords):
    results = {kw: set() for kw in keywords}
    for line in lines:
        parts = line.strip().split(":")
        if len(parts) >= 3:
            tk = parts[-2]
            mk = parts[-1]
            for kw in keywords:
                if kw.lower() in line.lower():  # check cả dòng
                    results[kw].add(f"{tk}:{mk}")
    return results

st.title("🔎 Account Extractor Tool")
st.write("Upload file .txt dạng `url:tk:mk` và chọn từ khóa để lọc.")

uploaded_file = st.file_uploader("Chọn file .txt", type=["txt"])
keywords_input = st.text_input("Nhập từ khóa (cách nhau bởi dấu phẩy)", "garena,roblox,epicgames")

if uploaded_file and keywords_input:
    keywords = [kw.strip() for kw in keywords_input.split(",") if kw.strip()]
    lines = uploaded_file.getvalue().decode("utf-8", errors="ignore").splitlines()

    if st.button("Bắt đầu lọc"):
        with st.spinner("Đang xử lý..."):
            results = extract_accounts(lines, keywords)

        # Hiển thị kết quả từng từ khóa
        for kw in keywords:
            accounts = sorted(results[kw])
            st.subheader(f"Kết quả cho **{kw}** ({len(accounts)} dòng)")
            if accounts:
                st.download_button(
                    label=f"Tải {kw}_accounts.txt",
                    data="\n".join(accounts),
                    file_name=f"{kw}_accounts.txt",
                    mime="text/plain",
                )
            else:
                st.info(f"❌ Không tìm thấy dữ liệu cho {kw}")

        # Tạo file ZIP chứa tất cả kết quả
        if any(results[kw] for kw in keywords):
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for kw in keywords:
                    accounts = sorted(results[kw])
                    if accounts:
                        zip_file.writestr(f"{kw}_accounts.txt", "\n".join(accounts))
            zip_buffer.seek(0)

            st.download_button(
                label="⬇️ Tải tất cả kết quả (ZIP)",
                data=zip_buffer,
                file_name="all_accounts.zip",
                mime="application/zip",
            )
