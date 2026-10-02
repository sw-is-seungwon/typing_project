import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client
import random
import json


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

    return create_client(
        url,
        key
    )


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
# 4. JavaScript 게임 컴포넌트
# =========================================================

typing_game = components.declare_component(
    "typing_game",
    path="game_component"
)


# =========================================================
# 5. Session State 초기화
# =========================================================

defaults = {

    "page":
        "home",

    "room_code":
        None,

    "nickname":
        None,

    "student_id":
        None,

    "team":
        None,

    "teacher_room":
        None,

    "last_room_status":
        None
}


for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# =========================================================
# 6. CSS
# =========================================================

st.markdown(
"""
<style>


/* ======================================================
   전체
====================================================== */

.stApp {

    background:
        linear-gradient(
            to bottom,
            #DDF3FF 0%,
            #EAF8FF 65%,
            #DDEFD4 65%,
            #CDE7C4 100%
        );

    color:
        #4E6875;
}


.block-container {

    max-width:
        1500px;

    padding-top:
        1.5rem;

    padding-bottom:
        4rem;
}


/* ======================================================
   제목
====================================================== */

.main-title {

    text-align:
        center;

    font-size:
        3.2rem;

    font-weight:
        800;

    color:
        #54798C;

    margin-top:
        10px;

    margin-bottom:
        5px;
}


.subtitle {

    text-align:
        center;

    color:
        #7896A5;

    font-size:
        1.05rem;

    margin-bottom:
        28px;
}


/* ======================================================
   일반 카드
====================================================== */

.garden-card {

    background:
        rgba(255,255,255,0.88);

    border:
        1px solid
        rgba(255,255,255,0.9);

    border-radius:
        25px;

    padding:
        25px;

    box-shadow:
        0px 8px 25px
        rgba(80,120,140,0.10);
}


/* ======================================================
   방 코드
====================================================== */

.room-code {

    text-align:
        center;

    font-size:
        5rem;

    font-weight:
        800;

    color:
        #648DA1;

    letter-spacing:
        10px;
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


/* ======================================================
   입력
====================================================== */

.stTextInput input {

    border-radius:
        14px;

    background:
        rgba(255,255,255,0.95);
}


/* ======================================================
   Metric
====================================================== */

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


/* ======================================================
   컴포넌트 iframe
====================================================== */

iframe {

    border-radius:
        28px;

}


/* ======================================================
   모바일
====================================================== */

@media (max-width: 900px) {

    .main-title {

        font-size:
            2.2rem;
    }

    .room-code {

        font-size:
            3.5rem;
    }
}


</style>
""",
unsafe_allow_html=True
)


# =========================================================
# 7. DB 함수
# =========================================================

def make_room_code():

    for _ in range(100):

        code = str(
            random.randint(
                10,
                99
            )
        )

        result = (
            supabase
            .table("rooms")
            .select("room_code")
            .eq(
                "room_code",
                code
            )
            .execute()
        )

        if not result.data:

            return code

    return None


# ---------------------------------------------------------
# 방 정보
# ---------------------------------------------------------

def get_room(
    room_code
):

    result = (
        supabase
        .table("rooms")
        .select("*")
        .eq(
            "room_code",
            room_code
        )
        .execute()
    )

    if result.data:

        return result.data[0]

    return None


# ---------------------------------------------------------
# 학생 목록
# ---------------------------------------------------------

def get_students(
    room_code
):

    result = (
        supabase
        .table("students")
        .select("*")
        .eq(
            "room_code",
            room_code
        )
        .order("team")
        .order(
            "score",
            desc=True
        )
        .execute()
    )

    return result.data


# ---------------------------------------------------------
# 학생 한 명
# ---------------------------------------------------------

def get_student(
    student_id
):

    result = (
        supabase
        .table("students")
        .select("*")
        .eq(
            "id",
            student_id
        )
        .execute()
    )

    if result.data:

        return result.data[0]

    return None


# ---------------------------------------------------------
# 팀 점수
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# 자동 팀 선택
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# 교사용 팀 변경
# ---------------------------------------------------------

def change_student_team(
    student_id,
    new_team
):

    (
        supabase
        .table("students")
        .update({
            "team":
                new_team
        })
        .eq(
            "id",
            student_id
        )
        .execute()
    )


# =========================================================
# 8. 처음으로 돌아가기
# =========================================================

def go_home():

    st.session_state.page = (
        "home"
    )

    st.session_state.room_code = (
        None
    )

    st.session_state.nickname = (
        None
    )

    st.session_state.student_id = (
        None
    )

    st.session_state.team = (
        None
    )

    st.session_state.teacher_room = (
        None
    )

    st.session_state.last_room_status = (
        None
    )

    st.rerun()


# =========================================================
# 9. 제목
# =========================================================

def show_title():

    title_html = """
<div class="main-title">
☁️ Python Typing Garden 🌱
</div>

<div class="subtitle">
떨어지는 파이썬 코드를 입력하고 팀과 함께 정원을 지켜보세요!
</div>
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

    left, center, right = (
        st.columns(
            [1, 1.6, 1]
        )
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

            room = (
                room.strip()
            )

            nickname = (
                nickname.strip()
            )

            # ---------------------------------------------
            # 방 코드 확인
            # ---------------------------------------------

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

                room_data = (
                    get_room(
                        room
                    )
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

                    # -------------------------------------
                    # 중복 닉네임 확인
                    # -------------------------------------

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

                        # ---------------------------------
                        # 자동 팀 배정
                        # ---------------------------------

                        team = (
                            choose_team(
                                room,
                                room_data[
                                    "team_count"
                                ]
                            )
                        )

                        # ---------------------------------
                        # 학생 생성
                        # ---------------------------------

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

                        # ---------------------------------
                        # 세션 저장
                        # ---------------------------------

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

                        st.session_state.last_room_status = (
                            room_data["status"]
                        )

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
# 11. 교사 방 만들기
# =========================================================

def teacher_create():

    show_title()

    left, center, right = (
        st.columns(
            [1, 1.5, 1]
        )
    )

    with center:

        st.subheader(
            "☁️ 새로운 게임 만들기"
        )

        team_count = (
            st.slider(
                "팀 개수",
                min_value=2,
                max_value=6,
                value=3
            )
        )

        st.caption(
            "학생은 처음 입장할 때 인원이 가장 적은 "
            "팀으로 자동 배정됩니다. "
            "게임 시작 전 교사가 직접 변경할 수 있습니다."
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

    col1, col2 = (
        st.columns(
            [1, 2]
        )
    )

    # -----------------------------------------------------
    # 방 코드
    # -----------------------------------------------------

    with col1:

        st.caption(
            "학생들에게 알려줄 방 코드"
        )

        room_html = f"""
<div class="garden-card">

<div style="text-align:center; color:#7896A5;">
ROOM CODE
</div>

<div class="room-code">
{room_code}
</div>

<div style="text-align:center; color:#7896A5;">
학생들에게 이 번호를 알려주세요.
</div>

</div>
"""

        st.markdown(
            room_html,
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # 게임 관리
    # -----------------------------------------------------

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
            f"팀 개수: "
            f"**{room['team_count']}팀**"
        )

        b1, b2 = (
            st.columns(2)
        )

        # ---------------------------------------------
        # 게임 시작
        # ---------------------------------------------

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

        # ---------------------------------------------
        # 게임 종료
        # ---------------------------------------------

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

    # -----------------------------------------------------
    # 팀 편성
    # -----------------------------------------------------

    teacher_team_manager(
        room_code,
        room["team_count"],
        room["status"]
    )

    st.divider()

    # -----------------------------------------------------
    # 실시간 현황
    # -----------------------------------------------------

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
# 13. 교사용 팀 관리
# =========================================================

@st.fragment(run_every="2s")
def teacher_team_manager(
    room_code,
    team_count,
    room_status
):

    st.write(
        "### 👥 학생 팀 관리"
    )

    if room_status == "waiting":

        st.caption(
            "학생이 입장하면 자동으로 팀이 배정됩니다. "
            "아래에서 원하는 팀으로 변경할 수 있습니다."
        )

    else:

        st.caption(
            "게임이 시작되어 팀 편성이 고정되었습니다."
        )

    students = (
        get_students(
            room_code
        )
    )

    if not students:

        st.info(
            "아직 입장한 학생이 없습니다."
        )

        return

    # -----------------------------------------------------
    # 학생별 팀 설정
    # -----------------------------------------------------

    for student in students:

        col1, col2, col3 = (
            st.columns(
                [2, 1, 2]
            )
        )

        with col1:

            st.write(
                f"**👤 {student['nickname']}**"
            )

        with col2:

            st.write(
                f"현재 **{student['team']}팀**"
            )

        with col3:

            new_team = (
                st.selectbox(

                    "팀 선택",

                    options=list(
                        range(
                            1,
                            team_count + 1
                        )
                    ),

                    index=(
                        student["team"]
                        - 1
                    ),

                    format_func=lambda x:
                        f"{x}팀",

                    key=(
                        f"team_select_"
                        f"{student['id']}"
                    ),

                    label_visibility=
                        "collapsed",

                    disabled=(
                        room_status
                        != "waiting"
                    )
                )
            )

            if (
                room_status
                == "waiting"
                and
                new_team
                != student["team"]
            ):

                change_student_team(
                    student["id"],
                    new_team
                )

                st.toast(
                    f"{student['nickname']} → "
                    f"{new_team}팀으로 변경했습니다."
                )

                st.rerun()


# =========================================================
# 14. 교사 실시간 현황
# =========================================================

@st.fragment(run_every="2s")
def teacher_live_panel(
    room_code,
    team_count
):

    students = (
        get_students(
            room_code
        )
    )

    scores = (
        get_team_scores(
            room_code,
            team_count
        )
    )

    total_correct = sum(

        student[
            "correct_count"
        ]

        for student in students
    )

    total_wrong = sum(

        student[
            "wrong_count"
        ]

        for student in students
    )

    # -----------------------------------------------------
    # 전체 현황
    # -----------------------------------------------------

    m1, m2, m3 = (
        st.columns(3)
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

    # -----------------------------------------------------
    # 팀 점수
    # -----------------------------------------------------

    st.write(
        "### 🌷 팀 점수"
    )

    columns = (
        st.columns(
            team_count
        )
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

<div class="team-number">
{icons[i]} {team}팀
</div>

<div class="team-score">
{scores[team]}점
</div>

</div>
"""

            st.markdown(
                team_html,
                unsafe_allow_html=True
            )

    # -----------------------------------------------------
    # 학생 현황
    # -----------------------------------------------------

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
                student[
                    "correct_count"
                ]
                +
                student[
                    "wrong_count"
                ]
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
                    student[
                        "correct_count"
                    ],

                "오답":
                    student[
                        "wrong_count"
                    ],

                "정확도":
                    accuracy
            })

        st.dataframe(
            table_data,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# 15. JavaScript 타자 게임
# =========================================================

def javascript_typing_game(
    student_id
):

    # -----------------------------------------------------
    # 학생 현재 상태
    # -----------------------------------------------------

    student = (
        get_student(
            student_id
        )
    )

    if student is None:

        st.error(
            "학생 정보를 찾을 수 없습니다."
        )

        return

    # -----------------------------------------------------
    # JavaScript 컴포넌트 실행
    # -----------------------------------------------------

    game_result = typing_game(

        commands=
            commands,

        score=
            student["score"],

        key=
            f"typing_game_{student_id}",

        default=
            None
    )

    # -----------------------------------------------------
    # 아직 입력 이벤트가 없음
    # -----------------------------------------------------

    if not game_result:

        return

    event_id = (
        game_result.get(
            "event_id"
        )
    )

    if event_id is None:

        return

    # -----------------------------------------------------
    # 중복 이벤트 방지
    # -----------------------------------------------------

    event_key = (
        f"last_game_event_"
        f"{student_id}"
    )

    last_event = (
        st.session_state.get(
            event_key
        )
    )

    if (
        last_event
        == event_id
    ):

        return

    # 먼저 기록하여
    # 같은 이벤트 중복 처리 방지

    st.session_state[
        event_key
    ] = event_id

    # -----------------------------------------------------
    # 최신 학생 정보
    # -----------------------------------------------------

    current = (
        get_student(
            student_id
        )
    )

    if current is None:

        return

    # -----------------------------------------------------
    # 정답
    # -----------------------------------------------------

    if game_result.get(
        "correct"
    ):

        new_score = (
            current["score"]
            + 10
        )

        new_correct = (
            current[
                "correct_count"
            ]
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

    # -----------------------------------------------------
    # 오답
    # -----------------------------------------------------

    else:

        new_wrong = (
            current[
                "wrong_count"
            ]
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


# =========================================================
# 16. 학생 화면
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

    # -----------------------------------------------------
    # 방 확인
    # -----------------------------------------------------

    room = (
        get_room(
            room_code
        )
    )

    if room is None:

        st.error(
            "방을 찾을 수 없습니다."
        )

        return

    # -----------------------------------------------------
    # 학생 정보
    # -----------------------------------------------------

    student = (
        get_student(
            student_id
        )
    )

    if student is None:

        st.error(
            "학생 정보를 찾을 수 없습니다."
        )

        return

    # 교사가 대기 중 팀을 변경한 경우 반영

    st.session_state.team = (
        student["team"]
    )

    show_title()

    # -----------------------------------------------------
    # 게임 상태 감시
    # -----------------------------------------------------

    student_room_monitor(
        room_code
    )

    # -----------------------------------------------------
    # 학생 상단 정보
    # -----------------------------------------------------

    top1, top2, top3 = (
        st.columns(
            [1, 1, 1]
        )
    )

    with top1:

        st.write(
            f"### 🌷 "
            f"{st.session_state.team}팀"
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
    # 게임 대기
    # -----------------------------------------------------

    if (
        room["status"]
        == "waiting"
    ):

        st.markdown(
            """
<div class="waiting-box">

<div style="font-size:65px;">
☁️
</div>

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

        st.info(
            f"🌷 현재 "
            f"{st.session_state.team}팀으로 "
            f"배정되었습니다."
        )

        return

    # -----------------------------------------------------
    # 게임 종료
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
    # 게임 진행
    # -----------------------------------------------------

    left, right = (
        st.columns(
            [4, 1.2]
        )
    )

    with left:

        javascript_typing_game(
            student_id
        )

    with right:

        live_team_scoreboard(
            room_code,
            room["team_count"]
        )


# =========================================================
# 17. 학생 게임 상태 감시
# =========================================================

@st.fragment(run_every="1s")
def student_room_monitor(
    room_code
):

    room = (
        get_room(
            room_code
        )
    )

    if room is None:

        return

    new_status = (
        room["status"]
    )

    current_status = (
        st.session_state.last_room_status
    )

    # -----------------------------------------------------
    # 최초 상태
    # -----------------------------------------------------

    if current_status is None:

        st.session_state.last_room_status = (
            new_status
        )

        return

    # -----------------------------------------------------
    # 상태가 변경됨
    # -----------------------------------------------------

    if (
        current_status
        != new_status
    ):

        st.session_state.last_room_status = (
            new_status
        )

        st.rerun()


# =========================================================
# 18. 학생 개인 점수
# =========================================================

@st.fragment(run_every="2s")
def student_score_panel(
    student_id
):

    student = (
        get_student(
            student_id
        )
    )

    if student:

        st.metric(
            "⭐ 내 점수",
            f"{student['score']}점"
        )


# =========================================================
# 19. 실시간 팀 점수
# =========================================================

@st.fragment(run_every="2s")
def live_team_scoreboard(
    room_code,
    team_count
):

    scores = (
        get_team_scores(
            room_code,
            team_count
        )
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

<div class="team-number">
{icons[team - 1]} {team}팀
</div>

<div class="team-score">
{score}점
</div>

</div>
"""

        st.markdown(
            team_html,
            unsafe_allow_html=True
        )


# =========================================================
# 20. 최종 결과
# =========================================================

def show_finished_screen(
    room_code,
    team_count
):

    st.success(
        "🌼 게임이 종료되었습니다!"
    )

    scores = (
        get_team_scores(
            room_code,
            team_count
        )
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

        icon = (
            rank_icons[
                min(
                    rank - 1,
                    len(rank_icons) - 1
                )
            ]
        )

        result_html = f"""
<div class="team-card">

<div class="team-number">
{icon} {rank}위
</div>

<div class="team-score">
{team}팀 · {score}점
</div>

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
# 21. 페이지 실행
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
