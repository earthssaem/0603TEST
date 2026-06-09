import streamlit as st
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>일식 · 월식 탐구 시뮬레이터</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Noto Sans KR',sans-serif;background:#e8e4db;display:flex;flex-direction:column;align-items:center;padding:18px 16px 14px;gap:10px;min-height:100vh}
footer{margin-top:4px;font-size:11px;color:#888;text-align:center;line-height:1.6}
footer a{color:inherit;text-decoration:none}
footer a:hover{text-decoration:underline}

/* 헤더 */
.header{display:flex;flex-direction:column;align-items:center;gap:6px;margin-top:2px}
h1{font-size:28px;font-weight:700;color:#1f2d4d;letter-spacing:-.6px;line-height:1.2;text-align:center;margin:0}
.subtitle{font-size:14px;color:#5a6373;line-height:1.5;text-align:center;letter-spacing:-.1px}

.tabs{display:flex;background:#fff;border-radius:10px;padding:3px;gap:3px;border:1px solid rgba(0,0,0,.1);margin-top:6px}
.tab{padding:5px 26px;font-size:13px;font-weight:500;font-family:inherit;border:none;border-radius:7px;cursor:pointer;background:transparent;color:#666;transition:background .15s,color .15s}
.tab.active{background:#1a4fa0;color:#fff}
.card{width:100%;max-width:900px;background:#fff;border-radius:18px;border:1px solid rgba(0,0,0,.09);box-shadow:0 2px 18px rgba(0,0,0,.07);overflow:hidden}
canvas{display:block;width:100%;background:#f2ede3;cursor:grab}
canvas.dragging{cursor:grabbing}
.panel{padding:10px 16px 12px;border-top:1px solid rgba(0,0,0,.08);display:flex;flex-direction:column;gap:9px}

/* 1. 상태 카드 (콤팩트) */
.status-card{display:flex;align-items:stretch;gap:14px;background:#f7f5f0;border:1px solid rgba(0,0,0,.08);border-radius:10px;padding:9px 14px}
.status-main{display:flex;flex-direction:column;gap:3px;flex:1;min-width:0;justify-content:center}
.status-title{font-size:14px;font-weight:700;color:#1a4fa0;letter-spacing:-.2px}
.status-desc{font-size:12px;color:#555;line-height:1.5}
.eye-wrap{display:flex;flex-direction:column;align-items:center;gap:4px;flex-shrink:0;border-left:1px solid rgba(0,0,0,.10);padding-left:14px;justify-content:center}
.eye-title{font-size:10.5px;font-weight:500;color:#666}
#eyeview{width:64px;height:64px;border-radius:7px;display:block}

/* 2. 조작 영역 */
.controls{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:0 2px}
.ctrl-btn{padding:5px 14px;font-size:12px;font-family:inherit;font-weight:500;border:1px solid rgba(0,0,0,.15);border-radius:7px;background:#fff;cursor:pointer;color:#333}
.ctrl-btn:hover{background:#f0f0f0}
.ctrl-btn.playing{background:#1a4fa0;color:#fff;border-color:transparent}
.slider-row{display:flex;align-items:center;gap:8px}
.slider-label{font-size:11.5px;color:#666;white-space:nowrap}
input[type=range]{accent-color:#1a4fa0;cursor:pointer;width:120px}
.slider-val{font-size:11.5px;font-weight:500;color:#333;min-width:50px}
.angle-label{font-size:11.5px;color:#888;margin-left:auto;font-variant-numeric:tabular-nums}

/* 상단 안내 (탭 아래) */
.top-hint{font-size:12px;color:#7a8090;text-align:center;padding:4px 6px 0;letter-spacing:-.1px;line-height:1.55}

/* 시뮬레이터 하단 조작 패널 */
.controls-bottom{display:flex;align-items:center;gap:12px;flex-wrap:wrap;padding:11px 18px;background:#fbfaf6;border-top:1px solid rgba(0,0,0,.08)}
.controls-bottom .angle-label{margin-left:auto}

/* 시뮬레이션 화면 내부 범례 (좌하단 오버레이) */
.canvas-wrap{position:relative}
.legend-overlay{position:absolute;left:12px;bottom:12px;display:flex;flex-direction:column;gap:4px;background:rgba(255,255,255,.78);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);border:1px solid rgba(0,0,0,.08);border-radius:8px;padding:7px 10px;font-size:11px;color:#444;pointer-events:none}
.legend-overlay .leg{display:flex;align-items:center;gap:6px;line-height:1.1}
.legend-overlay .leg-sq{width:11px;height:11px;border-radius:2px;display:inline-block}
.legend-overlay .leg-line{display:inline-block;width:18px;height:0;border-top:1.5px solid rgba(0,0,0,.55)}
.legend-overlay .leg-dash{display:inline-block;width:18px;height:0;border-top:1.5px dashed rgba(0,0,0,.45)}
</style>
</head>
<body>
<div class="header">
  <h1>일식 · 월식 탐구 시뮬레이터</h1>
  <div class="subtitle">태양, 지구, 달의 위치 관계에 따른 식 현상을 탐구해 보세요.</div>
</div>
<div class="tabs">
  <button class="tab active" id="tab-solar" onclick="setMode('solar')">🌑 일식</button>
  <button class="tab"        id="tab-lunar" onclick="setMode('lunar')">🌕 월식</button>
</div>
<div class="top-hint">💡 달과 관측 위치를 드래그하고 거리·공전 속도를 조절하며 식 현상을 탐구해 보세요.</div>
<div class="card">
  <div class="canvas-wrap">
    <canvas id="c"></canvas>
    <div class="legend-overlay">
      <div class="leg"><span class="leg-sq" style="background:rgba(30,30,90,.45)"></span>본그림자</div>
      <div class="leg"><span class="leg-sq" style="background:rgba(120,120,180,.2);border:1px solid rgba(100,100,160,.35)"></span>반그림자</div>
      <div class="leg"><span class="leg-line"></span>본그림자 경계</div>
      <div class="leg"><span class="leg-dash"></span>반그림자 경계</div>
      <div class="leg" id="leg-obs">📍 관측 위치</div>
    </div>
  </div>
  <div class="controls controls-bottom">
    <button class="ctrl-btn" id="btn-play" onclick="toggleAnim()">▶ 공전 시작</button>
    <button class="ctrl-btn" onclick="resetMoon()">↺ 초기 위치</button>
    <div class="slider-row">
      <span class="slider-label">달까지 거리</span>
      <input type="range" id="dist-slider" min="0.45" max="1.7" step="0.01" value="1.0"
             oninput="onDistChange(this.value)">
      <span class="slider-val" id="dist-val">보통</span>
    </div>
    <div class="slider-row">
      <span class="slider-label">공전 속도</span>
      <input type="range" id="speed-slider" min="0.001" max="0.03" step="0.001" value="0.007"
             oninput="onSpeedChange(this.value)">
      <span class="slider-val" id="speed-val">보통</span>
    </div>
    <span class="angle-label" id="angle-label">달 위치: 180°</span>
  </div>
  <div class="panel">
    <div class="status-card">
      <div class="status-main">
        <div class="status-title" id="st-type">—</div>
        <div class="status-desc"  id="st-desc">달을 드래그하거나 ▶ 버튼으로 공전시키세요.</div>
      </div>
      <div class="eye-wrap">
        <div class="eye-title">관측자 시점</div>
        <canvas id="eyeview" width="64" height="64"></canvas>
      </div>
    </div>
  </div>
</div>
<footer>© 2026 제작: 김연경(<a href="mailto:earthssaem@gmail.com">earthssaem@gmail.com</a>)</footer>

<script>
const canvas = document.getElementById('c');
const ctx    = canvas.getContext('2d');
const W = 900, H = 380;
canvas.width = W; canvas.height = H;

const SUN   = { x:110,  y:H/2, r:52 };
const EARTH = { x:640,  y:H/2, r:28 };
const BASE_OX = 150, BASE_OY = 150;
const MOON_R  = 13;

let mode='solar', moonAngle=Math.PI, distMul=1.0;
let observerAngle=Math.PI;
let animating=false, animId=null;
let animSpeed=0.007;

function getRX(){ return BASE_OX*distMul; }
function getRY(){ return BASE_OY*distMul; }
function getMoon(){
  return { x:EARTH.x+getRX()*Math.cos(moonAngle),
           y:EARTH.y+getRY()*Math.sin(moonAngle), r:MOON_R };
}
function getObserver(){
  return { x:EARTH.x+EARTH.r*Math.cos(observerAngle),
           y:EARTH.y+EARTH.r*Math.sin(observerAngle) };
}

// ══════════════════════════════════════════
// 그림자 기하 (정정판)
//   본그림자(umbra) 경계 = 외접선 (태양·달 같은 쪽 접점)
//                          → 외부 닮음중심에서 tip 형성
//   반그림자(penumbra) 경계 = 내접선 (태양 반대쪽 → 달 같은 쪽)
//                            → 달 뒤로 발산
// ══════════════════════════════════════════
function buildShadow(light, caster) {
  const dx = caster.x - light.x, dy = caster.y - light.y;
  const D  = Math.hypot(dx, dy) || 1;
  const ux = dx/D, uy = dy/D;
  const nx = -uy, ny = ux;

  // 본그림자 tip: 외부 닮음중심 = D·r / (R−r)  (caster 기준 거리)
  const tipDist = D * caster.r / Math.max(0.001, light.r - caster.r);
  const tip = { x: caster.x + ux*tipDist, y: caster.y + uy*tipDist };

  // 달 접점 (수직 근사 — 교육용으로 충분)
  const cT = { x: caster.x + nx*caster.r, y: caster.y + ny*caster.r };
  const cB = { x: caster.x - nx*caster.r, y: caster.y - ny*caster.r };

  // 본그림자(외접선): 태양 같은 쪽 접점
  const sunUT = { x: light.x + nx*light.r, y: light.y + ny*light.r };
  const sunUB = { x: light.x - nx*light.r, y: light.y - ny*light.r };
  // 반그림자(내접선): 태양 반대쪽 접점
  const sunPT = { x: light.x - nx*light.r, y: light.y - ny*light.r };
  const sunPB = { x: light.x + nx*light.r, y: light.y + ny*light.r };

  const FAR = 1400;
  function farPt(from, through) {
    const ddx=through.x-from.x, ddy=through.y-from.y, l=Math.hypot(ddx,ddy)||1;
    return { x: through.x + ddx/l*FAR, y: through.y + ddy/l*FAR };
  }

  // 본그림자 경계는 tip을 지나가지만, 시각화는 cT→tip→cB 삼각형으로 충분
  // 경계선(점선/실선) 끝점만 별도 연장
  const umbraTopFar = farPt(sunUT, cT);
  const umbraBotFar = farPt(sunUB, cB);
  const penTopFar   = farPt(sunPT, cT);
  const penBotFar   = farPt(sunPB, cB);

  return {
    ux, uy, nx, ny, D, tip, tipDist,
    cT, cB,
    sunUT, sunUB, sunPT, sunPB,
    umbraTopFar, umbraBotFar, penTopFar, penBotFar
  };
}

// ══════════════════════════════════════════
// 점 → 그림자 영역 판정
// ══════════════════════════════════════════
function pointInShadow(light, caster, px, py) {
  const dx=caster.x-light.x, dy=caster.y-light.y;
  const D=Math.hypot(dx,dy)||1;
  const ux=dx/D, uy=dy/D;

  const rx=px-caster.x, ry=py-caster.y;
  const along = rx*ux + ry*uy;
  const perp  = Math.abs(-rx*uy + ry*ux);
  if (along < -caster.r) return 'none';

  const tipDist = D * caster.r / Math.max(0.001, light.r - caster.r);

  // 본그림자: caster 표면(r)에서 tip(0)으로 수렴
  if (along >= 0 && along <= tipDist) {
    const umbHalf = caster.r * (1 - along/tipDist);
    if (perp <= umbHalf) return 'umbra';
  }
  // 금환(antumbra): tip 너머에서 다시 발산
  if (along > tipDist) {
    const antHalf = caster.r * (along/tipDist - 1);
    if (perp <= antHalf) return 'antumbra';
  }

  // 반그림자: 내접선 발산 콘  반폭 = r + along·(R+r)/D
  if (along > -caster.r) {
    const a = Math.max(0, along);
    const penHalf = caster.r + a * (light.r + caster.r) / D;
    if (perp <= penHalf) return 'penumbra';
  }

  return 'none';
}

function _line(a, b) {
  ctx.beginPath(); ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y); ctx.stroke();
}

function drawShadowCones(light, caster) {
  const sh = buildShadow(light, caster);
  ctx.save();

  // 채우기는 caster 뒤쪽만
  ctx.save();
  ctx.beginPath();
  ctx.rect(caster.x - caster.r, 0, W - caster.x + caster.r, H);
  ctx.clip();

  // 반그림자(발산): cT → penTopFar → penBotFar → cB
  ctx.fillStyle='rgba(140,140,200,0.16)';
  ctx.beginPath();
  ctx.moveTo(sh.cT.x, sh.cT.y);
  ctx.lineTo(sh.penTopFar.x, sh.penTopFar.y);
  ctx.lineTo(sh.penBotFar.x, sh.penBotFar.y);
  ctx.lineTo(sh.cB.x, sh.cB.y);
  ctx.closePath(); ctx.fill();

  // 본그림자(수렴): 단순 삼각형 cT → tip → cB
  ctx.fillStyle='rgba(30,30,90,0.34)';
  ctx.beginPath();
  ctx.moveTo(sh.cT.x,  sh.cT.y);
  ctx.lineTo(sh.tip.x, sh.tip.y);
  ctx.lineTo(sh.cB.x,  sh.cB.y);
  ctx.closePath(); ctx.fill();

  ctx.restore(); // clip 해제

  // antumbra (일식 전용): tip 너머 발산
  if (mode==='solar') {
    const ANT_LEN = 380;
    const halfAtFar = caster.r * ANT_LEN / sh.tipDist;
    const ax = sh.tip.x + sh.ux*ANT_LEN;
    const ay = sh.tip.y + sh.uy*ANT_LEN;
    const a1 = { x: ax + sh.nx*halfAtFar, y: ay + sh.ny*halfAtFar };
    const a2 = { x: ax - sh.nx*halfAtFar, y: ay - sh.ny*halfAtFar };
    ctx.fillStyle='rgba(100,70,160,0.12)';
    ctx.beginPath();
    ctx.moveTo(sh.tip.x, sh.tip.y);
    ctx.lineTo(a1.x, a1.y);
    ctx.lineTo(a2.x, a2.y);
    ctx.closePath(); ctx.fill();
  }

  // 경계선: 태양 접점에서 시작 (선만)
  ctx.save();
  ctx.strokeStyle='rgba(0,0,0,0.40)'; ctx.lineWidth=1.1; ctx.setLineDash([6,5]);
  _line(sh.sunPT, sh.penTopFar);
  _line(sh.sunPB, sh.penBotFar);
  ctx.strokeStyle='rgba(0,0,0,0.55)'; ctx.lineWidth=1.2; ctx.setLineDash([]);
  _line(sh.sunUT, sh.umbraTopFar);
  _line(sh.sunUB, sh.umbraBotFar);
  ctx.restore();

  ctx.restore();
  return sh;
}

// ══════════════════════════════════════════
// 천체 표면 그림자 색칠
// ══════════════════════════════════════════
function drawBodyShadow(body, light, caster) {
  const isSolar = (mode==='solar');
  const colUmbra = isSolar ? 'rgba(20,20,100,0.65)' : 'rgba(160,40,10,0.70)';
  const colAntu  = 'rgba(160,120,10,0.55)';
  const colPen   = isSolar ? 'rgba(70,70,180,0.35)' : 'rgba(110,50,10,0.38)';

  ctx.save();
  const STEP = 3;
  let umbSegs=[], antuSegs=[], penSegs=[];

  for (let deg=0; deg<360; deg+=STEP) {
    const a = deg*Math.PI/180;
    const px = body.x + body.r*Math.cos(a);
    const py = body.y + body.r*Math.sin(a);
    const reg = pointInShadow(light, caster, px, py);
    if (reg==='umbra')         umbSegs.push(a);
    else if (reg==='antumbra') antuSegs.push(a);
    else if (reg==='penumbra') penSegs.push(a);
  }

  function drawArcs(segs, color, lw) {
    if (!segs.length) return;
    ctx.strokeStyle=color; ctx.lineWidth=lw; ctx.lineCap='round'; ctx.setLineDash([]);
    const step=STEP*Math.PI/180;
    let i=0;
    while(i<segs.length){
      let j=i;
      while(j+1<segs.length && segs[j+1]-segs[j]<step*1.5) j++;
      ctx.beginPath();
      ctx.arc(body.x,body.y,body.r,segs[i],segs[j]+step*0.5);
      ctx.stroke();
      i=j+1;
    }
  }

  drawArcs(penSegs,  colPen,   5);
  drawArcs(umbSegs,  colUmbra, 8);
  drawArcs(antuSegs, colAntu,  7);
  ctx.restore();
}

function drawShadowLabels(sh) {
  const caster = mode==='solar' ? getMoon() : EARTH;
  const along  = Math.min(80, sh.tipDist*0.55);
  const cx = caster.x + sh.ux*along;
  const cy = caster.y + sh.uy*along;

  ctx.save();
  ctx.font='500 11px "Noto Sans KR",sans-serif';
  ctx.textAlign='center';

  ctx.fillStyle='rgba(10,10,70,.78)';
  ctx.fillText('본그림자', cx, cy-2);

  const penOff = caster.r + along*(SUN.r+caster.r)/sh.D + 12;
  ctx.fillStyle='rgba(50,50,140,.70)';
  ctx.fillText('반그림자', cx + sh.nx*penOff, cy + sh.ny*penOff);
  ctx.fillText('반그림자', cx - sh.nx*penOff, cy - sh.ny*penOff);

  ctx.restore();
}

function drawSun() {
  const g=ctx.createRadialGradient(SUN.x,SUN.y,SUN.r*.8,SUN.x,SUN.y,SUN.r*2.4);
  g.addColorStop(0,'rgba(255,210,80,.35)'); g.addColorStop(1,'rgba(255,130,0,0)');
  ctx.fillStyle=g; ctx.beginPath(); ctx.arc(SUN.x,SUN.y,SUN.r*2.4,0,Math.PI*2); ctx.fill();
  const sg=ctx.createRadialGradient(SUN.x-14,SUN.y-14,4,SUN.x,SUN.y,SUN.r);
  sg.addColorStop(0,'#FFF5C0'); sg.addColorStop(.5,'#FFD040'); sg.addColorStop(1,'#FF8C00');
  ctx.fillStyle=sg; ctx.beginPath(); ctx.arc(SUN.x,SUN.y,SUN.r,0,Math.PI*2); ctx.fill();
}

function drawEarth() {
  const eg=ctx.createRadialGradient(EARTH.x-7,EARTH.y-7,3,EARTH.x,EARTH.y,EARTH.r);
  eg.addColorStop(0,'#90d0ff'); eg.addColorStop(.45,'#2B7FD4'); eg.addColorStop(1,'#0d3a6b');
  ctx.fillStyle=eg; ctx.beginPath(); ctx.arc(EARTH.x,EARTH.y,EARTH.r,0,Math.PI*2); ctx.fill();
  ctx.save(); ctx.globalAlpha=.45; ctx.fillStyle='#7ab850';
  ctx.beginPath(); ctx.ellipse(EARTH.x-5,EARTH.y-5,9,7,.5,0,Math.PI*2); ctx.fill();
  ctx.beginPath(); ctx.ellipse(EARTH.x+7,EARTH.y+4,7,5,-.4,0,Math.PI*2); ctx.fill();
  ctx.restore();
  ctx.strokeStyle='rgba(130,200,255,.3)'; ctx.lineWidth=3.5;
  ctx.beginPath(); ctx.arc(EARTH.x,EARTH.y,EARTH.r+2,0,Math.PI*2); ctx.stroke();
}

function drawMoon(moon, blood) {
  const mg=ctx.createRadialGradient(moon.x-3,moon.y-3,1,moon.x,moon.y,moon.r);
  if(blood){ mg.addColorStop(0,'#dd6633'); mg.addColorStop(.6,'#992211'); mg.addColorStop(1,'#550800'); }
  else      { mg.addColorStop(0,'#eceadf'); mg.addColorStop(.6,'#c0bdb5'); mg.addColorStop(1,'#8a8880'); }
  ctx.fillStyle=mg; ctx.beginPath(); ctx.arc(moon.x,moon.y,moon.r,0,Math.PI*2); ctx.fill();
  if(!blood){
    ctx.save(); ctx.globalAlpha=.18; ctx.fillStyle='#666';
    ctx.beginPath(); ctx.arc(moon.x-3,moon.y-2,2.5,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.arc(moon.x+3,moon.y+3,1.8,0,Math.PI*2); ctx.fill();
    ctx.restore();
  }
}

function drawOrbit() {
  ctx.save();
  ctx.strokeStyle='rgba(80,120,200,.22)'; ctx.lineWidth=.9; ctx.setLineDash([5,8]);
  ctx.beginPath(); ctx.ellipse(EARTH.x,EARTH.y,getRX(),getRY(),0,0,Math.PI*2); ctx.stroke();
  ctx.setLineDash([]); ctx.restore();
}

function drawObserver(region) {
  const obs=getObserver();
  // 지구 표면 법선 방향(바깥쪽)으로 핀을 세움
  const nx = (obs.x - EARTH.x);
  const ny = (obs.y - EARTH.y);
  const nl = Math.hypot(nx, ny) || 1;
  const ux = nx/nl, uy = ny/nl;        // 지구 중심 → 관측자 (바깥 방향)
  const angle = Math.atan2(uy, ux) - Math.PI/2; // 핀 머리가 바깥쪽을 향하도록

  ctx.save();
  ctx.translate(obs.x, obs.y);
  ctx.rotate(angle);

  // 핀 그림자
  ctx.fillStyle='rgba(0,0,0,0.25)';
  ctx.beginPath(); ctx.ellipse(2, 2, 5.5, 2.5, 0, 0, Math.PI*2); ctx.fill();

  // 핀 몸체 (꼬리): 끝점이 (0,0) = 지구 표면, 머리는 위쪽(바깥쪽)
  ctx.beginPath();
  ctx.moveTo(0, 0);
  ctx.lineTo(-5.5, -12);
  ctx.quadraticCurveTo(0, -22, 5.5, -12);
  ctx.closePath();
  const grad = ctx.createLinearGradient(-6, -14, 6, -10);
  grad.addColorStop(0, '#ff5050');
  grad.addColorStop(1, '#c41e1e');
  ctx.fillStyle = grad;
  ctx.fill();
  ctx.strokeStyle = 'rgba(120,0,0,0.5)';
  ctx.lineWidth = 1;
  ctx.stroke();

  // 핀 머리 원
  ctx.beginPath(); ctx.arc(0, -14, 4.5, 0, Math.PI*2);
  const hg = ctx.createRadialGradient(-1.5, -15.5, 0.5, 0, -14, 5);
  hg.addColorStop(0, '#ffd0d0');
  hg.addColorStop(0.5, '#ff4040');
  hg.addColorStop(1, '#a01010');
  ctx.fillStyle = hg;
  ctx.fill();
  ctx.strokeStyle = 'rgba(80,0,0,0.4)';
  ctx.lineWidth = 0.8;
  ctx.stroke();

  // 머리 하이라이트
  ctx.beginPath(); ctx.arc(-1.4, -15.4, 1.4, 0, Math.PI*2);
  ctx.fillStyle = 'rgba(255,255,255,0.6)';
  ctx.fill();

  ctx.restore();
}

function lbl(t,x,y){ ctx.font='400 12px "Noto Sans KR",sans-serif'; ctx.fillStyle='#222'; ctx.textAlign='center'; ctx.fillText(t,x,y); }

// ══════════════════════════════════════════
// 개기일식 코로나 — 은빛 아지랑이 + 반짝임
// ══════════════════════════════════════════
let coronaPhase = 0;       // 반짝임 위상 (애니메이션)
let eyeAnimId = null;

function drawCorona(ex, ew, eh, cx, cy, R) {
  // 어두운 하늘
  ex.fillStyle = '#06060e';
  ex.fillRect(0, 0, ew, eh);

  // 배경 별 살짝
  for (const [sx, sy, r] of [[9,11,0.6],[58,10,0.5],[7,55,0.6],[60,56,0.5]]) {
    ex.fillStyle = 'rgba(200,200,255,0.6)';
    ex.beginPath(); ex.arc(sx, sy, r, 0, Math.PI*2); ex.fill();
  }

  ex.save();
  ex.translate(cx, cy);

  // 1) 부드러운 코로나 헤일로 (방사형 글로우)
  const halo = ex.createRadialGradient(0, 0, R*0.96, 0, 0, R*2.5);
  halo.addColorStop(0,   'rgba(245,245,255,0.55)');
  halo.addColorStop(0.25,'rgba(220,225,245,0.28)');
  halo.addColorStop(0.6, 'rgba(190,200,235,0.10)');
  halo.addColorStop(1,   'rgba(180,190,230,0)');
  ex.fillStyle = halo;
  ex.beginPath(); ex.arc(0, 0, R*2.5, 0, Math.PI*2); ex.fill();

  // 2) 코로나 줄기(streamer) — 위상에 따라 길이/밝기 반짝
  ex.globalCompositeOperation = 'lighter';
  const N = 44;
  for (let i = 0; i < N; i++) {
    const a = (i / N) * Math.PI * 2;
    // 의사난수 시드 (각도별 고정 패턴 + 시간 흔들림)
    const seed = Math.sin(i * 12.9898) * 43758.5453;
    const base = (seed - Math.floor(seed));          // 0~1 고정
    const shimmer = 0.5 + 0.5 * Math.sin(coronaPhase * 2.2 + i * 0.7);
    const len = R * (0.5 + base * 1.4) * (0.7 + 0.3 * shimmer);
    const alpha = (0.10 + base * 0.18) * (0.55 + 0.45 * shimmer);
    const spread = 0.035 + base * 0.025;             // 줄기 폭(라디안)

    const x1 = Math.cos(a) * R * 0.98;
    const y1 = Math.sin(a) * R * 0.98;
    const x2 = Math.cos(a) * (R + len);
    const y2 = Math.sin(a) * (R + len);

    const grad = ex.createLinearGradient(x1, y1, x2, y2);
    grad.addColorStop(0, `rgba(240,242,255,${alpha})`);
    grad.addColorStop(1, 'rgba(210,220,245,0)');
    ex.fillStyle = grad;
    ex.beginPath();
    ex.moveTo(Math.cos(a-spread)*R*0.98, Math.sin(a-spread)*R*0.98);
    ex.lineTo(x2, y2);
    ex.lineTo(Math.cos(a+spread)*R*0.98, Math.sin(a+spread)*R*0.98);
    ex.closePath();
    ex.fill();
  }
  ex.globalCompositeOperation = 'source-over';

  // 3) 채층(홍염) — 림 따라 분홍빛 점들
  for (let k = 0; k < 7; k++) {
    const a = (k / 7) * Math.PI * 2 + 0.4;
    const pulse = 0.6 + 0.4 * Math.sin(coronaPhase * 3 + k);
    ex.fillStyle = `rgba(255,90,120,${0.5 * pulse})`;
    ex.beginPath();
    ex.arc(Math.cos(a)*R, Math.sin(a)*R, R*0.05*pulse, 0, Math.PI*2);
    ex.fill();
  }

  // 4) 얇은 분홍 채층 링
  ex.strokeStyle = 'rgba(255,120,140,0.45)';
  ex.lineWidth = R*0.04;
  ex.beginPath(); ex.arc(0, 0, R*1.01, 0, Math.PI*2); ex.stroke();

  // 5) 달(검은 원반)
  ex.fillStyle = '#050509';
  ex.beginPath(); ex.arc(0, 0, R, 0, Math.PI*2); ex.fill();

  ex.restore();
}

// 코로나 반짝임 애니메이션 루프 (개기일식 인셋일 때만 작동)
function eyeShimmer() {
  eyeAnimId = requestAnimationFrame(eyeShimmer);
  if (mode !== 'solar') return;
  const obs = getObserver();
  const moon = getMoon();
  if (pointInShadow(SUN, moon, obs.x, obs.y) !== 'umbra') return;
  coronaPhase += 0.05;
  drawEyeView();
}

// ══════════════════════════════════════════
// 관측자 시점 (인셋) — obsRegion / classifyLunar 결과와
// 동기화된 실제 기하학 기반 렌더링
// ══════════════════════════════════════════
function drawEyeView() {
  const ec = document.getElementById('eyeview');
  if (!ec) return;
  const ex = ec.getContext('2d');
  const ew = ec.width, eh = ec.height;
  const cx = ew/2, cy = eh/2;
  ex.clearRect(0,0,ew,eh);

  if (mode === 'solar') {
    const obs = getObserver();
    const moon = getMoon();
    const obsReg = pointInShadow(SUN, moon, obs.x, obs.y);
    const R = ew * 0.34;  // 태양 원반 표시 반지름

    // ── 개기일식: 하늘이 어두워지고 코로나가 보인다 ──
    if (obsReg === 'umbra') {
      drawCorona(ex, ew, eh, cx, cy, R);
      return;
    }

    // ── 그 외(부분/금환/없음): 밝은 태양 + 달 실루엣 ──
    // 배경: 균일한 하늘 (태양 가장자리로 오해되는 글로우 없음)
    ex.fillStyle = '#10131c';
    ex.fillRect(0,0,ew,eh);

    // 태양 디스크 (균일한 노란빛 — 가장자리까지 밝게)
    const sg = ex.createRadialGradient(cx-R*0.22, cy-R*0.22, R*0.1, cx, cy, R);
    sg.addColorStop(0,'#FFF3B0');
    sg.addColorStop(0.7,'#FFD83A');
    sg.addColorStop(1,'#FFC400');
    ex.fillStyle = sg;
    ex.beginPath(); ex.arc(cx, cy, R, 0, Math.PI*2); ex.fill();

    if (obsReg === 'none') return;

    // 태양·달 각도차 부호 (어느 쪽으로 가려지는지)
    const sdx = SUN.x-obs.x, sdy = SUN.y-obs.y;
    const mdx = moon.x-obs.x, mdy = moon.y-obs.y;
    const cross = sdx*mdy - sdy*mdx;
    const sign  = cross>=0 ? 1 : -1;

    // 영역별 표시 (실제 기하 + obsRegion에 정합):
    //  antumbra : 달이 태양보다 작고 중앙 정렬     → 금환
    //  penumbra : 달≈태양 크기, perp 위치에 따라 부분 가림
    let moonR_disp, mOff;
    if (obsReg === 'antumbra') {
      moonR_disp = R * 0.66;
      mOff = 0;
    } else { // penumbra
      moonR_disp = R * 1.02;
      // 실제 각도로 부분 가림 정도 계산
      const sD = Math.hypot(sdx,sdy)||1;
      const mD = Math.hypot(mdx,mdy)||1;
      const dot = sdx*mdx + sdy*mdy;
      const angBet = Math.atan2(Math.abs(cross), dot);
      const sAng = SUN.r/sD, mAng = MOON_R/mD;
      const angOuter = sAng + mAng;              // 외부 접촉(반그림자 외곽)
      const angInner = Math.abs(sAng - mAng);    // 내부 접촉(본/금환 경계)
      const t = (angBet - angInner) / Math.max(1e-6, angOuter - angInner);
      const tc = Math.max(0, Math.min(1, t));
      const dMin = Math.abs(R - moonR_disp);     // 안쪽 한계 (거의 0)
      const dMax = R + moonR_disp;               // 바깥 한계 (살짝만 겹침)
      mOff = (dMin + (dMax - dMin) * tc) * sign;
    }

    // 달 (검은 실루엣) — 외곽선 없음
    ex.fillStyle = '#0b0b10';
    ex.beginPath(); ex.arc(cx + mOff, cy, moonR_disp, 0, Math.PI*2); ex.fill();

  } else {

    // 밤하늘 배경
    ex.fillStyle = '#070712';
    ex.fillRect(0,0,ew,eh);
    for(const[sx,sy,r]of[[10,12,0.7],[55,9,0.6],[8,52,0.7],[60,54,0.6],[33,6,0.5],[6,32,0.5]]){
      ex.fillStyle='rgba(200,200,255,0.7)';
      ex.beginPath(); ex.arc(sx,sy,r,0,Math.PI*2); ex.fill();
    }

    const moon = getMoon();
    const lec = classifyLunar(moon);

    // 지구 그림자 축에 대한 달 위치
    const axDx = EARTH.x-SUN.x, axDy = EARTH.y-SUN.y;
    const axD = Math.hypot(axDx,axDy)||1;
    const ux = axDx/axD, uy = axDy/axD;
    const nx = -uy, ny = ux;
    const rx = moon.x-EARTH.x, ry = moon.y-EARTH.y;
    const along = rx*ux+ry*uy;
    const perp  = rx*nx+ry*ny;
    const tipDist = axD*EARTH.r/Math.max(0.001, SUN.r-EARTH.r);
    const umbHalf = EARTH.r*Math.max(0,1-along/tipDist);
    const penHalf = EARTH.r + Math.max(0,along)*(SUN.r+EARTH.r)/axD;

    const MR = ew*0.32;
    const scale = MR/MOON_R;
    const shOffX = -perp*scale;
    const umbR = umbHalf*scale;
    const penR = penHalf*scale;

    // 달 본체 (개기월식이면 블러드문)
    const blood = (lec==='total');
    const mg = ex.createRadialGradient(cx-MR*0.25, cy-MR*0.25, MR*0.1, cx, cy, MR);
    if(blood){ mg.addColorStop(0,'#dd6633'); mg.addColorStop(.6,'#992211'); mg.addColorStop(1,'#550800'); }
    else     { mg.addColorStop(0,'#f0eddf'); mg.addColorStop(.6,'#c5c1b3'); mg.addColorStop(1,'#807d72'); }
    ex.fillStyle = mg;
    ex.beginPath(); ex.arc(cx, cy, MR, 0, Math.PI*2); ex.fill();

    // 그림자 (달 디스크 안에서만)
    if (!blood) {
      ex.save();
      ex.beginPath(); ex.arc(cx, cy, MR, 0, Math.PI*2); ex.clip();
      if (lec==='penumbral' && penR>0) {
        ex.fillStyle='rgba(40,25,15,0.45)';
        ex.beginPath(); ex.arc(cx+shOffX, cy, penR, 0, Math.PI*2); ex.fill();
      }
      if ((lec==='partial' || lec==='penumbral') && umbR>0) {
        ex.fillStyle='rgba(15,8,4,0.85)';
        ex.beginPath(); ex.arc(cx+shOffX, cy, umbR, 0, Math.PI*2); ex.fill();
      }
      ex.restore();
    }
  }
}

function classifyLunar(moon) {
  const pts=[[moon.x,moon.y]];
  for(let i=0;i<12;i++){const a=i/12*Math.PI*2; pts.push([moon.x+moon.r*.9*Math.cos(a),moon.y+moon.r*.9*Math.sin(a)]);}
  let umb=0,pen=0;
  for(const [px,py] of pts){
    const r=pointInShadow(SUN,EARTH,px,py);
    if(r==='umbra') umb++;
    else if(r==='penumbra') pen++;
  }
  const tot=pts.length;
  if(umb===tot) return 'total';
  if(umb>0)     return 'partial';
  if(pen===tot) return 'penumbral';
  if(pen>0)     return 'penumbral';
  return 'none';
}

function updateStatus(obsRegion, lunarEc) {
  let t,c,d;
  if(mode==='solar'){
    if(obsRegion==='umbra')
      {t='📍 개기일식 관측 중';c='#cc3300';d='관측 위치가 달의 본그림자 안에 있습니다. 달의 시지름이 태양보다 커 태양 전체가 가려집니다. 코로나를 관측할 수 있습니다.';}
    else if(obsRegion==='antumbra')
      {t='📍 금환일식 관측 중';c='#c07000';d='관측 위치가 달 그림자의 연장 영역에 있습니다. 달의 시지름이 태양보다 작아 태양 가장자리가 고리 모양으로 보입니다.';}
    else if(obsRegion==='penumbra')
      {t='📍 부분일식 관측 중';c='#cc6600';d='관측 위치가 달의 반그림자 안에 있어 태양의 일부만 가려져 보입니다.';}
    else
      {t='📍 일식 없음';c='#666';d='관측 위치가 달의 그림자 바깥에 있습니다.';}
  } else {
    if(lunarEc==='total')
      {t='📍 개기월식';c='#cc3300';d='달 전체가 지구의 본그림자 안에 있습니다. 지구 대기를 통과한 붉은빛 때문에 달이 붉게 보입니다.';}
    else if(lunarEc==='partial')
      {t='📍 부분월식';c='#cc6600';d='달의 일부가 지구의 본그림자 안에 들어가 가려져 보입니다.';}
    else if(lunarEc==='penumbral')
      {t='📍 반영식';c='#c07000';d='달 전체가 지구의 반그림자 안에 있습니다. 달의 밝기가 약간 감소하여 보입니다.';}
    else
      {t='📍 월식 없음';c='#666';d='달이 지구 그림자 바깥에 있습니다.';}
  }
  document.getElementById('st-type').textContent=t;
  document.getElementById('st-type').style.color=c;
  document.getElementById('st-desc').textContent=d;
}

function draw() {
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='#f2ede3'; ctx.fillRect(0,0,W,H);

  for(const[sx,sy]of[[50,38],[135,25],[230,50],[380,16],[500,36],[610,20],[720,42],[808,26],[64,70],[180,92],[440,56],[768,76],[320,84],[558,72],[854,54],[405,356],[258,341],[608,336],[758,366],[158,356],[508,374],[682,351]]){
    ctx.fillStyle='rgba(30,30,80,.2)'; ctx.beginPath(); ctx.arc(sx,sy,1.3,0,Math.PI*2); ctx.fill();
  }

  const moon=getMoon();

  if(mode==='solar'){
    const sh=drawShadowCones(SUN, moon);
    drawOrbit();
    drawSun();
    drawEarth();
    drawBodyShadow(EARTH, SUN, moon);
    drawMoon(moon, false);

    lbl('태양', SUN.x,   SUN.y+SUN.r+16);
    lbl('달',   moon.x,  moon.y+moon.r+14);
    lbl('지구', EARTH.x, EARTH.y+EARTH.r+14);
    drawShadowLabels(sh);

    const obs=getObserver();
    const obsReg=pointInShadow(SUN,moon,obs.x,obs.y);
    drawObserver(obsReg);
    updateStatus(obsReg, null);

  } else {
    const sh=drawShadowCones(SUN, EARTH);
    drawOrbit();
    drawSun();
    drawEarth();

    const lec=classifyLunar(moon);
    drawMoon(moon, lec==='total');
    drawBodyShadow(moon, SUN, EARTH);

    lbl('태양', SUN.x,   SUN.y+SUN.r+16);
    lbl('지구', EARTH.x, EARTH.y+EARTH.r+14);
    lbl('달',   moon.x,  moon.y+moon.r+14);
    drawShadowLabels(sh);

    updateStatus(null, lec);
  }

  let deg=Math.round(moonAngle*180/Math.PI)%360;
  if(deg<0) deg+=360;
  document.getElementById('angle-label').textContent='달 위치: '+deg+'°';

  drawEyeView();
}

let dragging=false, dragTarget=null;

function toL(e){
  const r=canvas.getBoundingClientRect(),sx=W/r.width,sy=H/r.height;
  const cx=e.touches?e.touches[0].clientX:e.clientX;
  const cy=e.touches?e.touches[0].clientY:e.clientY;
  return{x:(cx-r.left)*sx,y:(cy-r.top)*sy};
}
function nearMoon(p){const m=getMoon();return Math.hypot(p.x-m.x,p.y-m.y)<m.r+18;}
function nearObs(p){
  if(mode!=='solar')return false;
  const o=getObserver();
  // 핀이 지구 바깥쪽으로 ~22px 솟아 있으므로 그 근처도 잡히도록
  const ux=(o.x-EARTH.x)/EARTH.r, uy=(o.y-EARTH.y)/EARTH.r;
  const headX=o.x+ux*14, headY=o.y+uy*14;
  return Math.hypot(p.x-o.x,p.y-o.y)<14 || Math.hypot(p.x-headX,p.y-headY)<10;
}

function startDrag(p){
  if(nearObs(p)){dragging=true;dragTarget='obs';canvas.classList.add('dragging');}
  else if(nearMoon(p)){dragging=true;dragTarget='moon';canvas.classList.add('dragging');}
}
function moveDrag(p){
  if(!dragging)return;
  if(dragTarget==='obs'){
    let a=Math.atan2(p.y-EARTH.y,p.x-EARTH.x);
    // 태양은 지구 왼쪽 → 관측자는 태양을 볼 수 있는 왼쪽 반구에만
    if(Math.cos(a) > 0) a = a >= 0 ? Math.PI/2 : -Math.PI/2;
    observerAngle=a;
  } else {
    moonAngle=Math.atan2(p.y-EARTH.y, p.x-EARTH.x);
  }
  draw();
}
function endDrag(){dragging=false;dragTarget=null;canvas.classList.remove('dragging');}

canvas.addEventListener('mousedown',e=>startDrag(toL(e)));
canvas.addEventListener('mousemove',e=>moveDrag(toL(e)));
canvas.addEventListener('mouseup',endDrag);
canvas.addEventListener('mouseleave',endDrag);
canvas.addEventListener('touchstart',e=>{e.preventDefault();startDrag(toL(e));},{passive:false});
canvas.addEventListener('touchmove', e=>{e.preventDefault();moveDrag(toL(e));},{passive:false});
canvas.addEventListener('touchend',endDrag);

function toggleAnim(){
  animating=!animating;
  const btn=document.getElementById('btn-play');
  btn.textContent=animating?'⏸ 정지':'▶ 공전 시작';
  btn.classList.toggle('playing',animating);
  if(animating) animate(); else cancelAnimationFrame(animId);
}
function animate(){
  if(!animating)return;
  moonAngle-=animSpeed;
  draw();
  animId=requestAnimationFrame(animate);
}

function onDistChange(v){
  distMul=parseFloat(v);
  const t=distMul<0.65?'매우 가까움':distMul<0.88?'가까움':distMul<1.12?'보통':distMul<1.4?'멀':'매우 멀';
  document.getElementById('dist-val').textContent=t;
  draw();
}

function onSpeedChange(v){
  animSpeed=parseFloat(v);
  const t=animSpeed<0.004?'매우 느림':animSpeed<0.008?'느림':animSpeed<0.014?'보통':animSpeed<0.022?'빠름':'매우 빠름';
  document.getElementById('speed-val').textContent=t;
}

function setMode(m){
  mode=m;
  document.getElementById('tab-solar').classList.toggle('active',m==='solar');
  document.getElementById('tab-lunar').classList.toggle('active',m==='lunar');
  document.getElementById('leg-obs').style.display=m==='solar'?'flex':'none';
  resetMoon();
}

function resetMoon(){
  moonAngle=mode==='solar'?Math.PI:0;
  observerAngle=Math.PI;
  distMul=1.0;
  const ds=document.getElementById('dist-slider');
  if(ds){ ds.value='1.0'; document.getElementById('dist-val').textContent='보통'; }
  draw();
}

setMode('solar');
eyeShimmer();
</script>
</body>
</html>
