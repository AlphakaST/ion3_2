import streamlit as st
from st_pages import Page, show_pages
from PIL import Image

import pandas as pd
import mysql.connector
from openai import OpenAI

st.set_page_config(
    page_title="이온과 앙금 생성 반응",
    page_icon="./image/alpaca.jpg",
    layout="wide"
)

image = Image.open("image/header2.jpg")
st.image(image)
st.subheader("")
st.title("학생 답안 제출 양식")
st.divider()
st.header("5문제의 서술형 답안을 제출하세요")

# OpenAI API 키 설정
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# MySQL 연결 설정
db_config = {
    'host': st.secrets["connections"]["mysql"]["host"],
    'user': st.secrets["connections"]["mysql"]["username"],
    'password': st.secrets["connections"]["mysql"]["password"],
    'database': st.secrets["connections"]["mysql"]["database"],
    'port': st.secrets["connections"]["mysql"]["port"]
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# 데이터 읽기 함수
def read_existing_data():
    query = "SELECT * FROM student_responses_3"
    cursor.execute(query)
    result = cursor.fetchall()
    columns = cursor.column_names
    return pd.DataFrame(result, columns=columns)

existing_data = read_existing_data()

hints = {
    "1": "힌트: (+)전하와 (-)전하의 총량을 비교해 볼까요?",
    "2": "힌트: 원자핵의 전하량은 원소 번호와 동일합니다!",
    "3": "힌트: (-)극과 (+)극에는 각각 어떤 이온이 이동할까요?",
    "4": "힌트: Ca2+와 CO32-는 앙금 생성을 합니다. 나머지는 어떻게 될까요?",
    "5": "힌트: 생성된 앙금은 납과 아이오딘으로 구성되었고, 전기는 이온의 존재 유무와 관련 있습니다!"
}

example_answers = {
    "1": "원자는 (+)전하량과 (-)전하량의 총량이 같기 때문에 중성이다. 그리고 이온이란 원자에서 전자를 얻거나 잃어서 생긴 물질이다.",
    "2": "Ca2+이다. 원자핵의 전하량이 20이라는 것은 원소 번호가 20번이므로, Ca(칼슘)이고, 잃은 전자수가 2개 이므로 Ca2+이다.",
    "3": "(-)극에는 나트륨 이온(혹은 Na+)가 이동하고, (+)극에는 염화 이온(혹은 Cl-)이 이동한다. 따라서 전기가 통한다.",
    "4": "반응 결과, 칼슘 이온(혹은 Ca2+)과 탄산 이온(혹은 CO32- 혹은 CO3^2-)이 반응하여 탄산 칼슘(혹은 CaCO3)이 생성된다. 추가적으로 나트륨 이온(혹은 Na+)과 염화 이온(혹은 Cl-)은 반응하지 않고 혼합 용액에 남아 있다.",
    "5": "생성된 앙금은 아이오딘화 납(혹은 PbI2)이다. 혼합 용액에는 전기가 통한다. 그 까닭은, 반응에 참여하지 않은 질산 이온(혹은 NO3-)과 칼륨 이온(K+)이 남아 있기 때문이다."
}

# 힌트 상태 초기화
if 'show_hints' not in st.session_state:
    st.session_state.show_hints = [False] * 5

with st.form(key="Feedback_form"):
    student_id = st.text_input("**학번을 입력하세요**", placeholder="예: 1학년 1반 5번 -> 10105, 1학년 1반 30번 -> 10130)")

    # st.image("number1.jpg", caption="문제1", use_column_width=True)
    answer1 = st.text_area("**1. 원자가 중성인 이유는 무엇인지, 그리고 이온이란 무엇인지 서술하시오.**")
    
    
    # 문제 1에 대한 힌트
    submit_button1 = st.form_submit_button(label='힌트1')
    if submit_button1:
        st.session_state.show_hints[0] = not st.session_state.show_hints[0]
    if st.session_state.show_hints[0]:
        st.write(hints["1"])

    # st.image("number2.jpg", caption="문제2", use_column_width=True)
    answer2 = st.text_area("**2. 원자핵의 전하량이 20이고, 잃은 전자수가 2개일 때, 해당 이온의 실제 이온식을 쓰고, 그 과정을 서술하시오.**")
    
    # 문제 2에 대한 힌트
    submit_button2 = st.form_submit_button(label='힌트2')
    if submit_button2:
        st.session_state.show_hints[1] = not st.session_state.show_hints[1]
    if st.session_state.show_hints[1]:
        st.write(hints["2"])

    st.image("number3.jpg", caption="문제3", use_column_width=True)
    answer3 = st.text_area("**3. 그림은 염화 나트륨 수용액에 (-)극과 (+)극의 전원을 연결했을 때의 모습이다. 수용액에는 어떤 일이 발생하는지 서술하시오.**")
    
    # 문제 3에 대한 힌트
    submit_button3 = st.form_submit_button(label='힌트3')
    if submit_button3:
        st.session_state.show_hints[2] = not st.session_state.show_hints[2]
    if st.session_state.show_hints[2]:
        st.write(hints["3"])

    st.image("number4.jpg", caption="문제4", use_column_width=True)
    answer4 = st.text_area("**4. 그림은 염화 칼슘 수용액과 탄산 나트륨 수용액을 섞어 혼합 용액을 만드는 과정이다. 반응 결과를 2줄 이내로 서술하시오.**")
    
    # 문제 4에 대한 힌트
    submit_button4 = st.form_submit_button(label='힌트4')
    if submit_button4:
        st.session_state.show_hints[3] = not st.session_state.show_hints[3]
    if st.session_state.show_hints[3]:
        st.write(hints["4"])

    st.image("number5.jpg", caption="문제5", use_column_width=True)
    answer5 = st.text_area("**5. 그림은 질산 납 수용액과 질산 나트륨 수용액을 섞었을 때의 모습이다. 생성된 앙금을 쓰시오. 또한, 혼합 용액에 전기가 통하는지 안 통하는지 쓰고, 그 까닭에 대해서도 서술하시오.**")
    
    # 문제 5에 대한 힌트
    submit_button5 = st.form_submit_button(label='힌트5')
    if submit_button5:
        st.session_state.show_hints[4] = not st.session_state.show_hints[4]
    if st.session_state.show_hints[4]:
        st.write(hints["5"])

    submit_button = st.form_submit_button(label='제출하기')

    if submit_button:
        if len(student_id) != 5 or not student_id.isdigit():
            st.error("학번은 5자리 숫자로 입력해야 합니다. 다시 시도해 주세요.")
        elif not (answer1.strip() and answer2.strip() and answer3.strip() and answer4.strip() and answer5.strip()):
            st.error("모든 문항에 답변을 입력해 주세요.")
        else:
            feedbacks = []
            for i, (answer, example_answer) in enumerate(zip([answer1, answer2, answer3, answer4, answer5], 
                                                             [example_answers["1"], example_answers["2"], example_answers["3"], 
                                                              example_answers["4"], example_answers["5"]])):
                prompt = (f"학생 답안: {answer}\n\n"
                          f"예시 답안: {example_answer}\n\n"
                          f"채점 기준: 예시 답안과 비교하여, 학생 답안이 맞는지 확인하고, 틀린 부분이 있다면 어떤 부분을 공부해야 하는지 간단히 설명해 주세요. "
                          f"feedback을 줄 때는, 다음과 같은 양식을 따라서 답변해 주세요. 1) 정답인지 아닌지(예: 맞음, 틀림, 보완이 필요함), 2) 틀리거나 보완이 필요하다면, 예시 답안과 학생 답안을 비교하여 어떤 부분을 보완하고 공부해야 하는지 설명"
                          f"학생 답안이 예시 답안과 정확히 일치하지 않더라도, 내용이 맞다면 간단히 이유를 설명해 주세요."
                          f"학생 답안과 예시 답안을 비교할 때, 동의어와 다양한 표현을 고려하여 평가해 주세요."
                          f"현재 feedback 받는 대상은 중학생이며, 학습 내용 수준은 '이온의 정의와 이온식 작성, 전기를 통한 이온 확인 방법, 앙금 생성 반응으로 특정 이온 확인하기'를 학습한 상태임을 고려해서 수준에 맞게 답변해줘."
                          f"내용 설명은 최대 200자 이내로 요약하여 제한하고, 설명할 때 교사가 학생에게 대하듯 친절하게 설명해 주세요.")

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that provides feedback based on given criteria."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1,
                    max_tokens=200
                )
                feedback = response.choices[0].message.content.strip()
                feedbacks.append(feedback)

            feedback_data = pd.DataFrame(
                [
                    {
                        "student_id": student_id,
                        "number1": answer1,
                        "number2": answer2,
                        "number3": answer3,
                        "number4": answer4,
                        "number5": answer5,
                        "feedback1": feedbacks[0],
                        "feedback2": feedbacks[1],
                        "feedback3": feedbacks[2],
                        "feedback4": feedbacks[3],
                        "feedback5": feedbacks[4]
                    }
                ]
            )

            # 학생에게 피드백 보여주기
            st.subheader("제출한 답안에 대한 피드백:")
            for i in range(1, 6):
                st.write(f"문제 {i}: {feedbacks[i-1]}")

            # 기존 데이터에 새로운 데이터 추가
            for row in feedback_data.itertuples(index=False):
                cursor.execute(
                    """
                    INSERT INTO student_responses_3 (student_id, number1, number2, number3, number4, number5, feedback1, feedback2, feedback3, feedback4, feedback5)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    row
                )
            conn.commit()

            st.success("답안이 성공적으로 제출되었습니다!")

cursor.close()
conn.close()


# 다른 페이지 표시(side)
show_pages(
    [
        Page("app1_0.py", "복습하기", ":white_check_mark:"),
        Page("app1_1.py", "종합 평가", ":100:"),
    ]
)
