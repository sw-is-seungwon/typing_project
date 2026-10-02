import streamlit as st
from supabase import create_client
import random
import json
import time
import html


# =========================================================
# 1. 기본 설정
# =========================================================

st.set_page_config(
    page_title="Python Typing Garden",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# 2. Supabase 연결
# =========================================================

@st.cache_resource
def init_supabase():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_SECRET_KEY"]

    return create_client(url, key)


supabase = init_supabase()


# =========================================================
# 3. JSON 문제 불러오기
# =========================================================

@st.cache_data
def load_commands():

    with open(
        "data/commands.json",
        "r",
        encoding="utf-8"
    ) as f:
        data = json.load(f)

    return data["commands"]


commands = load_commands()


# =========================================================
# 4. Session State 초기화
# =========================================================

defaults = {
    "page": "home",
    "room_code": None,
    "nickname": None,
    "student_id": None,
    "team": None,
    "current_command": None,
    "teacher_room": None
}


for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# 5. 전체 디자인
# =========================================================

st.markdown(
"""
<style>

/* ======================================================
   전체 배경
====================================================== */

.stApp {
    background:
        linear-gradient(
            to bottom,
            #DDF3FF 0%,
            #EAF8FF 62%,
            #DDEFD4 62%,
            #CDE7C4 100%
        );

    color: #4E6875;
}


/* 기본 화면 폭 */

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* ======================================================
   제목
====================================================== */

.main-title {
    text-align: center;
    font-size: 3.2rem;
    font-weight: 800;
    color: #54798C;
    margin-top: 10px;
    margin-bottom: 5px;
}


.subtitle {
    text-align: center;
    color: #7896A5;
    font-size: 1.05rem;
    margin-bottom: 32px;
}


/* ======================================================
   일반 카드
====================================================== */

.garden-card {
    background: rgba(255, 255, 255, 0.88);
    border: 1px solid rgba(255,255,255,0.9);
    border-radius: 25px;
    padding: 25px;

    box-shadow:
        0px 8px 25px
        rgba(80,120,140,0.10);
}


/* ======================================================
   방 코드
====================================================== */

.room-code {
    text-align: center;
    font-size: 5rem;
    font-weight: 800;
    color: #648DA1;
    letter-spacing: 10px;
    padding: 10px;
}


/* ======================================================
   학생 게임 하늘
====================================================== */

.sky-game {

    height: 350px;

    position: relative;

    overflow: hidden;

    border-radius: 28px;

    background:
        linear-gradient(
            to bottom,
            #CDEEFF 0%,
            #E9F8FF 75%,
            #F4FCFF 100%
        );

    box-shadow:
        inset 0 0 30px
        rgba(120,190,220,0.15),
        0px 8px 20px
        rgba(70,110,130,0.08);

    margin-bottom: 15px;
}


/* ======================================================
   구름
====================================================== */

.cloud-one {

    position: absolute;

    top: 35px;

    left: 12%;

    font-size: 58px;

    opacity: 0.75;
}


.cloud-two {

    position: absolute;

    top: 85px;

    right: 15%;

    font-size: 48px;

    opacity: 0.65;
}


/* 작은 해 */

.sun {

    position: absolute;

    top: 28px;

    right: 7%;

    font-size: 42px;

    opacity: 0.85;
}


/* ======================================================
   떨어지는 코드
====================================================== */

.falling-code {

    position: absolute;

    left: 50%;

    transform: translateX(-50%);

    background:
        rgba(255,255,255,0.96);

    color:
        #4F6978;

    font-family:
        "Courier New",
        monospace;

    font-size: 1.45rem;

    font-weight: bold;

    padding:
        15px 26px;

    border-radius:
        18px;

    border:
        1px solid
        rgba(150,200,220,0.35);

    box-shadow:
        0 7px 18px
        rgba(70,110,130,0.15);

    white-space:
        nowrap;

    animation:
        falling 9s
        linear infinite;
}


@keyframes falling {

    0% {
        top: -70px;
    }

    100% {
        top: 275px;
    }

}


/* ======================================================
   들판
====================================================== */

.field {

    position: absolute;

    bottom: 0;

    left: 0;

    width: 100%;

    height: 65px;

    background:
        #C9E6BD;

    border-radius:
        55% 55% 0 0;

    text-align:
        center;

    font-size:
        26px;

    padding-top:
        15px;
}


/* ======================================================
   팀 카드
====================================================== */

.team-card {

    background:
        rgba(255,255,255,0.88);

    border-radius:
        18px;

    padding:
        16px;

    margin-bottom:
        10px;

    border:
        1px solid
        rgba(255,255,255,0.9);

    box-shadow:
        0 5px 15px
        rgba(80,120,140,0.08);
}


.team-number {

    font-size:
        1.05rem;

    color:
        #718A94;

    margin-bottom:
        4px;
}


.team-score {

    font-size:
        1.8rem;

    font-weight:
        bold;

    color:
        #527A68;
}


/* ======================================================
   대기 화면
====================================================== */

.waiting-box {

    text-align:
        center;

    background:
        rgba(255,255,255,0.80);

    border-radius:
        25px;

    padding:
        35px;

    margin-top:
        20px;

    box-shadow:
        0 7px 20px
        rgba(80,120,140,0.08);
}


.waiting-cloud {

    font-size:
        65px;

    margin-bottom:
        10px;
}


/* ======================================================
   버튼
====================================================== */

.stButton > button,
.stFormSubmitButton > button {

    border-radius:
        14px;

    border:
        none;

    min-height:
        45px;

    background:
        #BBDDEA;

    color:
        #456674;

    font-weight:
        700;

    transition:
        0.15s;
}


.stButton > button:hover,
.stFormSubmitButton > button:hover {

    background:
        #A9D1E1;

    color:
        #365866;

    border:
        none;
}


/* ======================================================
   입력창
====================================================== */

.stTextInput input {

    border-radius:
        14px;

    background:
        rgba(255,255,255,0.93);
}


/* ======================================================
   Metric
====================================================== */

[data-testid="stMetric"] {

    background:
        rgba(255,255,255,0.80);

    padding:
        15px;

    border-radius:
        18px;

    border:
        1px solid
        rgba(255,255,255,0.9);
}


/* ======================================================
   데이터프레임
====================================================== */

[data-testid="stDataFrame"] {

    background:
        rgba(255,255,255,0.85);

    border-radius:
        18px;
}


/* ======================================================
   모바일 대응
====================================================== */

@media (max-width: 800px) {

    .main-title {
        font-size: 2.2rem;
    }

    .falling-code {
        font-size: 1rem;
        padding: 12px 16px;
    }

    .room-code {
        font-size: 3.5rem;
    }

}

</style>
""",
unsafe_allow_html=True
)


# =========================================================
# 6. 데이터베이스 관련 공통 함수
# =========================================================

def make_room_code():

    """
    현재 사용하지 않는 두 자리 방 코드 생성
    """

    for _ in range(100):

        code = str(
            random.randint(10, 99)
        )

        result = (
            supabase
            .table("rooms")
            .select("room_code")
            .eq("room_code", code)
            .execute()
        )

        if not result.data:
            return code

    return None


def get_room(room_code):

    result = (
        supabase
        .table("rooms")
        .select("*")
        .eq("room_code", room_code)
        .execute()
    )

    if result.data:
        return result.data[0]

    return None


def get_students(room_code):

    result = (
        supabase
        .table("students")
        .select("*")
        .eq("room_code", room_code)
        .order("team")
        .order("score", desc=True)
        .execute()
    )

    return result.data


def get_team_scores(
    room_code,
    team_count
):

    students = get_students(
        room_code
    )

    scores = {
        team: 0
        for team in range(
            1,
            team_count + 1
        )
    }

    for student in students:

        team = student["team"]

        if team in scores:

            scores[team] += (
                student["score"]
            )

    return scores


def choose_team(
    room_code,
    team_count
):

    """
    현재 인원이 가장 적은 팀으로 자동 배정
    """

    students = get_students(
        room_code
    )

    counts = {
        team: 0
        for team in range(
            1,
            team_count + 1
        )
    }

    for student in students:

        team = student["team"]

        if team in counts:
            counts[team] += 1

    minimum = min(
        counts.values()
    )

    available = [
        team
        for team, count
        in counts.items()
        if count == minimum
    ]

    return random.choice(
        available
    )


# =========================================================
# 7. 게임 관련 공통 함수
# =========================================================

def new_command():

    st.session_state.current_command = (
        random.choice(commands)
    )


def go_home():

    keys = [
        "room_code",
        "nickname",
        "student_id",
        "team",
        "current_command",
        "teacher_room"
    ]

    for key in keys:
        st.session_state[key] = None

    st.session_state.page = "home"

    st.rerun()


# =========================================================
# 8. 공통 제목
# =========================================================

def show_title():

    title_html = """
<div class="main-title">☁️ Python Typing Garden 🌱</div>
<div class="subtitle">떨어지는 파이썬 코드를 입력하고 팀과 함께 정원을 지켜보세요!</div>
"""

    st.markdown(
        title_html,
        unsafe_allow_html=True
    )


# =========================================================
# 9. 홈 화면
# =========================================================

def home():

    show_title()

    left, center, right = st.columns(
        [1, 1.6, 1]
    )

    with center:

        garden_html = """
<div style="text-align:center; font-size:55px; margin-bottom:10px;">
☁️　☀️　☁️
</div>
"""

        st.markdown(
            garden_html,
            unsafe_allow_html=True
        )

        st.subheader(
            "🌼 게임 참가"
        )

        room = st.text_input(
            "방 코드",
            max_chars=2,
            placeholder="예: 27"
        )

        nickname = st.text_input(
            "닉네임",
            max_chars=12,
            placeholder="예: 테스트1"
        )

        if st.button(
            "🌱 방에 입장하기",
            use_container_width=True
        ):

            room = room.strip()
            nickname = nickname.strip()

            if (
                len(room) != 2
                or not room.isdigit()
            ):

                st.warning(
                    "두 자리 방 코드를 입력해주세요."
                )

            elif not nickname:

                st.warning(
                    "닉네임을 입력해주세요."
                )

            else:

                room_data = get_room(
                    room
                )

                if room_data is None:

                    st.error(
                        "존재하지 않는 방입니다."
                    )

                elif (
                    room_data["status"]
                    == "finished"
                ):

                    st.error(
                        "이미 종료된 게임입니다."
                    )

                else:

                    existing = (
                        supabase
                        .table("students")
                        .select("*")
                        .eq(
                            "room_code",
                            room
                        )
                        .eq(
                            "nickname",
                            nickname
                        )
                        .execute()
                    )

                    if existing.data:

                        st.error(
                            "이미 사용 중인 닉네임입니다."
                        )

                    else:

                        team = choose_team(
                            room,
                            room_data[
                                "team_count"
                            ]
                        )

                        result = (
                            supabase
                            .table("students")
                            .insert({
                                "room_code":
                                    room,

                                "nickname":
                                    nickname,

                                "team":
                                    team,

                                "score":
                                    0,

                                "correct_count":
                                    0,

                                "wrong_count":
                                    0
                            })
                            .execute()
                        )

                        student = (
                            result.data[0]
                        )

                        st.session_state.room_code = (
                            room
                        )

                        st.session_state.nickname = (
                            nickname
                        )

                        st.session_state.student_id = (
                            student["id"]
                        )

                        st.session_state.team = (
                            team
                        )

                        new_command()

                        st.session_state.page = (
                            "student"
                        )

                        st.rerun()

        st.write("")

        st.divider()

        st.caption(
            "선생님이신가요?"
        )

        if st.button(
            "☁️ 교사용 방 만들기",
            use_container_width=True
        ):

            st.session_state.page = (
                "teacher_create"
            )

            st.rerun()


# =========================================================
# 10. 교사 - 방 만들기
# =========================================================

def teacher_create():

    show_title()

    left, center, right = st.columns(
        [1, 1.5, 1]
    )

    with center:

        st.subheader(
            "☁️ 새로운 게임 만들기"
        )

        st.write(
            "학생들이 참여할 팀의 수를 선택해주세요."
        )

        team_count = st.slider(
            "팀 개수",
            min_value=2,
            max_value=6,
            value=3
        )

        st.caption(
            "학생들은 입장할 때 "
            "현재 인원이 가장 적은 팀으로 "
            "자동 배정됩니다."
        )

        if st.button(
            "🌱 방 만들기",
            use_container_width=True
        ):

            room_code = (
                make_room_code()
            )

            if room_code is None:

                st.error(
                    "방 코드를 생성하지 못했습니다."
                )

            else:

                (
                    supabase
                    .table("rooms")
                    .insert({
                        "room_code":
                            room_code,

                        "team_count":
                            team_count,

                        "status":
                            "waiting"
                    })
                    .execute()
                )

                st.session_state.teacher_room = (
                    room_code
                )

                st.session_state.page = (
                    "teacher_dashboard"
                )

                st.rerun()

        if st.button(
            "← 처음으로"
        ):
            go_home()


# =========================================================
# 11. 교사 - 대시보드
# =========================================================

def teacher_dashboard():

    room_code = (
        st.session_state.teacher_room
    )

    if room_code is None:

        go_home()
        return

    room = get_room(
        room_code
    )

    if room is None:

        st.error(
            "방을 찾을 수 없습니다."
        )

        return

    show_title()

    col1, col2 = st.columns(
        [1, 2]
    )

    with col1:

        st.caption(
            "학생들에게 알려줄 방 코드"
        )

        room_html = f"""
<div class="garden-card">
<div style="text-align:center; color:#7896A5;">ROOM CODE</div>
<div class="room-code">{room_code}</div>
<div style="text-align:center; color:#7896A5;">학생들에게 이 번호를 알려주세요.</div>
</div>
"""

        st.markdown(
            room_html,
            unsafe_allow_html=True
        )

    with col2:

        st.write(
            "### 🎮 게임 관리"
        )

        status_text = {
            "waiting":
                "🟡 입장 대기",

            "playing":
                "🟢 게임 진행 중",

            "finished":
                "🔴 게임 종료"
        }

        st.write(
            "현재 상태: "
            f"**{status_text[room['status']]}**"
        )

        st.write(
            f"팀 개수: **{room['team_count']}팀**"
        )

        b1, b2 = st.columns(
            2
        )

        with b1:

            if st.button(
                "▶️ 게임 시작",
                use_container_width=True,
                disabled=(
                    room["status"]
                    == "playing"
                    or
                    room["status"]
                    == "finished"
                )
            ):

                (
                    supabase
                    .table("rooms")
                    .update({
                        "status":
                            "playing"
                    })
                    .eq(
                        "room_code",
                        room_code
                    )
                    .execute()
                )

                st.rerun()

        with b2:

            if st.button(
                "⏹ 게임 종료",
                use_container_width=True,
                disabled=(
                    room["status"]
                    == "finished"
                )
            ):

                (
                    supabase
                    .table("rooms")
                    .update({
                        "status":
                            "finished"
                    })
                    .eq(
                        "room_code",
                        room_code
                    )
                    .execute()
                )

                st.rerun()

    st.divider()

    teacher_live_panel(
        room_code,
        room["team_count"]
    )

    st.write("")

    if st.button(
        "🏠 처음으로 돌아가기"
    ):
        go_home()


# =========================================================
# 12. 교사 - 실시간 현황
# =========================================================

@st.fragment(run_every="2s")
def teacher_live_panel(
    room_code,
    team_count
):

    students = get_students(
        room_code
    )

    scores = get_team_scores(
        room_code,
        team_count
    )

    total_correct = sum(
        s["correct_count"]
        for s in students
    )

    total_wrong = sum(
        s["wrong_count"]
        for s in students
    )

    m1, m2, m3 = st.columns(
        3
    )

    m1.metric(
        "👥 참가 학생",
        f"{len(students)}명"
    )

    m2.metric(
        "🌱 총 정답",
        f"{total_correct}개"
    )

    m3.metric(
        "🍂 총 오답",
        f"{total_wrong}개"
    )

    st.write(
        "### 🌷 팀 점수"
    )

    columns = st.columns(
        team_count
    )

    team_icons = [
        "🌷",
        "🌼",
        "🌿",
        "🪻",
        "🌻",
        "🍀"
    ]

    for i in range(
        team_count
    ):

        team = i + 1

        with columns[i]:

            team_html = f"""
<div class="team-card">
<div class="team-number">{team_icons[i]} {team}팀</div>
<div class="team-score">{scores[team]}점</div>
</div>
"""

            st.markdown(
                team_html,
                unsafe_allow_html=True
            )

    st.write(
        "### 👩‍💻 학생 현황"
    )

    if not students:

        st.info(
            "아직 입장한 학생이 없습니다."
        )

    else:

        table_data = []

        for student in students:

            attempts = (
                student["correct_count"]
                +
                student["wrong_count"]
            )

            if attempts == 0:

                accuracy = "-"

            else:

                accuracy = (
                    f"{student['correct_count'] / attempts * 100:.0f}%"
                )

            table_data.append({

                "닉네임":
                    student["nickname"],

                "팀":
                    f"{student['team']}팀",

                "점수":
                    student["score"],

                "정답":
                    student["correct_count"],

                "오답":
                    student["wrong_count"],

                "정확도":
                    accuracy
            })

        st.dataframe(
            table_data,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# 13. 학생 - 게임 화면
# =========================================================

def student_game():

    room_code = (
        st.session_state.room_code
    )

    student_id = (
        st.session_state.student_id
    )

    if (
        room_code is None
        or student_id is None
    ):

        go_home()
        return

    room = get_room(
        room_code
    )

    if room is None:

        st.error(
            "방이 존재하지 않습니다."
        )

        return

    show_title()

    top1, top2, top3 = (
        st.columns(
            [1, 1, 1]
        )
    )

    with top1:

        st.write(
            f"### 🌷 {st.session_state.team}팀"
        )

        st.caption(
            st.session_state.nickname
        )

    with top2:

        room_info_html = f"""
<div style="text-align:center; font-size:18px; padding-top:10px;">
방 코드 <strong>{room_code}</strong>
</div>
"""

        st.markdown(
            room_info_html,
            unsafe_allow_html=True
        )

    with top3:

        student_score_panel(
            student_id
        )

    # ---------------------------------------------
    # 대기 상태
    # ---------------------------------------------

    if room["status"] == "waiting":

        waiting_html = """
<div class="waiting-box">
<div class="waiting-cloud">☁️</div>
<div style="font-size:1.35rem; font-weight:bold; color:#5C7C8B;">
선생님이 게임을 준비하고 있어요.
</div>
<div style="margin-top:8px; color:#7D99A5;">
게임이 시작되면 자동으로 화면이 바뀝니다.
</div>
</div>
"""

        st.markdown(
            waiting_html,
            unsafe_allow_html=True
        )

        waiting_panel(
            room_code,
            room["team_count"]
        )

        return

    # ---------------------------------------------
    # 종료 상태
    # ---------------------------------------------

    if room["status"] == "finished":

        st.success(
            "🌼 게임이 종료되었습니다!"
        )

        final_scoreboard(
            room_code,
            room["team_count"]
        )

        return

    # ---------------------------------------------
    # 게임 진행
    # ---------------------------------------------

    if (
        st.session_state.current_command
        is None
    ):
        new_command()

    left, right = st.columns(
        [3, 1]
    )

    with left:

        safe_command = html.escape(
            st.session_state.current_command
        )

        # 중요:
        # HTML에 앞쪽 들여쓰기를 넣지 않음.
        # Markdown 코드 블록으로 인식되는 문제 방지.

        game_html = f"""
<div class="sky-game">
<div class="cloud-one">☁️</div>
<div class="cloud-two">☁️</div>
<div class="sun">☀️</div>
<div class="falling-code">{safe_command}</div>
<div class="field">🌱　🌷　🌿　🌼　🌱　🌷　🌿</div>
</div>
"""

        st.markdown(
            game_html,
            unsafe_allow_html=True
        )

        with st.form(
            "typing_form",
            clear_on_submit=True
        ):

            answer = st.text_input(
                "⌨️ 코드 입력",
                placeholder=(
                    "위의 코드를 정확하게 입력하세요"
                )
            )

            submitted = (
                st.form_submit_button(
                    "🌱 입력!",
                    use_container_width=True
                )
            )

        if submitted:

            check_answer(
                answer,
                student_id
            )

    with right:

        live_team_scoreboard(
            room_code,
            room["team_count"]
        )


# =========================================================
# 14. 학생 - 개인 점수
# =========================================================

@st.fragment(run_every="2s")
def student_score_panel(
    student_id
):

    result = (
        supabase
        .table("students")
        .select(
            "score, correct_count, wrong_count"
        )
        .eq(
            "id",
            student_id
        )
        .execute()
    )

    if result.data:

        student = (
            result.data[0]
        )

        st.metric(
            "⭐ 내 점수",
            f"{student['score']}점"
        )


# =========================================================
# 15. 정답 검사
# =========================================================

def check_answer(
    answer,
    student_id
):

    current = (
        st.session_state.current_command
    )

    result = (
        supabase
        .table("students")
        .select(
            "score, correct_count, wrong_count"
        )
        .eq(
            "id",
            student_id
        )
        .execute()
    )

    if not result.data:

        st.error(
            "학생 정보를 찾을 수 없습니다."
        )

        return

    student = (
        result.data[0]
    )

    # ---------------------------------------------
    # 정답
    # ---------------------------------------------

    if answer == current:

        new_score = (
            student["score"]
            + 10
        )

        new_correct = (
            student["correct_count"]
            + 1
        )

        (
            supabase
            .table("students")
            .update({
                "score":
                    new_score,

                "correct_count":
                    new_correct
            })
            .eq(
                "id",
                student_id
            )
            .execute()
        )

        st.toast(
            "정답! +10점 🌼"
        )

        new_command()

        time.sleep(
            0.15
        )

        st.rerun()

    # ---------------------------------------------
    # 오답
    # ---------------------------------------------

    else:

        new_wrong = (
            student["wrong_count"]
            + 1
        )

        (
            supabase
            .table("students")
            .update({
                "wrong_count":
                    new_wrong
            })
            .eq(
                "id",
                student_id
            )
            .execute()
        )

        st.error(
            "🍂 코드가 정확하지 않습니다. "
            "대소문자, 괄호, 따옴표, "
            "띄어쓰기를 확인하세요."
        )


# =========================================================
# 16. 학생 - 실시간 팀 점수
# =========================================================

@st.fragment(run_every="2s")
def live_team_scoreboard(
    room_code,
    team_count
):

    scores = get_team_scores(
        room_code,
        team_count
    )

    st.write(
        "### 🌼 팀 점수"
    )

    icons = [
        "🌷",
        "🌼",
        "🌿",
        "🪻",
        "🌻",
        "🍀"
    ]

    ranking = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    for team, score in ranking:

        team_html = f"""
<div class="team-card">
<div class="team-number">{icons[team - 1]} {team}팀</div>
<div class="team-score">{score}점</div>
</div>
"""

        st.markdown(
            team_html,
            unsafe_allow_html=True
        )


# =========================================================
# 17. 학생 - 대기 화면 실시간 갱신
# =========================================================

@st.fragment(run_every="2s")
def waiting_panel(
    room_code,
    team_count
):

    room = get_room(
        room_code
    )

    # 교사가 게임 시작
    if (
        room
        and
        room["status"] == "playing"
    ):

        st.rerun()
        return

    # 교사가 게임 종료
    if (
        room
        and
        room["status"] == "finished"
    ):

        st.rerun()
        return

    students = get_students(
        room_code
    )

    st.write("")

    st.write(
        f"현재 **{len(students)}명**이 "
        "입장했습니다."
    )

    columns = st.columns(
        team_count
    )

    icons = [
        "🌷",
        "🌼",
        "🌿",
        "🪻",
        "🌻",
        "🍀"
    ]

    for i in range(
        team_count
    ):

        team = i + 1

        count = len([
            student
            for student in students
            if student["team"] == team
        ])

        columns[i].metric(
            f"{icons[i]} {team}팀",
            f"{count}명"
        )


# =========================================================
# 18. 최종 점수판
# =========================================================

def final_scoreboard(
    room_code,
    team_count
):

    scores = get_team_scores(
        room_code,
        team_count
    )

    ranking = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    st.write(
        "### 🏆 최종 결과"
    )

    icons = [
        "🥇",
        "🥈",
        "🥉",
        "🌱",
        "🌱",
        "🌱"
    ]

    for rank, (
        team,
        score
    ) in enumerate(
        ranking,
        start=1
    ):

        icon = icons[
            min(
                rank - 1,
                len(icons) - 1
            )
        ]

        result_html = f"""
<div class="team-card">
<div class="team-number">{icon} {rank}위</div>
<div class="team-score">{team}팀 · {score}점</div>
</div>
"""

        st.markdown(
            result_html,
            unsafe_allow_html=True
        )


# =========================================================
# 19. 페이지 실행
# =========================================================

if (
    st.session_state.page
    == "home"
):

    home()


elif (
    st.session_state.page
    == "teacher_create"
):

    teacher_create()


elif (
    st.session_state.page
    == "teacher_dashboard"
):

    teacher_dashboard()


elif (
    st.session_state.page
    == "student"
):

    student_game()


else:

    st.session_state.page = (
        "home"
    )

    st.rerun()
