import streamlit as st

# ─── 페이지 설정 ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🌟 MBTI 직업 탐험대",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── MBTI 데이터 ───────────────────────────────────────────────────────────────
MBTI_DATA = {
    "INTJ": {
        "emoji": "🦉",
        "nickname": "전략가",
        "color": "#4A00E0",
        "light": "#e8e0ff",
        "desc": "논리적이고 독립적인 전략 설계자",
        "jobs": [
            {"title": "데이터 과학자", "emoji": "📊", "desc": "빅데이터를 분석해 인사이트를 도출합니다", "salary": "★★★★★"},
            {"title": "전략 컨설턴트", "emoji": "♟️", "desc": "기업의 장기 전략을 수립하고 실행합니다", "salary": "★★★★★"},
            {"title": "AI 연구원", "emoji": "🤖", "desc": "인공지능 알고리즘을 연구 개발합니다", "salary": "★★★★★"},
            {"title": "보안 전문가", "emoji": "🔐", "desc": "사이버 위협을 분석하고 방어합니다", "salary": "★★★★☆"},
            {"title": "건축가", "emoji": "🏛️", "desc": "공간과 구조를 체계적으로 설계합니다", "salary": "★★★★☆"},
        ],
    },
    "INTP": {
        "emoji": "🧪",
        "nickname": "논리학자",
        "color": "#0072ff",
        "light": "#d6eaff",
        "desc": "창의적인 발명가, 지식에 목마른 사상가",
        "jobs": [
            {"title": "소프트웨어 엔지니어", "emoji": "💻", "desc": "복잡한 문제를 코드로 해결합니다", "salary": "★★★★★"},
            {"title": "철학자·윤리학자", "emoji": "🤔", "desc": "사회의 근본 질문을 탐구합니다", "salary": "★★★☆☆"},
            {"title": "물리학자", "emoji": "⚛️", "desc": "우주의 법칙을 수식으로 풀어냅니다", "salary": "★★★★☆"},
            {"title": "게임 개발자", "emoji": "🎮", "desc": "창의적인 세계관을 게임으로 구현합니다", "salary": "★★★★☆"},
            {"title": "경제학자", "emoji": "📈", "desc": "경제 현상을 분석하고 예측합니다", "salary": "★★★★☆"},
        ],
    },
    "ENTJ": {
        "emoji": "👑",
        "nickname": "통솔자",
        "color": "#c0392b",
        "light": "#ffe0de",
        "desc": "대담하고 상상력 넘치는 강인한 리더",
        "jobs": [
            {"title": "CEO·창업가", "emoji": "🚀", "desc": "조직을 이끌며 비전을 실현합니다", "salary": "★★★★★"},
            {"title": "변호사", "emoji": "⚖️", "desc": "논리와 설득으로 정의를 추구합니다", "salary": "★★★★★"},
            {"title": "정치인", "emoji": "🏛️", "desc": "사회 변화를 이끄는 리더십을 발휘합니다", "salary": "★★★★☆"},
            {"title": "금융 매니저", "emoji": "💰", "desc": "대규모 자산을 전략적으로 운용합니다", "salary": "★★★★★"},
            {"title": "프로젝트 매니저", "emoji": "📋", "desc": "팀을 조율해 목표를 달성합니다", "salary": "★★★★☆"},
        ],
    },
    "ENTP": {
        "emoji": "🔥",
        "nickname": "변론가",
        "color": "#f39c12",
        "light": "#fff3cd",
        "desc": "아이디어가 넘치는 토론의 달인",
        "jobs": [
            {"title": "스타트업 창업가", "emoji": "💡", "desc": "혁신적인 아이디어로 시장을 바꿉니다", "salary": "★★★★★"},
            {"title": "마케팅 디렉터", "emoji": "📣", "desc": "창의적인 전략으로 브랜드를 키웁니다", "salary": "★★★★☆"},
            {"title": "변리사", "emoji": "📝", "desc": "발명과 지식재산을 법적으로 보호합니다", "salary": "★★★★★"},
            {"title": "저널리스트", "emoji": "📰", "desc": "세상의 이슈를 날카롭게 보도합니다", "salary": "★★★☆☆"},
            {"title": "PD·크리에이터", "emoji": "🎬", "desc": "독창적인 콘텐츠로 대중을 사로잡습니다", "salary": "★★★★☆"},
        ],
    },
    "INFJ": {
        "emoji": "🌙",
        "nickname": "옹호자",
        "color": "#6c3483",
        "light": "#f0e6ff",
        "desc": "신비롭고 이상적인 꿈을 가진 조력자",
        "jobs": [
            {"title": "심리상담사", "emoji": "💜", "desc": "마음의 상처를 치유하고 성장을 돕습니다", "salary": "★★★★☆"},
            {"title": "작가·소설가", "emoji": "✍️", "desc": "깊은 통찰을 이야기로 표현합니다", "salary": "★★★☆☆"},
            {"title": "사회복지사", "emoji": "🤝", "desc": "사회적 약자를 위한 실질적 지원을 합니다", "salary": "★★★☆☆"},
            {"title": "인문학 교수", "emoji": "📚", "desc": "인간과 사회에 대한 깊은 이해를 가르칩니다", "salary": "★★★★☆"},
            {"title": "NGO 활동가", "emoji": "🌍", "desc": "세상을 더 나은 곳으로 만들기 위해 일합니다", "salary": "★★★☆☆"},
        ],
    },
    "INFP": {
        "emoji": "🌈",
        "nickname": "중재자",
        "color": "#1abc9c",
        "light": "#d5f5ef",
        "desc": "시적 감수성을 가진 이상주의자",
        "jobs": [
            {"title": "예술가·화가", "emoji": "🎨", "desc": "감정과 상상을 예술로 표현합니다", "salary": "★★★☆☆"},
            {"title": "UX 디자이너", "emoji": "✨", "desc": "사용자 경험을 아름답게 디자인합니다", "salary": "★★★★★"},
            {"title": "음악가", "emoji": "🎵", "desc": "감정을 음악이라는 언어로 전달합니다", "salary": "★★★☆☆"},
            {"title": "환경 활동가", "emoji": "🌿", "desc": "지구와 자연을 위해 목소리를 높입니다", "salary": "★★★☆☆"},
            {"title": "도서관 사서", "emoji": "📖", "desc": "지식의 보고를 정리하고 연결합니다", "salary": "★★★☆☆"},
        ],
    },
    "ENFJ": {
        "emoji": "☀️",
        "nickname": "선도자",
        "color": "#e74c3c",
        "light": "#fde8e8",
        "desc": "카리스마 넘치는 영감을 주는 리더",
        "jobs": [
            {"title": "교사·강사", "emoji": "🏫", "desc": "학생들의 잠재력을 이끌어냅니다", "salary": "★★★☆☆"},
            {"title": "인사 관리자", "emoji": "👥", "desc": "조직 내 사람들의 성장을 지원합니다", "salary": "★★★★☆"},
            {"title": "방송인·MC", "emoji": "🎤", "desc": "따뜻한 에너지로 대중과 소통합니다", "salary": "★★★★☆"},
            {"title": "코치·멘토", "emoji": "🏆", "desc": "개인의 목표 달성을 옆에서 도웁니다", "salary": "★★★★☆"},
            {"title": "외교관", "emoji": "🌐", "desc": "국가 간 가교 역할을 수행합니다", "salary": "★★★★★"},
        ],
    },
    "ENFP": {
        "emoji": "🎉",
        "nickname": "활동가",
        "color": "#e91e63",
        "light": "#fce4ec",
        "desc": "열정적이고 창의적인 자유로운 영혼",
        "jobs": [
            {"title": "광고 크리에이터", "emoji": "🎯", "desc": "창의적인 캠페인으로 감동을 줍니다", "salary": "★★★★☆"},
            {"title": "배우·연기자", "emoji": "🎭", "desc": "다양한 캐릭터를 통해 이야기를 전달합니다", "salary": "★★★☆☆"},
            {"title": "이벤트 플래너", "emoji": "🎊", "desc": "특별한 순간을 기획하고 연출합니다", "salary": "★★★★☆"},
            {"title": "유튜버·인플루언서", "emoji": "📱", "desc": "개성 있는 콘텐츠로 팔로워를 사로잡습니다", "salary": "★★★☆☆"},
            {"title": "여행 작가", "emoji": "✈️", "desc": "세계를 누비며 경험을 글로 담습니다", "salary": "★★★☆☆"},
        ],
    },
    "ISTJ": {
        "emoji": "🏛️",
        "nickname": "현실주의자",
        "color": "#2c3e50",
        "light": "#e8ecf0",
        "desc": "철저하고 신뢰할 수 있는 관리자",
        "jobs": [
            {"title": "공무원·행정직", "emoji": "🏢", "desc": "체계적으로 공공 서비스를 운영합니다", "salary": "★★★★☆"},
            {"title": "회계사", "emoji": "🧾", "desc": "정확한 수치로 재무를 관리합니다", "salary": "★★★★☆"},
            {"title": "판사", "emoji": "⚖️", "desc": "법과 원칙에 따라 공정하게 판결합니다", "salary": "★★★★★"},
            {"title": "의사·외과의", "emoji": "⚕️", "desc": "철저한 지식과 기술로 생명을 지킵니다", "salary": "★★★★★"},
            {"title": "군인·경찰", "emoji": "🛡️", "desc": "원칙과 책임감으로 사회를 수호합니다", "salary": "★★★★☆"},
        ],
    },
    "ISFJ": {
        "emoji": "🌸",
        "nickname": "수호자",
        "color": "#27ae60",
        "light": "#d5f5e3",
        "desc": "헌신적이고 따뜻한 보호자",
        "jobs": [
            {"title": "간호사", "emoji": "💉", "desc": "환자 곁에서 섬세하게 돌봄을 제공합니다", "salary": "★★★★☆"},
            {"title": "초등학교 교사", "emoji": "🍎", "desc": "아이들의 첫 배움을 함께합니다", "salary": "★★★☆☆"},
            {"title": "영양사", "emoji": "🥗", "desc": "건강한 식습관을 설계하고 조언합니다", "salary": "★★★☆☆"},
            {"title": "사회복지사", "emoji": "💛", "desc": "도움이 필요한 이들의 손을 잡아줍니다", "salary": "★★★☆☆"},
            {"title": "비서·어시스턴트", "emoji": "📌", "desc": "꼼꼼함으로 조직을 든든히 지원합니다", "salary": "★★★☆☆"},
        ],
    },
    "ESTJ": {
        "emoji": "💼",
        "nickname": "경영자",
        "color": "#d35400",
        "light": "#fde8d8",
        "desc": "탁월한 관리 능력을 가진 경영자",
        "jobs": [
            {"title": "기업 임원", "emoji": "👔", "desc": "조직의 목표를 달성하는 강한 리더입니다", "salary": "★★★★★"},
            {"title": "부동산 개발자", "emoji": "🏗️", "desc": "부동산을 분석하고 개발 전략을 세웁니다", "salary": "★★★★★"},
            {"title": "군 장교", "emoji": "🎖️", "desc": "강한 리더십으로 부대를 이끕니다", "salary": "★★★★☆"},
            {"title": "금융 분석가", "emoji": "📉", "desc": "시장을 분석해 투자 결정을 지원합니다", "salary": "★★★★★"},
            {"title": "학교 교장", "emoji": "🎓", "desc": "학교 전체를 효율적으로 운영합니다", "salary": "★★★★☆"},
        ],
    },
    "ESFJ": {
        "emoji": "🤗",
        "nickname": "집정관",
        "color": "#8e44ad",
        "light": "#f3e5f5",
        "desc": "인기 많고 배려심 넘치는 사교가",
        "jobs": [
            {"title": "이벤트 코디네이터", "emoji": "🎀", "desc": "사람들이 행복한 순간을 만들어냅니다", "salary": "★★★★☆"},
            {"title": "항공 승무원", "emoji": "✈️", "desc": "친절한 서비스로 편안한 여행을 만듭니다", "salary": "★★★★☆"},
            {"title": "영업 매니저", "emoji": "🤝", "desc": "관계를 통해 신뢰를 쌓고 성과를 냅니다", "salary": "★★★★★"},
            {"title": "웨딩 플래너", "emoji": "💍", "desc": "소중한 순간을 완벽하게 기획합니다", "salary": "★★★★☆"},
            {"title": "홍보 담당자", "emoji": "📢", "desc": "브랜드 이미지를 따뜻하게 관리합니다", "salary": "★★★★☆"},
        ],
    },
    "ISTP": {
        "emoji": "🔧",
        "nickname": "만능재주꾼",
        "color": "#607d8b",
        "light": "#eceff1",
        "desc": "손재주 있고 냉정한 분석가",
        "jobs": [
            {"title": "항공 파일럿", "emoji": "🛩️", "desc": "침착하게 항공기를 조종합니다", "salary": "★★★★★"},
            {"title": "기계 엔지니어", "emoji": "⚙️", "desc": "정교한 기계 시스템을 설계·제작합니다", "salary": "★★★★☆"},
            {"title": "법의학자", "emoji": "🔬", "desc": "과학적 분석으로 사건의 실마리를 찾습니다", "salary": "★★★★☆"},
            {"title": "운동선수", "emoji": "🏋️", "desc": "강인한 신체와 순발력을 발휘합니다", "salary": "★★★★☆"},
            {"title": "IT 기술지원", "emoji": "🖥️", "desc": "기술 문제를 빠르고 정확하게 해결합니다", "salary": "★★★★☆"},
        ],
    },
    "ISFP": {
        "emoji": "🎨",
        "nickname": "모험가",
        "color": "#00897b",
        "light": "#e0f2f1",
        "desc": "자유로운 영혼의 예술적 탐험가",
        "jobs": [
            {"title": "패션 디자이너", "emoji": "👗", "desc": "트렌드를 읽고 스타일을 창조합니다", "salary": "★★★★☆"},
            {"title": "사진작가", "emoji": "📷", "desc": "순간의 아름다움을 영원히 담습니다", "salary": "★★★☆☆"},
            {"title": "플로리스트", "emoji": "💐", "desc": "꽃으로 감동적인 공간을 연출합니다", "salary": "★★★☆☆"},
            {"title": "요리사·셰프", "emoji": "👨‍🍳", "desc": "감각적인 요리로 미각을 자극합니다", "salary": "★★★★☆"},
            {"title": "물리치료사", "emoji": "🏃", "desc": "몸의 회복을 섬세하게 도와드립니다", "salary": "★★★★☆"},
        ],
    },
    "ESTP": {
        "emoji": "⚡",
        "nickname": "사업가",
        "color": "#e64a19",
        "light": "#fbe9e7",
        "desc": "눈치 빠르고 에너지 넘치는 행동파",
        "jobs": [
            {"title": "기업가·사업가", "emoji": "💸", "desc": "빠른 판단력으로 사업 기회를 잡습니다", "salary": "★★★★★"},
            {"title": "스포츠 코치", "emoji": "🏅", "desc": "선수의 잠재력을 극대화합니다", "salary": "★★★★☆"},
            {"title": "경찰·형사", "emoji": "🔍", "desc": "현장에서 빠르게 상황을 파악합니다", "salary": "★★★★☆"},
            {"title": "트레이더·딜러", "emoji": "📊", "desc": "실시간 시장에서 기민하게 거래합니다", "salary": "★★★★★"},
            {"title": "응급구조사", "emoji": "🚑", "desc": "위기 상황에서 침착하게 생명을 구합니다", "salary": "★★★★☆"},
        ],
    },
    "ESFP": {
        "emoji": "🌟",
        "nickname": "연예인",
        "color": "#f06292",
        "light": "#fce4ec",
        "desc": "즉흥적이고 에너지 넘치는 엔터테이너",
        "jobs": [
            {"title": "아이돌·연예인", "emoji": "🎤", "desc": "무대 위에서 빛나는 끼를 발산합니다", "salary": "★★★★★"},
            {"title": "뷰티 크리에이터", "emoji": "💄", "desc": "트렌디한 뷰티 콘텐츠로 팬을 모읍니다", "salary": "★★★★☆"},
            {"title": "파티 플래너", "emoji": "🎊", "desc": "신나고 즐거운 파티를 완벽히 기획합니다", "salary": "★★★★☆"},
            {"title": "바리스타·바텐더", "emoji": "☕", "desc": "감각적인 드링크로 분위기를 만듭니다", "salary": "★★★☆☆"},
            {"title": "소셜 미디어 매니저", "emoji": "📲", "desc": "트렌드에 맞는 콘텐츠로 팔로워를 늘립니다", "salary": "★★★★☆"},
        ],
    },
}

MBTI_GROUPS = {
    "🧠 분석가형": ["INTJ", "INTP", "ENTJ", "ENTP"],
    "💚 외교관형": ["INFJ", "INFP", "ENFJ", "ENFP"],
    "🛡️ 관리자형": ["ISTJ", "ISFJ", "ESTJ", "ESFJ"],
    "🎯 탐험가형": ["ISTP", "ISFP", "ESTP", "ESFP"],
}

# ─── 스타일 ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');

* { font-family: 'Noto Sans KR', sans-serif; box-sizing: border-box; }

/* 배경 */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 40%, #24243e 100%);
    min-height: 100vh;
}

/* 기본 텍스트 */
.stApp, .stApp * { color: #f0f0ff; }

/* 히어로 헤더 */
.hero-header {
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
}
.hero-title {
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(90deg, #a78bfa, #f472b6, #60a5fa, #34d399);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientShift 4s ease infinite;
    line-height: 1.2;
    margin: 0;
}
.hero-sub {
    font-size: 1.15rem;
    color: #c4b5fd;
    margin-top: 0.8rem;
    font-weight: 400;
    letter-spacing: 0.05em;
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* 구분선 */
.fancy-divider {
    height: 3px;
    background: linear-gradient(90deg, transparent, #a78bfa, #f472b6, #60a5fa, transparent);
    border: none;
    margin: 1.5rem auto;
    width: 60%;
    border-radius: 99px;
}

/* 그룹 라벨 */
.group-label {
    font-size: 1.1rem;
    font-weight: 700;
    color: #c4b5fd;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.5rem 0 0.3rem;
    margin-bottom: 0.5rem;
}

/* MBTI 카드 버튼 */
div[data-testid="column"] .stButton > button {
    width: 100%;
    border-radius: 18px;
    padding: 1.1rem 0.5rem;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.25s ease;
    border: 2px solid rgba(255,255,255,0.15);
    background: rgba(255,255,255,0.06);
    color: #f0f0ff;
    letter-spacing: 0.05em;
}
div[data-testid="column"] .stButton > button:hover {
    transform: translateY(-4px) scale(1.04);
    border-color: rgba(167,139,250,0.7);
    background: rgba(167,139,250,0.18);
    box-shadow: 0 12px 40px rgba(167,139,250,0.35);
    color: #fff;
}
div[data-testid="column"] .stButton > button:active {
    transform: translateY(-1px) scale(1.01);
}

/* 선택된 MBTI 배너 */
.selected-banner {
    border-radius: 24px;
    padding: 2rem 2.5rem;
    text-align: center;
    margin: 1.5rem 0;
    position: relative;
    overflow: hidden;
}
.selected-banner::before {
    content: '';
    position: absolute;
    inset: 0;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(8px);
}
.selected-banner-inner { position: relative; z-index: 1; }
.selected-banner-emoji { font-size: 4rem; display: block; margin-bottom: 0.3rem; }
.selected-banner-name {
    font-size: 2.8rem;
    font-weight: 900;
    color: #fff;
    text-shadow: 0 0 40px rgba(255,255,255,0.6);
}
.selected-banner-nick {
    font-size: 1.3rem;
    color: rgba(255,255,255,0.85);
    margin-top: 0.2rem;
    font-weight: 500;
}
.selected-banner-desc {
    font-size: 1rem;
    color: rgba(255,255,255,0.7);
    margin-top: 0.5rem;
}

/* 직업 카드 섹션 헤더 */
.jobs-header {
    font-size: 1.4rem;
    font-weight: 700;
    color: #e0d7ff;
    margin: 1.5rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* 직업 카드 */
.job-card {
    border-radius: 18px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    background: rgba(255,255,255,0.06);
    border: 1.5px solid rgba(255,255,255,0.12);
    backdrop-filter: blur(12px);
    transition: transform 0.2s, box-shadow 0.2s;
    position: relative;
    overflow: hidden;
}
.job-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 5px;
    border-radius: 99px 0 0 99px;
}
.job-card:hover {
    transform: translateX(6px);
    box-shadow: 0 8px 32px rgba(167,139,250,0.2);
}
.job-card-header {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin-bottom: 0.4rem;
}
.job-emoji { font-size: 1.8rem; }
.job-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: #f0f0ff;
}
.job-desc {
    font-size: 0.9rem;
    color: rgba(220,210,255,0.8);
    margin-top: 0.3rem;
    line-height: 1.5;
}
.job-salary {
    margin-top: 0.5rem;
    font-size: 0.95rem;
    color: #fbbf24;
    letter-spacing: 0.03em;
}

/* 뒤로가기 버튼 */
.stButton > button[kind="secondary"] {
    background: rgba(255,255,255,0.08) !important;
    border: 1.5px solid rgba(255,255,255,0.2) !important;
    color: #c4b5fd !important;
    border-radius: 12px !important;
    padding: 0.5rem 1.2rem !important;
}

/* 통계 배지 */
.stat-row {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
    margin: 1rem 0;
}
.stat-badge {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 99px;
    padding: 0.35rem 1rem;
    font-size: 0.85rem;
    color: #c4b5fd;
}

/* 제거: Streamlit 기본 UI 요소 */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 900px; }
div[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ─── 상태 초기화 ───────────────────────────────────────────────────────────────
if "selected_mbti" not in st.session_state:
    st.session_state.selected_mbti = None

# ─── 히어로 헤더 ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
  <p class="hero-title">🔮 MBTI 직업 탐험대</p>
  <p class="hero-sub">✨ 나의 성격 유형에 맞는 꿈의 직업을 발견해보세요! ✨</p>
</div>
<hr class="fancy-divider"/>
""", unsafe_allow_html=True)

# ─── 결과 화면 ─────────────────────────────────────────────────────────────────
if st.session_state.selected_mbti:
    key  = st.session_state.selected_mbti
    data = MBTI_DATA[key]
    color = data["color"]
    light = data["light"]

    # 뒤로가기
    if st.button("← 다시 선택하기"):
        st.session_state.selected_mbti = None
        st.rerun()

    # 선택된 MBTI 배너
    st.markdown(f"""
    <div class="selected-banner" style="background: linear-gradient(135deg, {color}cc, {color}44); border: 2px solid {color}88;">
      <div class="selected-banner-inner">
        <span class="selected-banner-emoji">{data['emoji']}</span>
        <div class="selected-banner-name">{key}</div>
        <div class="selected-banner-nick">💫 {data['nickname']} 💫</div>
        <div class="selected-banner-desc">🌟 {data['desc']}</div>
      </div>
    </div>
    <div class="stat-row">
      <span class="stat-badge">🎯 추천 직업 {len(data['jobs'])}가지</span>
      <span class="stat-badge">💡 성격 기반 매칭</span>
      <span class="stat-badge">🚀 진로 탐색 완료</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="jobs-header">🏆 추천 직업 Top 5</div>', unsafe_allow_html=True)

    accent_colors = ["#a78bfa", "#f472b6", "#60a5fa", "#34d399", "#fbbf24"]
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

    for i, job in enumerate(data["jobs"]):
        acc = accent_colors[i % len(accent_colors)]
        st.markdown(f"""
        <div class="job-card" style="border-color: {acc}44;">
          <div style="position:absolute;left:0;top:0;bottom:0;width:5px;background:{acc};border-radius:99px 0 0 99px;"></div>
          <div class="job-card-header">
            <span class="job-emoji">{job['emoji']}</span>
            <div>
              <div class="job-title">{medals[i]} {job['title']}</div>
            </div>
          </div>
          <div class="job-desc">📌 {job['desc']}</div>
          <div class="job-salary">💰 연봉 수준 &nbsp; {job['salary']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <hr class="fancy-divider" style="margin:2rem auto;"/>
    <div style="text-align:center; color:#a78bfa; font-size:0.95rem; padding-bottom:2rem;">
      🌟 더 자세한 직업 정보는 <b>커리어넷</b>이나 <b>워크넷</b>에서 탐색해보세요! 🌟<br/>
      <span style="color:#c4b5fd; font-size:0.85rem; display:block; margin-top:0.5rem;">
        💡 MBTI는 참고 지표일 뿐, 가장 중요한 건 나의 열정과 노력이에요! 💪
      </span>
    </div>
    """, unsafe_allow_html=True)

# ─── MBTI 선택 화면 ────────────────────────────────────────────────────────────
else:
    st.markdown("""
    <div style="text-align:center; font-size:1.1rem; color:#c4b5fd; margin-bottom:1.5rem;">
      👇 아래에서 나의 MBTI를 선택해보세요!
    </div>
    """, unsafe_allow_html=True)

    for group_name, mbti_list in MBTI_GROUPS.items():
        st.markdown(f'<div class="group-label">{group_name}</div>', unsafe_allow_html=True)
        cols = st.columns(4)
        for j, mbti in enumerate(mbti_list):
            d = MBTI_DATA[mbti]
            with cols[j]:
                label = f"{d['emoji']}\n{mbti}\n{d['nickname']}"
                if st.button(label, key=f"btn_{mbti}", use_container_width=True):
                    st.session_state.selected_mbti = mbti
                    st.rerun()
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    st.markdown("""
    <hr class="fancy-divider" style="margin:2rem auto;"/>
    <div style="text-align:center; padding-bottom:2rem;">
      <div style="font-size:1rem; color:#a78bfa; font-weight:600; margin-bottom:0.5rem;">
        🎓 이 서비스는 진로 교육을 위한 참고 자료입니다
      </div>
      <div style="font-size:0.85rem; color:rgba(196,181,253,0.65);">
        16가지 MBTI 유형 × 각 5개 추천 직업 = 80가지 진로 탐색 🗺️
      </div>
    </div>
    """, unsafe_allow_html=True)
