import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Review",
    page_icon="./image/alpaca.jpg",
    layout="wide"
)

# 헤더 이미지 표시
header_image = Image.open("image/header2.jpg")
st.image(header_image, use_column_width=True)

st.subheader("")
st.title("이온에 대해 배웠던 내용 😅")
st.header("✅ 슬라이드쇼")

# 슬라이드 이미지 파일 경로 리스트
image_files = [f"image/review{i}.jpg" for i in range(1, 9)]

# 교사의 설명 리스트 (슬라이드별 설명)
teacher_notes = [
    "1. 리튬의 원자핵의 전하량은 원소 번호를 의미합니다. 원자는 (+)전하량과 (-)전하량이 동일하여 중성입니다.",
    "2. 양이온은 원자가 전자를 잃어서 생성됩니다.",
    "3. 음이온은 원자가 전자를 얻어서 생성됩니다.",
    "4. 양이온의 이온식 규칙입니다.",
    "5. 음이온의 이온식 규칙입니다.",
    "6. 다양힌 이온식입니다. 항상 규칙을 따르지는 않아요!",
    "7. 이온이 담긴 수용액에서는 양전하와 음전하로 나뉘어 전기가 통합니다.",
    "8. 교과서에 나온 중요한 앙금 생성 반응 3가지입니다 :)."
]

# 현재 이미지 인덱스를 저장하기 위한 상태 설정
if 'index' not in st.session_state:
    st.session_state.index = 0

# 버튼을 위한 열 만들기
col1, col2 = st.columns([1, 1])

# 이전 이미지 버튼 클릭 시 인덱스 감소
with col1:
    if st.button("이전 이미지"):
        st.session_state.index = (st.session_state.index - 1) % len(image_files)

# 다음 이미지 버튼 클릭 시 인덱스 증가
with col2:
    if st.button("다음 이미지"):
        st.session_state.index = (st.session_state.index + 1) % len(image_files)

# 슬라이드 이미지와 설명 표시
st.image(image_files[st.session_state.index], width=600)
st.write(teacher_notes[st.session_state.index])
