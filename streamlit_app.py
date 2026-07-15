import random

import streamlit as st


QUESTIONS = [
    {"korean": "행복한", "answer": "happy", "choices": ["happy", "angry", "sleepy", "heavy"]},
    {"korean": "친구", "answer": "friend", "choices": ["friend", "enemy", "ghost", "river"]},
    {"korean": "여행하다", "answer": "travel", "choices": ["travel", "build", "listen", "borrow"]},
    {"korean": "배우다", "answer": "learn", "choices": ["learn", "cook", "drop", "guess"]},
    {"korean": "발견하다", "answer": "discover", "choices": ["discover", "remember", "invite", "break"]},
    {"korean": "도와주다", "answer": "help", "choices": ["help", "climb", "push", "throw"]},
    {"korean": "큰", "answer": "big", "choices": ["big", "small", "thin", "short"]},
    {"korean": "공부하다", "answer": "study", "choices": ["study", "play", "sleep", "eat"]},
    {"korean": "읽다", "answer": "read", "choices": ["read", "write", "run", "jump"]},
    {"korean": "좋아하다", "answer": "like", "choices": ["like", "hate", "mean", "find"]},
]


def build_questions():
    questions = []
    for item in QUESTIONS:
        new_item = dict(item)
        new_item["choices"] = item["choices"][:]
        random.shuffle(new_item["choices"])
        questions.append(new_item)
    random.shuffle(questions)
    return questions


if "questions" not in st.session_state:
    st.session_state.questions = build_questions()
    st.session_state.score = 0
    st.session_state.current_index = 0
    st.session_state.answer_checked = False
    st.session_state.finished = False


st.set_page_config(page_title="영단어 게임", page_icon="📚", layout="centered")
st.title("📚 영어 단어 맞추기 게임")
st.write("뜻에 맞는 영어 단어를 고르세요. 중학생 수준의 쉬운 단어들입니다.")

if st.session_state.finished:
    st.success(f"게임이 끝났습니다! 총 {len(st.session_state.questions)}문제 중 {st.session_state.score}문제를 맞혔어요.")
    if st.button("다시 시작"):
        st.session_state.questions = build_questions()
        st.session_state.score = 0
        st.session_state.current_index = 0
        st.session_state.answer_checked = False
        st.session_state.finished = False
        st.rerun()
    st.stop()

current_question = st.session_state.questions[st.session_state.current_index]
progress = (st.session_state.current_index + 1) / len(st.session_state.questions)
st.progress(progress)
st.caption(f"점수: {st.session_state.score} / {len(st.session_state.questions)}")

st.subheader(f"{st.session_state.current_index + 1}번 문제")
st.write(f"뜻: {current_question['korean']}")

widget_key = f"choice_{st.session_state.current_index}"
choice = st.radio(
    "정답을 선택하세요.",
    current_question["choices"],
    key=widget_key,
    index=None,
    horizontal=False,
)

if choice is not None and not st.session_state.answer_checked:
    if choice == current_question["answer"]:
        st.session_state.score += 1
        st.success("정답입니다! 👍")
    else:
        st.error(f"아쉽네요. 정답은 '{current_question['answer']}'입니다.")

    st.session_state.answer_checked = True
    if st.session_state.current_index < len(st.session_state.questions) - 1:
        st.session_state.current_index += 1
        st.session_state.answer_checked = False
        st.rerun()
    else:
        st.session_state.finished = True
        st.rerun()
