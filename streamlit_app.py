import streamlit as st
from supabase import create_client
import random
import json
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
# 3. 문제 불러오기
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
# 4. Session State
# =========================================================

defaults = {
    "page": "home",
    "room_code": None,
    "nickname": None,
    "student_id": None,
    "team": None,
    "teacher_room": None,
    "active_commands": []
}


for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# 5. 디자인
# =========================================================

st.markdown(
"""
<style>

/* 전체 */

.stApp {
    background:
        linear-gradient(
            to bottom,
            #DDF3FF 0%,
            #EAF8FF 65%,
            #DDEFD4 65%,
            #CDE7C4 100%
        );

    color: #4E6875;
}

.block-container {
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}


/* 제목 */

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
    margin-bottom: 28px;
}


/* 일반 카드 */

.garden-card {
    background: rgba(255,255,255,0.88);
    border: 1px solid rgba(255,255,255,0.9);
    border-radius: 25px;
    padding: 25px;

    box-shadow:
        0px 8px 25px
        rgba(80,120,140,0.10);
}


/* 방 코드 */

.room-code {
    text-align: center;
    font-size: 5rem;
    font-weight: 800;
    color: #648DA1;
    letter-spacing: 10px;
}


/* ======================================================
   게임 하늘
====================================================== */

.sky-game {

    height: 650px;

    position: relative;

    overflow: hidden;

    border-radius: 30px;

    background:
        linear-gradient(
            to bottom,
            #CDEEFF 0%,
            #E7F7FF 72%,
            #F2FBFF 100%
        );

    box-shadow:
        inset 0 0 40px
        rgba(120,190,220,0.18),
        0 8px 25px
        rgba(70,110,130,0.10);

    margin-bottom: 18px;
}


/* 구름 */

.cloud {
    position: absolute;
    opacity: 0.65;
    z-index: 1;
}

.cloud1 {
    top: 40px;
    left: 7%;
    font-size: 65px;
}

.cloud2 {
    top: 110px;
    right: 8%;
    font-size: 50px;
}

.cloud3 {
    top: 240px;
    left: 45%;
    font-size: 42px;
    opacity: 0.4;
}

.sun {
    position: absolute;
    top: 35px;
    right: 25%;
    font-size: 48px;
    opacity: 0.85;
}


/* ======================================================
   떨어지는 코드 공통
====================================================== */

.falling-code {

    position: absolute;

    background:
        rgba(255,255,255,0.96);

    color:
        #4E6875;

    font-family:
        "Courier New",
        monospace;

    font-size:
        1.15rem;

    font-weight:
        700;

    padding:
        12px 20px;

    border-radius:
        16px;

    border:
        1px solid
        rgba(150,200,220,0.4);

    box-shadow:
        0 7px 18px
        rgba(70,110,130,0.13);

    white-space:
        nowrap;

    z-index:
        5;
}


/* 코드 1 */

.code1 {
    left: 8%;

    animation:
        fall1 12s
        linear infinite;
}


/* 코드 2 */

.code2 {
    left: 32%;

    animation:
        fall2 15s
        linear infinite;

    animation-delay:
        -4s;
}


/* 코드 3 */

.code3 {
    left: 56%;

    animation:
        fall3 13s
        linear infinite;

    animation-delay:
        -7s;
}


/* 코드 4 */

.code4 {
    left: 72%;

    animation:
        fall4 17s
        linear infinite;

    animation-delay:
        -10s;
}


@keyframes fall1 {

    from {
        top: -70px;
    }

    to {
        top: 575px;
    }

}


@keyframes fall2 {

    from {
        top: -70px;
    }

    to {
        top: 575px;
    }

}


@keyframes fall3 {

    from {
        top: -70px;
    }

    to {
        top: 575px;
    }

}


@keyframes fall4 {

    from {
        top: -70px;
    }

    to {
        top: 575px;
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

    height: 75px;

    background:
        #C8E6BB;

    border-radius:
        55% 55% 0 0;

    text-align:
        center;

    font-size:
        29px;

    padding-top:
        18px;

    z-index:
        2;
}


/* ======================================================
   팀 카드
====================================================== */

.team-card {

    background:
        rgba(255,255,255,0.90);

    border-radius:
        18px;

    padding:
        16px;

    margin-bottom:
        10px;

    border:
        1px solid
        rgba(255,255,255,0.95);

    box-shadow:
        0 5px 15px
        rgba(80,120,140,0.08);
}


.team-number {

    font-size:
        1.05rem;

    color:
        #718A94;
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
        rgba(255,255,255,0.82);

    border-radius:
        25px;

    padding:
        40px;

    margin-top:
        20px;

    box-shadow:
        0 7px 20px
        rgba(80,120,140,0.08);
}


/* 버튼 */

.stButton > button,
.stFormSubmitButton > button {

    border-radius:
        14px;

    border:
        none;

    min-height:
        46px;

    background:
        #BBDDEA;

    color:
        #456674;

    font-weight:
        700;
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


/* 입력 */

.stTextInput input {

    border-radius:
        14px;

    background:
        rgba(255,255,255,0.95);

    font-family:
        "Courier New",
        monospace;

    font-size:
        1.05rem;
}


/* Metric */

[data-testid="stMetric"] {

    background:
        rgba(255,255,255,0.82);

    padding:
        15px;

    border-radius:
        18px;

    border:
        1px solid
        rgba(255,255,255,0.9);
}


/* 모바일 */

@media (max-width: 900px) {

    .main-title {
        font-size: 2.2rem;
    }

    .falling-code {
        font-size: 0.8rem;
        padding: 10px;
    }

    .sky-game {
        height: 550px;
    }

}

</style>
""",
unsafe_allow_html=True
)


# =========================================================
# 6. DB 함수
# =========================================================

def make_room_code():

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

        if student["team"] in scores:

            scores[
                student["team"]
            ] += student["score"]

    return scores


def choose_team(
    room_code,
    team_count
):

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

        if student["team"] in counts:

            counts[
                student["team"]
            ] += 1

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
# 7. 게임 명령어 관리
# =========================================================

def create_command_set():

    """
    동시에 보여줄 4개 문제 생성
    """

    if len(commands) >= 4:

        st.session_state.active_commands = (
            random.sample(
                commands,
                4
            )
        )

    else:

        st.session_state.active_commands = [
            random.choice(commands)
            for _ in range(4)
        ]


def replace_command(index):

    """
    맞힌 문제 하나만 새 문제로 교체
    """

    current = (
        st.session_state.active_commands
    )

    available = [
        command
        for command in commands
        if command not in current
    ]

    if available:

        new_value = (
            random.choice(
                available
            )
        )

    else:

        new_value = (
            random.choice(
                commands
            )
        )

    st.session_state.active_commands[
        index
    ] = new_value


# =========================================================
# 8. 초기화
# =========================================================

def go_home():

    for key in [
        "room_code",
        "nickname",
        "student_id",
        "team",
        "teacher_room"
    ]:

        st.session_state[key] = None

    st.session_state.active_commands = []

    st.session_state.page = "home"

    st.rerun()


# =========================================================
# 9. 제목
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
# 10. 홈
# =========================================================

def home():

    show_title()

    left, center, right = st.columns(
        [1, 1.6, 1]
    )

    with center:

        st.markdown(
            """
<div style="text-align:center; font-size:55px;">
☁️　☀️　☁️
</div>
""",
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
                or
                not room.isdigit()
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

                        create_command_set()

                        st.session_state.page = (
                            "student"
                        )

                        st.rerun()

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
# 11. 교사 방 생성
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

        team_count = st.slider(
            "팀 개수",
            2,
            6,
            3
        )

        st.caption(
            "학생들은 현재 인원이 가장 적은 "
            "팀으로 자동 배정됩니다."
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
# 12. 교사 대시보드
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
            f"현재 상태: "
            f"**{status_text[room['status']]}**"
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
                    in [
                        "playing",
                        "finished"
                    ]
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

    if st.button(
        "🏠 처음으로 돌아가기"
    ):
        go_home()


# =========================================================
# 13. 교사 실시간 현황
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
        student["correct_count"]
        for student in students
    )

    total_wrong = sum(
        student["wrong_count"]
        for student in students
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

        with columns[i]:

            team_html = f"""
<div class="team-card">
<div class="team-number">{icons[i]} {team}팀</div>
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
# 14. 학생 화면
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
        or
        student_id is None
    ):

        go_home()
        return

    show_title()

    # -----------------------------------------------------
    # 게임 상태 감시
    # -----------------------------------------------------

    student_room_monitor(
        room_code
    )

    room = get_room(
        room_code
    )

    if room is None:

        st.error(
            "방을 찾을 수 없습니다."
        )

        return

    # -----------------------------------------------------
    # 상단 정보
    # -----------------------------------------------------

    top1, top2, top3 = st.columns(
        [1, 1, 1]
    )

    with top1:

        st.write(
            f"### 🌷 {st.session_state.team}팀"
        )

        st.caption(
            st.session_state.nickname
        )

    with top2:

        st.markdown(
            f"""
<div style="text-align:center; font-size:18px; padding-top:10px;">
방 코드 <strong>{room_code}</strong>
</div>
""",
            unsafe_allow_html=True
        )

    with top3:

        student_score_panel(
            student_id
        )

    # -----------------------------------------------------
    # 대기
    # -----------------------------------------------------

    if (
        room["status"]
        == "waiting"
    ):

        st.markdown(
            """
<div class="waiting-box">
<div style="font-size:65px;">☁️</div>
<div style="font-size:1.3rem; font-weight:bold;">
선생님이 게임을 준비하고 있어요.
</div>
<div style="margin-top:8px;">
게임이 시작되면 자동으로 화면이 바뀝니다.
</div>
</div>
""",
            unsafe_allow_html=True
        )

        return

    # -----------------------------------------------------
    # 종료
    # -----------------------------------------------------

    if (
        room["status"]
        == "finished"
    ):

        show_finished_screen(
            room_code,
            room["team_count"]
        )

        return

    # -----------------------------------------------------
    # 명령어 없으면 생성
    # -----------------------------------------------------

    if (
        len(
            st.session_state.active_commands
        )
        != 4
    ):

        create_command_set()

    # -----------------------------------------------------
    # 게임 화면
    # -----------------------------------------------------

    left, right = st.columns(
        [4, 1.2]
    )

    with left:

        safe_commands = [
            html.escape(command)
            for command
            in st.session_state.active_commands
        ]

        game_html = f"""
<div class="sky-game">

<div class="cloud cloud1">☁️</div>
<div class="cloud cloud2">☁️</div>
<div class="cloud cloud3">☁️</div>
<div class="sun">☀️</div>

<div class="falling-code code1">{safe_commands[0]}</div>
<div class="falling-code code2">{safe_commands[1]}</div>
<div class="falling-code code3">{safe_commands[2]}</div>
<div class="falling-code code4">{safe_commands[3]}</div>

<div class="field">
🌱　🌷　🌿　🌼　🌱　🌷　🌿　🌼　🌱
</div>

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
                    "떨어지는 코드 중 하나를 "
                    "정확하게 입력하세요"
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
# 15. 학생 게임 상태 감시
# =========================================================

@st.fragment(run_every="1s")
def student_room_monitor(
    room_code
):

    room = get_room(
        room_code
    )

    if room is None:
        return

    # 현재 Python 렌더링 상태와
    # DB 상태가 달라지면 전체 화면 재실행

    current_status = (
        st.session_state.get(
            "last_room_status"
        )
    )

    new_status = (
        room["status"]
    )

    if (
        current_status is None
    ):

        st.session_state.last_room_status = (
            new_status
        )

        return

    if (
        current_status
        != new_status
    ):

        st.session_state.last_room_status = (
            new_status
        )

        st.rerun()


# =========================================================
# 16. 개인 점수
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
# 17. 정답 검사
# =========================================================

def check_answer(
    answer,
    student_id
):

    answer = answer.strip()

    # 현재 네 문제 중에서
    # 입력값과 일치하는 문제 찾기

    matched_index = None

    for index, command in enumerate(
        st.session_state.active_commands
    ):

        if answer == command:

            matched_index = index
            break

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

    # -----------------------------------------------------
    # 정답
    # -----------------------------------------------------

    if matched_index is not None:

        (
            supabase
            .table("students")
            .update({

                "score":
                    student["score"]
                    + 10,

                "correct_count":
                    student["correct_count"]
                    + 1

            })
            .eq(
                "id",
                student_id
            )
            .execute()
        )

        # 맞힌 문제만 교체

        replace_command(
            matched_index
        )

        st.toast(
            "정답! +10점 🌼"
        )

        st.rerun()

    # -----------------------------------------------------
    # 오답
    # -----------------------------------------------------

    else:

        (
            supabase
            .table("students")
            .update({

                "wrong_count":
                    student["wrong_count"]
                    + 1

            })
            .eq(
                "id",
                student_id
            )
            .execute()
        )

        st.error(
            "🍂 화면에 있는 코드와 일치하지 않습니다. "
            "대소문자, 괄호, 따옴표를 확인하세요."
        )


# =========================================================
# 18. 실시간 팀 점수
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
        key=lambda item:
            item[1],
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
# 19. 게임 종료 화면
# =========================================================

def show_finished_screen(
    room_code,
    team_count
):

    st.success(
        "🌼 게임이 종료되었습니다!"
    )

    scores = get_team_scores(
        room_code,
        team_count
    )

    ranking = sorted(
        scores.items(),
        key=lambda item:
            item[1],
        reverse=True
    )

    st.write(
        "## 🏆 최종 결과"
    )

    rank_icons = [
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

        icon = rank_icons[
            min(
                rank - 1,
                len(rank_icons) - 1
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

    st.write("")

    if st.button(
        "🏠 처음 화면으로"
    ):

        go_home()


# =========================================================
# 20. 페이지 실행
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
