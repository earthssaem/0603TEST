import streamlit as st

st.set_page_config(
    page_title="🌟 나의 직업 유형 테스트",
    page_icon="🧸",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
# 데이터: 질문 (10개)
# 각 보기에 직업 유형별 점수 부여
# 유형: creator / helper / analyst / leader /
#       artist / scientist / adventurer / builder /
#       performer / counselor / techie / nature
# ──────────────────────────────────────────────
QUESTIONS = [
    {
        "q": "주말 오후, 내가 가장 하고 싶은 건?",
        "emoji": "🌤️",
        "choices": [
            ("유튜브 영상이나 블로그 글 만들기 ✏️",        {"creator":3, "artist":2, "performer":1}),
            ("친구나 가족 고민 들어주고 조언하기 💬",       {"helper":3, "counselor":2, "leader":1}),
            ("퍼즐, 코딩, 수학 문제 풀기 🧩",              {"analyst":3, "techie":2, "scientist":2}),
            ("밖에 나가서 새로운 곳 탐험하기 🗺️",          {"adventurer":3, "nature":2, "builder":1}),
        ],
    },
    {
        "q": "모둠 프로젝트를 할 때 나는 주로?",
        "emoji": "🤝",
        "choices": [
            ("아이디어 뱅크! 기발한 아이디어 마구 냄 💡",   {"creator":3, "artist":2, "adventurer":1}),
            ("팀장 역할, 일 분배하고 이끌어 감 📋",         {"leader":3, "builder":2, "analyst":1}),
            ("자료 조사하고 꼼꼼하게 정리함 🔍",            {"analyst":3, "scientist":2, "techie":2}),
            ("분위기 메이커, 모두 즐겁게 만듦 🎉",          {"performer":3, "helper":2, "counselor":1}),
        ],
    },
    {
        "q": "내가 가장 뿌듯함을 느끼는 순간은?",
        "emoji": "🏅",
        "choices": [
            ("내가 만든 결과물을 사람들이 좋아할 때 🎨",    {"creator":3, "artist":3, "performer":1}),
            ("누군가의 문제를 내가 해결해줬을 때 🌱",       {"helper":3, "counselor":3, "leader":1}),
            ("어려운 문제를 끝까지 혼자 풀었을 때 🧠",      {"analyst":3, "scientist":3, "techie":2}),
            ("몸으로 직접 뭔가를 만들거나 완성했을 때 🔨",  {"builder":3, "nature":2, "adventurer":2}),
        ],
    },
    {
        "q": "친구들이 나에 대해 자주 하는 말은?",
        "emoji": "💬",
        "choices": [
            ("\"너 진짜 창의적이다!\" 🌈",                 {"creator":3, "artist":2, "performer":2}),
            ("\"네가 있으면 든든해\" 🛡️",                  {"leader":3, "helper":2, "builder":2}),
            ("\"진짜 꼼꼼하고 정확해\" 📏",                {"analyst":3, "scientist":2, "techie":2}),
            ("\"넌 왜 이렇게 공감을 잘해?\" 🫂",           {"counselor":3, "helper":3, "performer":1}),
        ],
    },
    {
        "q": "좋아하는 TV 프로그램 / 유튜브 장르는?",
        "emoji": "📺",
        "choices": [
            ("요리, 공예, 그림 그리기 등 만들기 콘텐츠 🍳", {"artist":3, "creator":2, "builder":2}),
            ("과학, 우주, 역사 다큐 🔭",                   {"scientist":3, "analyst":2, "nature":2}),
            ("여행 브이로그, 탐험, 스포츠 🏄",              {"adventurer":3, "nature":2, "performer":1}),
            ("토크쇼, 예능, 드라마 🎭",                    {"performer":3, "counselor":2, "creator":1}),
        ],
    },
    {
        "q": "10년 뒤 내 모습, 가장 끌리는 건?",
        "emoji": "🔮",
        "choices": [
            ("내 이름을 건 브랜드·채널을 운영 중 🚀",       {"creator":3, "leader":2, "performer":2}),
            ("사람들을 돕는 전문직으로 일하는 중 💼",        {"helper":3, "counselor":3, "leader":1}),
            ("첨단 기술·연구 분야에서 활약 중 🤖",          {"techie":3, "scientist":3, "analyst":2}),
            ("자연·동물과 함께, 또는 해외 어딘가에서 일 중 🌿", {"nature":3, "adventurer":3, "builder":1}),
        ],
    },
    {
        "q": "스트레스 받을 때 나만의 해소법은?",
        "emoji": "💆",
        "choices": [
            ("그림 그리기, 글쓰기, 음악 듣기 🎵",           {"artist":3, "creator":2, "counselor":1}),
            ("운동하거나 밖에 나가서 몸 쓰기 🏃",           {"adventurer":3, "nature":2, "builder":2}),
            ("게임, 코딩, 퍼즐 같은 두뇌 활동 🎮",          {"techie":3, "analyst":2, "scientist":1}),
            ("친구 만나거나 수다 떨기 🧋",                  {"performer":3, "helper":2, "counselor":2}),
        ],
    },
    {
        "q": "수업 시간 중 가장 집중이 잘 되는 과목은?",
        "emoji": "📖",
        "choices": [
            ("국어·문학·미술처럼 표현하는 과목 🖊️",         {"creator":3, "artist":3, "counselor":1}),
            ("수학·과학·정보처럼 논리적인 과목 🔢",          {"analyst":3, "scientist":2, "techie":3}),
            ("사회·역사·경제처럼 세상을 이해하는 과목 🌍",   {"leader":3, "analyst":2, "adventurer":1}),
            ("체육·음악·연극처럼 몸과 감각을 쓰는 과목 🎶",  {"performer":3, "adventurer":2, "artist":2}),
        ],
    },
    {
        "q": "내가 정말 싫어하는 상황은?",
        "emoji": "😤",
        "choices": [
            ("똑같은 일을 반복해야 할 때 😩",               {"creator":3, "adventurer":3, "performer":1}),
            ("혼자서 모든 걸 결정해야 할 때 😰",             {"helper":3, "counselor":2, "artist":1}),
            ("감정적으로 대화해야 할 때 😶",                 {"analyst":3, "techie":3, "scientist":2}),
            ("계획 없이 즉흥적으로 움직여야 할 때 😵",       {"builder":3, "leader":2, "analyst":1}),
        ],
    },
    {
        "q": "내가 만약 학교 행사를 기획한다면?",
        "emoji": "🎪",
        "choices": [
            ("영상·포스터·굿즈 제작 담당 🎨",               {"creator":3, "artist":3, "techie":1}),
            ("전체 일정·예산 총괄 진행 담당 📊",             {"leader":3, "analyst":2, "builder":2}),
            ("참여자 케어, 분위기 살리기 담당 🌸",           {"helper":3, "counselor":3, "performer":1}),
            ("무대·공연·이벤트 아이디어 담당 🎭",            {"performer":3, "adventurer":2, "creator":2}),
        ],
    },
]

# ──────────────────────────────────────────────
# 결과 유형 (12가지)
# ──────────────────────────────────────────────
RESULTS = {
    "creator": {
        "title": "🎬 크리에이터형",
        "sub": "세상을 내 콘텐츠로 물들이는 아이디어 메이커!",
        "color": "#FF6B9D",
        "bg": "#fff0f6",
        "emoji": "🎬",
        "desc": "새로운 것을 만들고 표현하는 걸 좋아하는 당신! 유튜버, 작가, 마케터처럼 '나만의 것'을 세상에 내놓는 직업이 딱이에요.",
        "jobs": ["📹 유튜버·크리에이터", "✍️ 작가·웹툰 작가", "📣 마케터·브랜드 디자이너", "🎙️ 방송 PD·기자", "📱 SNS 매니저"],
        "study": ["국어·문학", "미디어·영상", "광고·홍보학"],
    },
    "helper": {
        "title": "🌻 헬퍼형",
        "sub": "누군가의 든든한 버팀목이 되어주는 따뜻한 사람!",
        "color": "#FFB347",
        "bg": "#fff8ed",
        "emoji": "🌻",
        "desc": "다른 사람을 돕는 데서 보람을 느끼는 당신! 사람과 함께하는 서비스·복지·교육 분야에서 빛을 발해요.",
        "jobs": ["🏫 교사·교육 전문가", "🏥 간호사·의료 복지사", "🤝 사회복지사", "✈️ 항공 승무원", "🌍 NGO 활동가"],
        "study": ["교육학", "사회복지학", "간호·보건학"],
    },
    "analyst": {
        "title": "🔍 분석가형",
        "sub": "숫자와 데이터 속에서 진실을 찾아내는 두뇌파!",
        "color": "#6C63FF",
        "bg": "#f0efff",
        "emoji": "🔍",
        "desc": "논리적으로 생각하고 꼼꼼하게 분석하는 게 강점인 당신! 데이터·금융·경영 분야에서 두각을 나타낼 거예요.",
        "jobs": ["📊 데이터 분석가", "💹 금융 애널리스트", "🧾 회계사·세무사", "📋 경영 컨설턴트", "🔎 시장조사 전문가"],
        "study": ["경영·경제학", "통계학", "수학·데이터사이언스"],
    },
    "leader": {
        "title": "👑 리더형",
        "sub": "사람들을 이끌고 큰 그림을 그리는 타고난 리더!",
        "color": "#E74C3C",
        "bg": "#fff0ef",
        "emoji": "👑",
        "desc": "목표를 정하고 사람들을 이끌어가는 능력이 탁월한 당신! 경영·정치·법조 분야에서 큰 일을 해낼 거예요.",
        "jobs": ["🏢 기업 CEO·임원", "⚖️ 변호사·판사", "🏛️ 공무원·정치인", "📋 프로젝트 매니저", "🎖️ 장교·소방관"],
        "study": ["경영학", "법학", "행정학"],
    },
    "artist": {
        "title": "🎨 아티스트형",
        "sub": "세상을 아름답게 만드는 감성 충만 예술가!",
        "color": "#FF8C42",
        "bg": "#fff6f0",
        "emoji": "🎨",
        "desc": "감각과 감성으로 세상을 표현하는 당신! 디자인·예술·패션 분야에서 당신만의 색깔을 마음껏 펼쳐봐요.",
        "jobs": ["🖌️ 화가·일러스트레이터", "👗 패션 디자이너", "🏠 인테리어 디자이너", "📸 사진작가", "🎭 무대 예술가"],
        "study": ["시각디자인", "미술·조형", "패션디자인"],
    },
    "scientist": {
        "title": "🔬 과학자형",
        "sub": "세상의 원리를 파고드는 호기심 탐구자!",
        "color": "#00C9A7",
        "bg": "#edfff9",
        "emoji": "🔬",
        "desc": "왜?라는 질문을 멈추지 않는 당신! 자연과학·의학·공학에서 새로운 발견을 이뤄낼 거예요.",
        "jobs": ["⚗️ 화학·생명과학 연구원", "🏥 의사·약사", "🌌 우주·물리학자", "🧬 유전공학자", "🤖 AI 연구원"],
        "study": ["생명과학", "화학·물리", "의학·약학"],
    },
    "adventurer": {
        "title": "🧭 모험가형",
        "sub": "늘 새로운 도전을 찾아 떠나는 행동파!",
        "color": "#F7971E",
        "bg": "#fff8ed",
        "emoji": "🧭",
        "desc": "가만히 앉아있기보다 직접 몸으로 부딪히는 걸 좋아하는 당신! 여행·스포츠·현장 직업이 잘 맞아요.",
        "jobs": ["✈️ 파일럿·스튜어디스", "⚽ 프로 운동선수·코치", "🗺️ 여행 작가·여행 유튜버", "🚒 소방관·구조대원", "🌿 탐험가·트레킹 가이드"],
        "study": ["체육학", "관광·항공학", "지리·환경학"],
    },
    "builder": {
        "title": "🔨 빌더형",
        "sub": "손으로 직접 만들고 완성하는 뚝딱이 장인!",
        "color": "#8B5CF6",
        "bg": "#f5f0ff",
        "emoji": "🔨",
        "desc": "계획하고 제작하고 완성하는 과정을 즐기는 당신! 건축·엔지니어링·IT 개발이 딱 맞아요.",
        "jobs": ["🏗️ 건축가·토목 엔지니어", "💻 소프트웨어 개발자", "⚙️ 기계·자동차 엔지니어", "🔌 전기·전자 기술자", "🎮 게임 개발자"],
        "study": ["건축학", "컴퓨터공학", "기계·전자공학"],
    },
    "performer": {
        "title": "🎤 퍼포머형",
        "sub": "무대 위에서 빛을 발하는 타고난 엔터테이너!",
        "color": "#EC4899",
        "bg": "#fff0f8",
        "emoji": "🎤",
        "desc": "사람들의 시선을 한 몸에 받고 에너지를 나누는 걸 즐기는 당신! 공연·방송·스포츠 분야가 딱이에요.",
        "jobs": ["🎵 가수·뮤지션", "🎭 배우·연극인", "🎙️ MC·아나운서", "💃 댄서·안무가", "🤸 스포츠 선수"],
        "study": ["연극·영화학", "실용음악", "체육·무용학"],
    },
    "counselor": {
        "title": "💜 카운슬러형",
        "sub": "마음을 읽고 치유하는 따뜻한 공감 전문가!",
        "color": "#7C3AED",
        "bg": "#f5f0ff",
        "emoji": "💜",
        "desc": "사람의 감정을 섬세하게 읽고 공감하는 능력이 탁월한 당신! 심리·상담·교육 분야에서 큰 역할을 해낼 거예요.",
        "jobs": ["🧠 심리상담사·심리치료사", "👩‍⚕️ 정신건강 전문의", "📖 학교 상담교사", "🌱 코치·멘토", "🎓 특수교육 교사"],
        "study": ["심리학", "교육학", "사회복지학"],
    },
    "techie": {
        "title": "🤖 테키형",
        "sub": "기술로 세상을 바꾸는 디지털 네이티브!",
        "color": "#0EA5E9",
        "bg": "#f0faff",
        "emoji": "🤖",
        "desc": "최신 기술에 눈이 반짝이고 코딩·게임이 재밌는 당신! IT·인공지능·사이버 분야가 딱 맞아요.",
        "jobs": ["💻 개발자·프로그래머", "🔐 보안 전문가", "🤖 AI·머신러닝 엔지니어", "🎮 게임 기획자", "📡 네트워크 엔지니어"],
        "study": ["컴퓨터공학", "AI·데이터사이언스", "정보보안학"],
    },
    "nature": {
        "title": "🌿 네이처형",
        "sub": "자연과 생명을 사랑하는 지구의 친구!",
        "color": "#10B981",
        "bg": "#edfff7",
        "emoji": "🌿",
        "desc": "동물, 식물, 환경에 관심이 많은 당신! 수의사·환경 연구·농업 바이오 등 생명과 연결된 직업이 잘 맞아요.",
        "jobs": ["🐾 수의사·동물 훈련사", "🌾 농업 연구원·스마트팜 전문가", "♻️ 환경 컨설턴트", "🐋 해양 생물학자", "🌲 산림·조경 전문가"],
        "study": ["수의학", "환경공학", "생명·농업과학"],
    },
}

# ──────────────────────────────────────────────
# CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

html, body, .stApp { font-family: 'Noto Sans KR', sans-serif; }

.stApp {
    background: linear-gradient(160deg, #fdf4ff 0%, #fef9ec 50%, #f0f9ff 100%);
    min-height: 100vh;
}

/* 공통 숨김 */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; max-width: 720px; }

/* ── 히어로 ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}
.hero-emoji {
    font-size: 4rem;
    display: block;
    margin-bottom: 0.4rem;
    animation: bounce 2s infinite;
}
@keyframes bounce {
    0%,100% { transform: translateY(0); }
    50%      { transform: translateY(-10px); }
}
.hero-title {
    font-size: 2.2rem;
    font-weight: 900;
    color: #3b1f6e;
    line-height: 1.3;
    margin: 0;
}
.hero-title span {
    background: linear-gradient(90deg, #a855f7, #ec4899, #f97316);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1rem;
    color: #7c5cbf;
    margin-top: 0.5rem;
}

/* ── 진행바 ── */
.progress-wrap {
    margin: 1rem 0 1.5rem;
}
.progress-label {
    font-size: 0.85rem;
    color: #9b7cc8;
    text-align: right;
    margin-bottom: 0.3rem;
    font-weight: 500;
}
.progress-bar-bg {
    width: 100%;
    height: 10px;
    background: #e9d5ff;
    border-radius: 99px;
    overflow: hidden;
}
.progress-bar-fill {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #a855f7, #ec4899);
    transition: width 0.4s ease;
}

/* ── 질문 카드 ── */
.q-card {
    background: #fff;
    border-radius: 24px;
    padding: 1.8rem 2rem 1.5rem;
    box-shadow: 0 4px 24px rgba(168,85,247,0.10);
    border: 2px solid #f3e8ff;
    margin-bottom: 1.2rem;
}
.q-number {
    font-size: 0.78rem;
    font-weight: 700;
    color: #c084fc;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.q-emoji { font-size: 2rem; display: block; margin-bottom: 0.3rem; }
.q-text {
    font-size: 1.25rem;
    font-weight: 700;
    color: #2d1b69;
    line-height: 1.5;
}

/* ── 선택지 버튼 ── */
div[data-testid="column"] .stButton > button,
.stButton > button {
    width: 100%;
    border-radius: 16px !important;
    padding: 0.85rem 1rem !important;
    font-size: 0.97rem !important;
    font-weight: 600 !important;
    text-align: left !important;
    cursor: pointer;
    transition: all 0.2s ease;
    border: 2px solid #e9d5ff !important;
    background: #fdf4ff !important;
    color: #4a1d96 !important;
    line-height: 1.45 !important;
    white-space: pre-wrap !important;
}
div[data-testid="column"] .stButton > button:hover,
.stButton > button:hover {
    border-color: #a855f7 !important;
    background: #f5e6ff !important;
    transform: translateX(4px) scale(1.01);
    box-shadow: 0 4px 16px rgba(168,85,247,0.18) !important;
    color: #6b21a8 !important;
}

/* ── 결과 카드 ── */
.result-outer {
    border-radius: 28px;
    padding: 2.2rem 2rem 1.8rem;
    text-align: center;
    margin: 0.5rem 0 1.5rem;
    box-shadow: 0 8px 40px rgba(0,0,0,0.08);
    border: 2.5px solid;
    position: relative;
    overflow: hidden;
}
.result-outer::after {
    content: '✨';
    position: absolute;
    font-size: 7rem;
    opacity: 0.06;
    right: -1rem;
    top: -1rem;
    pointer-events: none;
}
.result-main-emoji { font-size: 4.5rem; display: block; margin-bottom: 0.3rem; }
.result-title {
    font-size: 1.9rem;
    font-weight: 900;
    line-height: 1.2;
    margin-bottom: 0.3rem;
}
.result-sub {
    font-size: 1rem;
    font-weight: 600;
    opacity: 0.85;
    margin-bottom: 0.8rem;
}
.result-desc {
    font-size: 0.95rem;
    line-height: 1.7;
    opacity: 0.9;
    background: rgba(255,255,255,0.55);
    border-radius: 14px;
    padding: 0.8rem 1rem;
    text-align: left;
}

/* ── 직업 태그 ── */
.job-tag {
    display: inline-block;
    background: rgba(255,255,255,0.7);
    border-radius: 99px;
    padding: 0.35rem 0.9rem;
    font-size: 0.88rem;
    font-weight: 600;
    margin: 0.25rem 0.2rem;
}

/* ── 추천 과목 ── */
.study-box {
    background: rgba(255,255,255,0.5);
    border-radius: 14px;
    padding: 0.7rem 1rem;
    margin-top: 0.8rem;
    font-size: 0.88rem;
    text-align: left;
}
.study-label {
    font-weight: 700;
    font-size: 0.8rem;
    letter-spacing: 0.05em;
    opacity: 0.7;
    margin-bottom: 0.3rem;
}

/* ── 다시하기 버튼 ── */
.restart-btn .stButton > button {
    background: linear-gradient(90deg, #a855f7, #ec4899) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 99px !important;
    padding: 0.8rem 2.5rem !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 20px rgba(168,85,247,0.35) !important;
    letter-spacing: 0.03em;
}
.restart-btn .stButton > button:hover {
    transform: scale(1.04) !important;
    box-shadow: 0 6px 28px rgba(168,85,247,0.5) !important;
    background: linear-gradient(90deg, #9333ea, #db2777) !important;
}

/* ── 장식 구분선 ── */
.deco-divider {
    text-align: center;
    color: #d8b4fe;
    font-size: 1.1rem;
    letter-spacing: 0.5rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# 상태 초기화
# ──────────────────────────────────────────────
if "step" not in st.session_state:
    st.session_state.step = 0          # 0 = 시작 화면, 1~7 = 질문, 8 = 결과
if "scores" not in st.session_state:
    st.session_state.scores = {k: 0 for k in RESULTS}
if "answers" not in st.session_state:
    st.session_state.answers = []

def reset():
    st.session_state.step = 0
    st.session_state.scores = {k: 0 for k in RESULTS}
    st.session_state.answers = []

def answer(choice_scores):
    for k, v in choice_scores.items():
        st.session_state.scores[k] += v
    st.session_state.step += 1
    st.rerun()

# ──────────────────────────────────────────────
# 화면 렌더링
# ──────────────────────────────────────────────

# ── 시작 화면 ──
if st.session_state.step == 0:
    st.markdown("""
    <div class="hero">
      <span class="hero-emoji">🧸</span>
      <p class="hero-title">나의 직업 유형은<br/><span>뭘까요?</span></p>
      <p class="hero-sub">✨ 10가지 질문으로 찾는 나만의 진로 유형 ✨</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#fff; border-radius:20px; padding:1.2rem 1.5rem;
                border:2px solid #f3e8ff; box-shadow:0 2px 16px rgba(168,85,247,0.08);
                margin-bottom:1.5rem;">
      <div style="font-size:0.88rem; color:#7c5cbf; line-height:1.8;">
        🌟 &nbsp;총 <b>10개</b> 질문, <b>5분</b>이면 완료!<br/>
        💡 &nbsp;<b>12가지</b> 직업 유형 중 나에게 맞는 유형 발견<br/>
        📚 &nbsp;추천 직업 + 관련 공부 분야까지 알려드려요<br/>
        🎯 &nbsp;고등학생의 진로 탐색을 위해 만들어졌어요
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
    if st.button("🚀  테스트 시작하기!", use_container_width=True):
        st.session_state.step = 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="deco-divider">· · · · ·</div>
    <div style="text-align:center; font-size:0.8rem; color:#c4b5fd; padding-bottom:1.5rem;">
      결과는 참고용이에요 🌈 가장 중요한 건 나의 열정과 노력이랍니다!
    </div>
    """, unsafe_allow_html=True)

# ── 질문 화면 (1~7) ──
elif 1 <= st.session_state.step <= len(QUESTIONS):
    idx = st.session_state.step - 1
    q = QUESTIONS[idx]
    total = len(QUESTIONS)
    pct = int((idx / total) * 100)

    # 진행바
    st.markdown(f"""
    <div class="progress-wrap">
      <div class="progress-label">질문 {idx+1} / {total}</div>
      <div class="progress-bar-bg">
        <div class="progress-bar-fill" style="width:{pct}%"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 질문 카드
    st.markdown(f"""
    <div class="q-card">
      <div class="q-number">Q{idx+1}</div>
      <span class="q-emoji">{q['emoji']}</span>
      <div class="q-text">{q['q']}</div>
    </div>
    """, unsafe_allow_html=True)

    # 선택지
    for label, scores in q["choices"]:
        if st.button(label, key=f"q{idx}_{label[:6]}", use_container_width=True):
            answer(scores)

    st.markdown(f"""
    <div style="text-align:center; font-size:0.8rem; color:#c084fc; margin-top:1rem; padding-bottom:1rem;">
      {'⬤ ' * (idx+1)}{'○ ' * (total - idx - 1)}
    </div>
    """, unsafe_allow_html=True)

# ── 결과 화면 ──
elif st.session_state.step > len(QUESTIONS):
    top_key = max(st.session_state.scores, key=lambda k: st.session_state.scores[k])
    r = RESULTS[top_key]
    c = r["color"]

    st.markdown(f"""
    <div style="text-align:center; font-size:1rem; color:#9b7cc8;
                font-weight:600; margin-bottom:0.8rem;">
      🎉 결과가 나왔어요! 🎉
    </div>
    <div class="result-outer" style="background:{r['bg']}; border-color:{c}66; color:{c};">
      <span class="result-main-emoji">{r['emoji']}</span>
      <div class="result-title" style="color:{c};">{r['title']}</div>
      <div class="result-sub">{r['sub']}</div>
      <div class="result-desc" style="color:#3b1f6e;">{r['desc']}</div>
    </div>
    """, unsafe_allow_html=True)

    # 추천 직업
    st.markdown(f"""
    <div style="background:#fff; border-radius:20px; padding:1.2rem 1.5rem;
                border:2px solid {c}44; margin-bottom:1rem;">
      <div style="font-size:0.85rem; font-weight:700; color:{c};
                  letter-spacing:0.05em; margin-bottom:0.6rem;">
        💼  추천 직업
      </div>
      <div>
    """, unsafe_allow_html=True)

    tags_html = "".join(
        f'<span class="job-tag" style="color:{c}; border:1.5px solid {c}44;">{j}</span>'
        for j in r["jobs"]
    )
    st.markdown(f"""
      {tags_html}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 추천 공부 분야
    study_tags = " &nbsp;·&nbsp; ".join(r["study"])
    st.markdown(f"""
    <div style="background:#fff; border-radius:20px; padding:1.2rem 1.5rem;
                border:2px solid {c}44; margin-bottom:1.5rem;">
      <div style="font-size:0.85rem; font-weight:700; color:{c};
                  letter-spacing:0.05em; margin-bottom:0.4rem;">
        📚  관련 공부 분야
      </div>
      <div style="font-size:0.93rem; color:#4a1d96; font-weight:500;">
        {study_tags}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 전체 점수 (상위 3개)
    sorted_scores = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
    top3 = sorted_scores[:3]
    st.markdown("""
    <div style="font-size:0.85rem; font-weight:700; color:#9b7cc8;
                letter-spacing:0.05em; margin-bottom:0.5rem;">
      📊  나의 TOP 3 유형
    </div>
    """, unsafe_allow_html=True)

    for rank, (key, score) in enumerate(top3):
        rv = RESULTS[key]
        medals = ["🥇", "🥈", "🥉"]
        bar_w = int((score / (top3[0][1] + 0.01)) * 100)
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:0.7rem;
                    margin-bottom:0.5rem; background:#fff;
                    border-radius:14px; padding:0.6rem 1rem;
                    border:1.5px solid #f3e8ff;">
          <span style="font-size:1.2rem;">{medals[rank]}</span>
          <span style="font-size:1.1rem;">{rv['emoji']}</span>
          <div style="flex:1;">
            <div style="font-size:0.88rem; font-weight:700;
                        color:#4a1d96;">{rv['title']}</div>
            <div style="height:6px; background:#f3e8ff; border-radius:99px;
                        margin-top:4px; overflow:hidden;">
              <div style="height:100%; width:{bar_w}%;
                          background:linear-gradient(90deg,{rv['color']},{rv['color']}99);
                          border-radius:99px;"></div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown('<div class="restart-btn">', unsafe_allow_html=True)
    if st.button("🔄  다시 테스트하기", use_container_width=True):
        reset()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="deco-divider">· · · · ·</div>

    <!-- 진로 탐색 안내 박스 -->
    <div style="background: linear-gradient(135deg, #fdf4ff, #fef9ec);
                border-radius: 20px; padding: 1.4rem 1.6rem;
                border: 2px solid #e9d5ff; margin-bottom: 1rem;">
      <div style="font-size:0.95rem; font-weight:800; color:#7c3aed; margin-bottom:0.8rem;">
        🔎 더 깊이 탐색하고 싶다면?
      </div>
      <div style="font-size:0.88rem; color:#4a1d96; line-height:2;">
        이 테스트는 <b>간단한 참고용</b>이에요!<br/>
        진짜 나에게 맞는 직업·학과를 찾으려면 아래 공식 사이트에서
        <b>전문 검사</b>를 꼭 받아보세요 🌟
      </div>
      <div style="margin-top:1rem; display:flex; flex-direction:column; gap:0.55rem;">

        <div style="background:#fff; border-radius:14px; padding:0.7rem 1rem;
                    border:1.5px solid #e9d5ff; display:flex; align-items:center; gap:0.7rem;">
          <span style="font-size:1.4rem;">🎓</span>
          <div>
            <div style="font-size:0.9rem; font-weight:700; color:#6d28d9;">커리어넷 (진로정보망)</div>
            <div style="font-size:0.8rem; color:#7c5cbf; margin-top:0.1rem;">
              직업·학과 탐색 + 무료 직업흥미검사 제공<br/>
              <b>www.career.go.kr</b>
            </div>
          </div>
        </div>

        <div style="background:#fff; border-radius:14px; padding:0.7rem 1rem;
                    border:1.5px solid #e9d5ff; display:flex; align-items:center; gap:0.7rem;">
          <span style="font-size:1.4rem;">💼</span>
          <div>
            <div style="font-size:0.9rem; font-weight:700; color:#6d28d9;">워크넷 (고용노동부)</div>
            <div style="font-size:0.8rem; color:#7c5cbf; margin-top:0.1rem;">
              직업심리검사 + 직업·채용 정보 탐색<br/>
              <b>www.work.go.kr</b>
            </div>
          </div>
        </div>

        <div style="background:#fff; border-radius:14px; padding:0.7rem 1rem;
                    border:1.5px solid #e9d5ff; display:flex; align-items:center; gap:0.7rem;">
          <span style="font-size:1.4rem;">🏫</span>
          <div>
            <div style="font-size:0.9rem; font-weight:700; color:#6d28d9;">학교 진로 선생님</div>
            <div style="font-size:0.8rem; color:#7c5cbf; margin-top:0.1rem;">
              학교 진로상담실에서 1:1 상담을 받아보세요!<br/>
              나만을 위한 맞춤 진로 조언을 해 주실 거예요 🌸
            </div>
          </div>
        </div>

      </div>
    </div>

    <div style="text-align:center; font-size:0.8rem; color:#c4b5fd; padding-bottom:2rem; margin-top:0.5rem;">
      결과는 참고용이에요 🌈 어떤 유형이든 노력하면 꿈을 이룰 수 있어요! 💪
    </div>
    """, unsafe_allow_html=True)
