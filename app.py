import streamlit as st
import tempfile
import os

st.set_page_config(page_title="MP3 Playlist Generator", layout="centered")

st.title("🎵 MP3 플레이리스트 생성기 (웹 버전)")
st.markdown("여러 MP3 파일을 업로드하면 `.m3u` 파일로 만들어줄게!")

uploaded_files = st.file_uploader("MP3 파일들을 업로드하세요 🎶", type="mp3", accept_multiple_files=True)

playlist_name = st.text_input("📛 플레이리스트 이름 (확장자 제외)", "my_playlist")

sort_option = st.selectbox("📑 정렬 방식 선택", ["이름순", "업로드 순"])

if st.button("🎧 플레이리스트 생성"):
    if not uploaded_files:
        st.warning("MP3 파일을 업로드해주세요!")
    elif not playlist_name:
        st.warning("플레이리스트 이름을 입력해주세요!")
    else:
        # 임시 폴더 만들기
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = []
            for file in uploaded_files:
                path = os.path.join(temp_dir, file.name)
                with open(path, "wb") as f:
                    f.write(file.read())
                paths.append(path)

            # 정렬
            if sort_option == "이름순":
                paths.sort()
            elif sort_option == "업로드 순":
                pass  # 업로드 순 = 그대로 유지

            # 플레이리스트 생성
            m3u_path = os.path.join(temp_dir, f"{playlist_name}.m3u")
            with open(m3u_path, "w", encoding="utf-8") as f:
                f.write("#EXTM3U\n")
                for path in paths:
                    f.write(f"{os.path.basename(path)}\n")

            # 다운로드 제공
            with open(m3u_path, "rb") as f:
                st.download_button(
                    label="⬇️ 플레이리스트 다운로드",
                    data=f,
                    file_name=f"{playlist_name}.m3u",
                    mime="text/plain"
                )
