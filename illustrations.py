"""
illustrations.py — High-impact, responsive 3D vector illustrations for RainCheck.
Features custom animated graphics for:
1. Hero / Main Page (Iconic Umbrella Boat with floating telemetry badges)
2. Farmer (Crops, agricultural fields, weather radar pill)
3. Rider (Motorcycle courier on route, road conditions, safety badge)
4. Trader (Open-air market stall canopy, inventory protection)

Strictly zero leading line indentation and zero HTML comments to prevent markdown code-block bleeding.
"""
from typing import Dict, Any, Optional
from translations import get_ui_text

def _clean_html(html: str) -> str:
    """Strip leading spaces from each line so CommonMark never treats HTML as pre/code."""
    return "\n".join(line.strip() for line in html.strip().splitlines() if line.strip())

def get_floodsimple_hero_illustration(live_weather: Optional[Dict[str, Any]] = None, hit_rate_pct: int = 71) -> str:
    """The signature FloodSimple-inspired Umbrella Boat with people, pet dog, and 3D floating cards."""
    if live_weather is None:
        live_weather = {}
    temp = live_weather.get("temperature_c", 28.7)
    city_name = live_weather.get("city", "Kasese, Uganda").split(",")[0].strip()
    condition = live_weather.get("condition", "Overcast")

    html = f"""<style>
@keyframes floatA {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-8px); }} }}
@keyframes floatB {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(8px); }} }}
.gl-badge {{
position: absolute; display: flex; align-items: center; gap: 10px; padding: 10px 18px;
background: rgba(255, 255, 255, 0.96); backdrop-filter: blur(12px);
border: 1px solid rgba(255, 255, 255, 0.98); border-radius: 16px;
box-shadow: 0 16px 32px -8px rgba(2, 132, 199, 0.18), 0 4px 12px rgba(15, 23, 42, 0.06);
z-index: 10; white-space: nowrap;
}}
.gl-badge.b1 {{ top: 22px; left: -14px; animation: floatA 4s ease-in-out infinite; }}
.gl-badge.b2 {{ top: 48px; right: -12px; animation: floatB 4.5s ease-in-out infinite; }}
.gl-badge.b3 {{ bottom: 30px; right: 14px; animation: floatA 5s ease-in-out infinite; }}
</style>
<div style="position: relative; width: 100%; max-width: 520px; margin: 0 auto;">
<div class="gl-badge b1">
<div style="width: 32px; height: 32px; border-radius: 50%; background: #DCFCE7; display: flex; align-items: center; justify-content: center;">
<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
<polyline points="20 6 9 17 4 12"></polyline>
</svg>
</div>
<div>
<div style="font-size: 0.88rem; font-weight: 800; color: #0B132B;">{hit_rate_pct}% Accuracy</div>
<div style="font-size: 0.70rem; color: #64748B; font-weight: 600;">Verified Hit Rate</div>
</div>
</div>
<div class="gl-badge b2">
<div style="width: 32px; height: 32px; border-radius: 50%; background: #E0F2FE; display: flex; align-items: center; justify-content: center;">
<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
<circle cx="12" cy="12" r="5"></circle>
<line x1="12" y1="1" x2="12" y2="3"></line>
<line x1="12" y1="21" x2="12" y2="23"></line>
<line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
<line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
</svg>
</div>
<div>
<div style="font-size: 0.88rem; font-weight: 800; color: #0B132B;">{city_name} &bull; {temp}°C</div>
<div style="font-size: 0.70rem; color: #64748B; font-weight: 600;">{condition}</div>
</div>
</div>
<div class="gl-badge b3">
<div style="width: 32px; height: 32px; border-radius: 50%; background: #FEF3C7; display: flex; align-items: center; justify-content: center;">
<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
</svg>
</div>
<div>
<div style="font-size: 0.88rem; font-weight: 800; color: #0B132B;">Safe AI Guard</div>
<div style="font-size: 0.70rem; color: #64748B; font-weight: 600;">Zero Hallucinations</div>
</div>
</div>
<svg viewBox="0 0 540 420" width="100%" height="auto" style="overflow: visible; display: block;">
<defs>
<linearGradient id="skyGl" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stop-color="#F0F9FF" stop-opacity="0.9"/>
<stop offset="100%" stop-color="#E0F2FE" stop-opacity="0.3"/>
</linearGradient>
<linearGradient id="umbGrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#0284C7"/>
<stop offset="100%" stop-color="#0369A1"/>
</linearGradient>
<linearGradient id="waveFr" x1="0%" y1="0%" x2="100%" y2="0%">
<stop offset="0%" stop-color="#BAE6FD" stop-opacity="0.75"/>
<stop offset="50%" stop-color="#7DD3FC" stop-opacity="0.9"/>
<stop offset="100%" stop-color="#BAE6FD" stop-opacity="0.75"/>
</linearGradient>
<filter id="shadow3d" x="-15%" y="-15%" width="130%" height="140%">
<feDropShadow dx="0" dy="16" stdDeviation="14" flood-color="#0369A1" flood-opacity="0.2"/>
</filter>
</defs>
<ellipse cx="270" cy="220" rx="230" ry="170" fill="url(#skyGl)"/>
<circle cx="430" cy="85" r="38" fill="#FEF3C7" opacity="0.85"/>
<circle cx="430" cy="85" r="26" fill="#F59E0B"/>
<path d="M 90 110 Q 110 90 135 105 Q 160 85 185 105 Q 210 115 195 135 L 85 135 Q 70 120 90 110 Z" fill="#FFFFFF" opacity="0.95"/>
<path d="M 330 140 Q 345 125 365 135 Q 385 120 405 135 Q 420 145 410 160 L 325 160 Q 315 145 330 140 Z" fill="#FFFFFF" opacity="0.85"/>
<path d="M 20 320 Q 140 300 270 320 T 520 320 L 520 390 L 20 390 Z" fill="#E0F2FE" opacity="0.75"/>
<g filter="url(#shadow3d)">
<path d="M 270 260 L 270 125 C 270 95 245 95 245 115" fill="none" stroke="#0F172A" stroke-width="7" stroke-linecap="round"/>
<circle cx="230" cy="190" r="15" fill="#0B132B"/>
<path d="M 205 245 C 205 210 255 210 255 245 Z" fill="#0B132B"/>
<path d="M 208 215 Q 190 200 185 185" fill="none" stroke="#0B132B" stroke-width="5" stroke-linecap="round"/>
<circle cx="295" cy="180" r="16" fill="#0284C7"/>
<path d="M 270 245 C 270 205 320 205 320 245 Z" fill="#0284C7"/>
<ellipse cx="355" cy="225" rx="15" ry="12" fill="#64748B"/>
<circle cx="365" cy="214" r="9" fill="#64748B"/>
<polygon points="360,207 364,213 358,213" fill="#475569"/>
<polygon points="370,214 376,216 370,219" fill="#475569"/>
<path d="M 70 245 Q 270 375 470 245 Q 420 265 370 245 Q 320 265 270 245 Q 220 265 170 245 Q 120 265 70 245 Z" fill="url(#umbGrad)"/>
<path d="M 70 245 Q 170 345 170 245 Q 120 265 70 245 Z" fill="#0284C7"/>
<path d="M 170 245 Q 220 365 270 245 Q 220 265 170 245 Z" fill="#F8FAFC"/>
<path d="M 270 245 Q 320 365 370 245 Q 320 265 270 245 Z" fill="#0B132B"/>
<path d="M 370 245 Q 420 345 470 245 Q 420 265 370 245 Z" fill="#0369A1"/>
<circle cx="70" cy="245" r="4" fill="#0F172A"/>
<circle cx="170" cy="245" r="4" fill="#0F172A"/>
<circle cx="270" cy="245" r="4" fill="#0F172A"/>
<circle cx="370" cy="245" r="4" fill="#0F172A"/>
<circle cx="470" cy="245" r="4" fill="#0F172A"/>
</g>
<path d="M 0 335 Q 130 315 270 335 T 540 335 L 540 420 L 0 420 Z" fill="url(#waveFr)"/>
<path d="M 0 355 Q 140 340 280 355 T 540 355 L 540 420 L 0 420 Z" fill="#38BDF8" opacity="0.3"/>
<ellipse cx="140" cy="350" rx="24" ry="4" fill="#BAE6FD" opacity="0.6"/>
<ellipse cx="380" cy="365" rx="30" ry="5" fill="#BAE6FD" opacity="0.6"/>
</svg>
</div>"""
    return _clean_html(html)

def get_role_illustration(
    role: str = "Farmer",
    live_weather: Optional[Dict[str, Any]] = None,
    hit_rate_pct: int = 71
) -> str:
    """Return dedicated persona graphic."""
    if role == "Rider":
        return get_rider_illustration(live_weather, hit_rate_pct)
    elif role == "Trader":
        return get_trader_illustration(live_weather, hit_rate_pct)
    else:
        return get_farmer_illustration(live_weather, hit_rate_pct)

def get_farmer_illustration(live_weather: Optional[Dict[str, Any]] = None, hit_rate_pct: int = 71) -> str:
    if live_weather is None:
        live_weather = {}
    temp = live_weather.get("temperature_c", 28.7)
    city_name = live_weather.get("city", "Kasese, Uganda").split(",")[0].strip()
    rain_prob = live_weather.get("rain_prob_24h", 34)

    html = f"""<style>
@keyframes floatA {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-8px); }} }}
@keyframes floatB {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(8px); }} }}
.gl-badge {{
position: absolute; display: flex; align-items: center; gap: 8px; padding: 8px 14px;
background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px);
border: 1px solid rgba(226, 232, 240, 0.9); border-radius: 14px;
box-shadow: 0 12px 24px -6px rgba(2, 132, 199, 0.18); z-index: 10;
}}
.gl-badge.b1 {{ top: 15px; left: -10px; animation: floatA 4s ease-in-out infinite; }}
.gl-badge.b2 {{ top: 40px; right: -8px; animation: floatB 4.5s ease-in-out infinite; }}
.gl-badge.b3 {{ bottom: 25px; right: 10px; animation: floatA 5s ease-in-out infinite; }}
</style>
<div style="position: relative; width: 100%; max-width: 500px; margin: 0 auto;">
<div class="gl-badge b1">
<div style="width: 28px; height: 28px; border-radius: 50%; background: #DCFCE7; display: flex; align-items: center; justify-content: center;">
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
</div>
<div>
<div style="font-size: 0.82rem; font-weight: 800; color: #0B132B;">{hit_rate_pct}% Accuracy</div>
<div style="font-size: 0.68rem; color: #64748B; font-weight: 600;">Crop Calendar Verified</div>
</div>
</div>
<div class="gl-badge b2">
<div style="width: 28px; height: 28px; border-radius: 50%; background: #E0F2FE; display: flex; align-items: center; justify-content: center;">
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2.5"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line></svg>
</div>
<div>
<div style="font-size: 0.82rem; font-weight: 800; color: #0B132B;">{city_name} &bull; {temp}°C</div>
<div style="font-size: 0.68rem; color: #64748B; font-weight: 600;">Rain Chance: {rain_prob}%</div>
</div>
</div>
<div class="gl-badge b3">
<div style="width: 28px; height: 28px; border-radius: 50%; background: #FEF3C7; display: flex; align-items: center; justify-content: center;">
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
</div>
<div>
<div style="font-size: 0.82rem; font-weight: 800; color: #0B132B;">Soil Protocol</div>
<div style="font-size: 0.68rem; color: #64748B; font-weight: 600;">Optimal Agrochemicals</div>
</div>
</div>
<svg viewBox="0 0 520 380" width="100%" height="auto" style="overflow: visible; display: block;">
<defs>
<linearGradient id="farmSky" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stop-color="#E0F2FE"/>
<stop offset="100%" stop-color="#F0FDF4"/>
</linearGradient>
<linearGradient id="hillGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#86EFAC"/>
<stop offset="100%" stop-color="#22C55E"/>
</linearGradient>
<linearGradient id="hillGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#4ADE80"/>
<stop offset="100%" stop-color="#15803D"/>
</linearGradient>
<linearGradient id="soilRows" x1="0%" y1="0%" x2="100%" y2="0%">
<stop offset="0%" stop-color="#CA8A04"/>
<stop offset="50%" stop-color="#EAB308"/>
<stop offset="100%" stop-color="#A16207"/>
</linearGradient>
<filter id="farmShadow" x="-10%" y="-10%" width="125%" height="125%">
<feDropShadow dx="0" dy="12" stdDeviation="12" flood-color="#16A34A" flood-opacity="0.16"/>
</filter>
</defs>
<rect x="0" y="0" width="520" height="380" rx="24" fill="url(#farmSky)"/>
<circle cx="420" cy="80" r="34" fill="#FEF3C7"/>
<circle cx="420" cy="80" r="24" fill="#F59E0B"/>
<path d="M 70 95 Q 90 75 115 90 Q 140 70 165 90 Q 185 100 175 120 L 65 120 Z" fill="#FFFFFF" opacity="0.9"/>
<path d="M 0 240 Q 140 180 320 230 Q 440 265 520 220 L 520 380 L 0 380 Z" fill="url(#hillGrad1)"/>
<path d="M 0 270 Q 180 220 360 260 Q 460 280 520 250 L 520 380 L 0 380 Z" fill="url(#hillGrad2)"/>
<g filter="url(#farmShadow)">
<path d="M 40 330 Q 180 300 320 330 T 520 330 L 520 380 L 0 380 Z" fill="url(#soilRows)"/>
<path d="M 60 340 L 480 340" stroke="#713F12" stroke-width="4" stroke-dasharray="14 10"/>
<path d="M 50 355 L 490 355" stroke="#713F12" stroke-width="4" stroke-dasharray="18 10"/>
<g fill="#166534">
<path d="M 90 325 C 85 305 105 305 100 325 Z"/>
<path d="M 140 322 C 135 302 155 302 150 322 Z"/>
<path d="M 190 324 C 185 304 205 304 200 324 Z"/>
<path d="M 240 323 C 235 303 255 303 250 323 Z"/>
<path d="M 290 325 C 285 305 305 305 300 325 Z"/>
</g>
<circle cx="360" cy="220" r="16" fill="#0B132B"/>
<ellipse cx="360" cy="210" rx="22" ry="6" fill="#D97706"/>
<path d="M 345 280 C 345 240 375 240 375 280 Z" fill="#0284C7"/>
<path d="M 370 250 L 395 240" stroke="#0284C7" stroke-width="5" stroke-linecap="round"/>
<path d="M 395 235 L 395 285" stroke="#78350F" stroke-width="4" stroke-linecap="round"/>
<polygon points="385,285 405,285 395,300" fill="#64748B"/>
<path d="M 340 270 Q 330 250 310 250" fill="none" stroke="#0284C7" stroke-width="4" stroke-linecap="round"/>
<rect x="290" y="245" width="22" height="20" rx="4" fill="#B45309"/>
</g>
</svg>
</div>"""
    return _clean_html(html)

def get_rider_illustration(live_weather: Optional[Dict[str, Any]] = None, hit_rate_pct: int = 71) -> str:
    if live_weather is None:
        live_weather = {}
    temp = live_weather.get("temperature_c", 28.7)
    wind = live_weather.get("wind_speed_kmh", 5.1)

    html = f"""<style>
@keyframes floatA {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-8px); }} }}
@keyframes floatB {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(8px); }} }}
.gl-badge {{
position: absolute; display: flex; align-items: center; gap: 8px; padding: 8px 14px;
background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px);
border: 1px solid rgba(226, 232, 240, 0.9); border-radius: 14px;
box-shadow: 0 12px 24px -6px rgba(2, 132, 199, 0.18); z-index: 10;
}}
.gl-badge.b1 {{ top: 15px; left: -10px; animation: floatA 4s ease-in-out infinite; }}
.gl-badge.b2 {{ top: 40px; right: -8px; animation: floatB 4.5s ease-in-out infinite; }}
.gl-badge.b3 {{ bottom: 25px; right: 10px; animation: floatA 5s ease-in-out infinite; }}
</style>
<div style="position: relative; width: 100%; max-width: 500px; margin: 0 auto;">
<div class="gl-badge b1">
<div style="width: 28px; height: 28px; border-radius: 50%; background: #E0F2FE; display: flex; align-items: center; justify-content: center;">
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2.5"><polygon points="3 11 22 2 13 21 11 13 3 11"></polygon></svg>
</div>
<div>
<div style="font-size: 0.82rem; font-weight: 800; color: #0B132B;">Boda Route Active</div>
<div style="font-size: 0.68rem; color: #64748B; font-weight: 600;">Road Visibility: High</div>
</div>
</div>
<div class="gl-badge b2">
<div style="width: 28px; height: 28px; border-radius: 50%; background: #DCFCE7; display: flex; align-items: center; justify-content: center;">
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
</div>
<div>
<div style="font-size: 0.82rem; font-weight: 800; color: #0B132B;">Wind: {wind} km/h</div>
<div style="font-size: 0.68rem; color: #64748B; font-weight: 600;">Calm Highway Conditions</div>
</div>
</div>
<div class="gl-badge b3">
<div style="width: 28px; height: 28px; border-radius: 50%; background: #FEF3C7; display: flex; align-items: center; justify-content: center;">
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
</div>
<div>
<div style="font-size: 0.82rem; font-weight: 800; color: #0B132B;">6h Lead Horizon</div>
<div style="font-size: 0.68rem; color: #64748B; font-weight: 600;">Keep Rain Gear on Standby</div>
</div>
</div>
<svg viewBox="0 0 520 380" width="100%" height="auto" style="overflow: visible; display: block;">
<defs>
<linearGradient id="riderSky" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stop-color="#E0F2FE"/>
<stop offset="100%" stop-color="#F8FAFC"/>
</linearGradient>
<linearGradient id="roadGrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#334155"/>
<stop offset="100%" stop-color="#1E293B"/>
</linearGradient>
<filter id="riderShadow" x="-10%" y="-10%" width="125%" height="125%">
<feDropShadow dx="0" dy="14" stdDeviation="12" flood-color="#0284C7" flood-opacity="0.2"/>
</filter>
</defs>
<rect x="0" y="0" width="520" height="380" rx="24" fill="url(#riderSky)"/>
<circle cx="390" cy="75" r="32" fill="#FEF3C7"/>
<circle cx="390" cy="75" r="22" fill="#F59E0B"/>
<path d="M 0 250 L 520 220 L 520 380 L 0 380 Z" fill="#64748B" opacity="0.3"/>
<path d="M 60 380 L 220 220 L 300 220 L 460 380 Z" fill="url(#roadGrad)"/>
<path d="M 260 220 L 260 380" stroke="#F8FAFC" stroke-width="5" stroke-dasharray="24 16"/>
<g filter="url(#riderShadow)">
<circle cx="210" cy="330" r="26" fill="#0F172A"/>
<circle cx="210" cy="330" r="14" fill="#94A3B8"/>
<circle cx="310" cy="330" r="26" fill="#0F172A"/>
<circle cx="310" cy="330" r="14" fill="#94A3B8"/>
<path d="M 210 330 L 245 285 L 290 285 L 310 330 Z" fill="#0284C7"/>
<path d="M 245 285 L 235 255 L 260 255" stroke="#0F172A" stroke-width="6" stroke-linecap="round"/>
<rect x="180" y="270" width="28" height="24" rx="4" fill="#D97706"/>
<circle cx="260" cy="205" r="16" fill="#0284C7"/>
<circle cx="264" cy="206" r="6" fill="#0F172A"/>
<path d="M 245 270 C 245 225 275 225 275 270 Z" fill="#0B132B"/>
<path d="M 260 240 L 285 240" stroke="#F8FAFC" stroke-width="3"/>
<path d="M 255 235 L 240 255" stroke="#0B132B" stroke-width="5" stroke-linecap="round"/>
</g>
</svg>
</div>"""
    return _clean_html(html)

def get_trader_illustration(live_weather: Optional[Dict[str, Any]] = None, hit_rate_pct: int = 71) -> str:
    if live_weather is None:
        live_weather = {}
    temp = live_weather.get("temperature_c", 28.7)
    condition = live_weather.get("condition", "Overcast")

    html = f"""<style>
@keyframes floatA {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-8px); }} }}
@keyframes floatB {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(8px); }} }}
.gl-badge {{
position: absolute; display: flex; align-items: center; gap: 8px; padding: 8px 14px;
background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px);
border: 1px solid rgba(226, 232, 240, 0.9); border-radius: 14px;
box-shadow: 0 12px 24px -6px rgba(2, 132, 199, 0.18); z-index: 10;
}}
.gl-badge.b1 {{ top: 15px; left: -10px; animation: floatA 4s ease-in-out infinite; }}
.gl-badge.b2 {{ top: 40px; right: -8px; animation: floatB 4.5s ease-in-out infinite; }}
.gl-badge.b3 {{ bottom: 25px; right: 10px; animation: floatA 5s ease-in-out infinite; }}
</style>
<div style="position: relative; width: 100%; max-width: 500px; margin: 0 auto;">
<div class="gl-badge b1">
<div style="width: 28px; height: 28px; border-radius: 50%; background: #FEF3C7; display: flex; align-items: center; justify-content: center;">
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#D97706" stroke-width="2.5"><path d="m2 7 4.41-4.41A2 2 0 0 1 7.83 2h8.34a2 2 0 0 1 1.42.59L22 7"></path><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"></path></svg>
</div>
<div>
<div style="font-size: 0.82rem; font-weight: 800; color: #0B132B;">Market Stall Safe</div>
<div style="font-size: 0.68rem; color: #64748B; font-weight: 600;">Coverings Ready</div>
</div>
</div>
<div class="gl-badge b2">
<div style="width: 28px; height: 28px; border-radius: 50%; background: #DCFCE7; display: flex; align-items: center; justify-content: center;">
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#16A34A" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
</div>
<div>
<div style="font-size: 0.82rem; font-weight: 800; color: #0B132B;">{condition} &bull; {temp}°C</div>
<div style="font-size: 0.68rem; color: #64748B; font-weight: 600;">Open-Air Trading</div>
</div>
</div>
<div class="gl-badge b3">
<div style="width: 28px; height: 28px; border-radius: 50%; background: #E0F2FE; display: flex; align-items: center; justify-content: center;">
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
</div>
<div>
<div style="font-size: 0.82rem; font-weight: 800; color: #0B132B;">Zero Inventory Damage</div>
<div style="font-size: 0.68rem; color: #64748B; font-weight: 600;">Elevated Crate Protocol</div>
</div>
</div>
<svg viewBox="0 0 520 380" width="100%" height="auto" style="overflow: visible; display: block;">
<defs>
<linearGradient id="marketSky" x1="0%" y1="0%" x2="0%" y2="100%">
<stop offset="0%" stop-color="#E0F2FE"/>
<stop offset="100%" stop-color="#FEF3C7"/>
</linearGradient>
<linearGradient id="canopyBlue" x1="0%" y1="0%" x2="100%" y2="0%">
<stop offset="0%" stop-color="#0284C7"/>
<stop offset="50%" stop-color="#0369A1"/>
<stop offset="100%" stop-color="#0284C7"/>
</linearGradient>
<filter id="traderShadow" x="-10%" y="-10%" width="125%" height="125%">
<feDropShadow dx="0" dy="14" stdDeviation="12" flood-color="#D97706" flood-opacity="0.18"/>
</filter>
</defs>
<rect x="0" y="0" width="520" height="380" rx="24" fill="url(#marketSky)"/>
<circle cx="410" cy="70" r="30" fill="#FEF3C7"/>
<circle cx="410" cy="70" r="20" fill="#F59E0B"/>
<rect x="0" y="270" width="520" height="110" fill="#F1F5F9"/>
<g filter="url(#traderShadow)">
<rect x="120" y="250" width="280" height="50" rx="6" fill="#B45309"/>
<path d="M 100 170 L 420 170 L 400 215 L 120 215 Z" fill="url(#canopyBlue)"/>
<path d="M 100 170 L 140 170 L 140 215 L 120 215 Z" fill="#F8FAFC"/>
<path d="M 180 170 L 220 170 L 220 215 L 200 215 Z" fill="#F8FAFC"/>
<path d="M 260 170 L 300 170 L 300 215 L 280 215 Z" fill="#F8FAFC"/>
<path d="M 340 170 L 380 170 L 380 215 L 360 215 Z" fill="#F8FAFC"/>
<line x1="125" y1="215" x2="125" y2="300" stroke="#78350F" stroke-width="6"/>
<line x1="395" y1="215" x2="395" y2="300" stroke="#78350F" stroke-width="6"/>
<rect x="140" y="240" width="45" height="20" rx="3" fill="#CA8A04"/>
<circle cx="152" cy="245" r="5" fill="#EF4444"/>
<circle cx="165" cy="245" r="5" fill="#22C55E"/>
<circle cx="175" cy="245" r="5" fill="#F59E0B"/>
<rect x="195" y="240" width="45" height="20" rx="3" fill="#A16207"/>
<rect x="250" y="240" width="45" height="20" rx="3" fill="#CA8A04"/>
<circle cx="340" cy="190" r="15" fill="#0B132B"/>
<path d="M 325 245 C 325 210 355 210 355 245 Z" fill="#10B981"/>
<path d="M 320 225 L 300 240" stroke="#10B981" stroke-width="4" stroke-linecap="round"/>
</g>
</svg>
</div>"""
    return _clean_html(html)


def get_3d_product_cards_html(
    lang: str = "en",
    active_role: str = "Overview",
    hit_rate_pct: int = 71
) -> str:
    """
    Renders 3 animated role cards for RainCheck:
    - Farmer: crop/leaf SVG, verified hit rate metric
    - Rider: motorcycle SVG, 6h lead horizon metric
    - Trader: market stall SVG, dry window metric
    Card style: floating pop-out icon, big metric, orange pill button, hover lift.
    No shoes. No product badge. Pure RainCheck weather app content.
    """
    farmer_name = get_ui_text("role_farmer", lang)
    farmer_desc = get_ui_text("card_farmers_desc", lang)
    farmer_metric_lbl = get_ui_text("card_farmer_metric", lang)

    rider_name = get_ui_text("role_rider", lang)
    rider_desc = get_ui_text("card_riders_desc", lang)
    rider_metric_lbl = get_ui_text("card_rider_metric", lang)

    trader_name = get_ui_text("role_trader", lang)
    trader_desc = get_ui_text("card_traders_desc", lang)
    trader_metric_lbl = get_ui_text("card_trader_metric", lang)

    btn_text = get_ui_text("card_btn_text", lang)

    farmer_active = " active" if active_role == "Farmer" else ""
    rider_active  = " active" if active_role == "Rider"  else ""
    trader_active = " active" if active_role == "Trader" else ""

    # ── Farmer icon: wheat sheaf / crop leaf SVG ──────────────────────────────
    farmer_svg = """<svg viewBox="0 0 120 120" width="96" height="96" style="overflow:visible;">
<defs>
<filter id="rcFShd" x="-30%" y="-30%" width="170%" height="170%">
<feDropShadow dx="0" dy="10" stdDeviation="8" flood-color="#10B981" flood-opacity="0.28"/>
</filter>
<linearGradient id="rcFGrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#DCFCE7"/>
<stop offset="100%" stop-color="#BBF7D0"/>
</linearGradient>
</defs>
<g filter="url(#rcFShd)">
<circle cx="60" cy="60" r="44" fill="url(#rcFGrad)"/>
<path d="M 60 82 L 60 38" stroke="#16A34A" stroke-width="3.5" stroke-linecap="round"/>
<path d="M 60 52 Q 44 42 40 28 Q 52 30 60 44 Q 68 30 80 28 Q 76 42 60 52 Z" fill="#22C55E"/>
<path d="M 60 64 Q 50 56 44 46 Q 54 46 60 58 Q 66 46 76 46 Q 70 56 60 64 Z" fill="#16A34A" opacity="0.7"/>
<ellipse cx="60" cy="84" rx="10" ry="4" fill="#15803D" opacity="0.3"/>
</g>
</svg>"""

    # ── Rider icon: motorcycle SVG ────────────────────────────────────────────
    rider_svg = """<svg viewBox="0 0 120 120" width="96" height="96" style="overflow:visible;">
<defs>
<filter id="rcRShd" x="-30%" y="-30%" width="170%" height="170%">
<feDropShadow dx="0" dy="10" stdDeviation="8" flood-color="#0284C7" flood-opacity="0.28"/>
</filter>
<linearGradient id="rcRGrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#DBEAFE"/>
<stop offset="100%" stop-color="#BAE6FD"/>
</linearGradient>
</defs>
<g filter="url(#rcRShd)">
<circle cx="60" cy="60" r="44" fill="url(#rcRGrad)"/>
<circle cx="36" cy="74" r="11" fill="none" stroke="#0369A1" stroke-width="4"/>
<circle cx="84" cy="74" r="11" fill="none" stroke="#0369A1" stroke-width="4"/>
<circle cx="36" cy="74" r="4" fill="#0284C7"/>
<circle cx="84" cy="74" r="4" fill="#0284C7"/>
<path d="M 36 74 L 50 58 L 62 58 L 70 48 L 84 52 L 84 74" fill="none" stroke="#0284C7" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M 62 58 L 65 50 L 74 50" fill="none" stroke="#0369A1" stroke-width="3" stroke-linecap="round"/>
<ellipse cx="60" cy="85" rx="12" ry="4" fill="#0369A1" opacity="0.18"/>
</g>
</svg>"""

    # ── Trader icon: market stall / canopy SVG ────────────────────────────────
    trader_svg = """<svg viewBox="0 0 120 120" width="96" height="96" style="overflow:visible;">
<defs>
<filter id="rcTShd" x="-30%" y="-30%" width="170%" height="170%">
<feDropShadow dx="0" dy="10" stdDeviation="8" flood-color="#D97706" flood-opacity="0.28"/>
</filter>
<linearGradient id="rcTGrad" x1="0%" y1="0%" x2="100%" y2="100%">
<stop offset="0%" stop-color="#FEF3C7"/>
<stop offset="100%" stop-color="#FDE68A"/>
</linearGradient>
<linearGradient id="rcCanopy" x1="0%" y1="0%" x2="100%" y2="0%">
<stop offset="0%" stop-color="#0284C7"/>
<stop offset="50%" stop-color="#0369A1"/>
<stop offset="100%" stop-color="#0284C7"/>
</linearGradient>
</defs>
<g filter="url(#rcTShd)">
<circle cx="60" cy="60" r="44" fill="url(#rcTGrad)"/>
<path d="M 28 58 L 92 58 L 86 72 L 34 72 Z" fill="url(#rcCanopy)"/>
<path d="M 28 58 L 40 58 L 40 72 L 34 72 Z" fill="#FFFFFF" opacity="0.35"/>
<path d="M 56 58 L 64 58 L 64 72 L 56 72 Z" fill="#FFFFFF" opacity="0.35"/>
<line x1="38" y1="72" x2="38" y2="88" stroke="#92400E" stroke-width="4" stroke-linecap="round"/>
<line x1="82" y1="72" x2="82" y2="88" stroke="#92400E" stroke-width="4" stroke-linecap="round"/>
<rect x="40" y="78" width="40" height="10" rx="3" fill="#B45309"/>
<rect x="43" y="80" width="10" height="6" rx="2" fill="#FCD34D"/>
<rect x="56" y="80" width="10" height="6" rx="2" fill="#FCD34D"/>
<ellipse cx="60" cy="90" rx="14" ry="4" fill="#92400E" opacity="0.18"/>
</g>
</svg>"""

    html = f"""<style>
@keyframes rcFloatA {{ 0%, 100% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-10px); }} }}
@keyframes rcFloatB {{ 0%, 100% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-8px); }} }}
@keyframes rcFloatC {{ 0%, 100% {{ transform: translateY(0px); }} 50% {{ transform: translateY(-12px); }} }}

.rc-cards-wrap {{
display: grid;
grid-template-columns: repeat(3, 1fr);
gap: 28px;
margin-top: 32px;
margin-bottom: 8px;
}}

@media (max-width: 820px) {{
.rc-cards-wrap {{ grid-template-columns: 1fr; gap: 80px; }}
}}

.rc-role-card {{
background: #FFFFFF;
border: 1.5px solid #E2E8F0;
border-radius: 22px;
padding: 64px 22px 28px;
text-align: center;
position: relative;
box-shadow: 0 12px 32px -8px rgba(15,23,42,0.07), 0 2px 6px rgba(15,23,42,0.04);
transition: transform 0.32s cubic-bezier(0.16,1,0.3,1), box-shadow 0.32s cubic-bezier(0.16,1,0.3,1);
display: flex;
flex-direction: column;
justify-content: space-between;
}}

.rc-role-card:hover {{
transform: translateY(-16px);
box-shadow: 0 32px 52px -12px rgba(234,88,12,0.28), 0 8px 18px rgba(15,23,42,0.07);
}}

.rc-role-card.active {{
border: 2px solid #0284C7;
box-shadow: 0 20px 40px -8px rgba(2,132,199,0.25);
}}

.rc-icon-float {{
position: absolute;
top: -48px;
left: 50%;
transform: translateX(-50%);
width: 96px;
height: 96px;
z-index: 5;
transition: transform 0.32s ease;
}}

.rc-role-card:hover .rc-icon-float {{
transform: translateX(-50%) translateY(-6px) scale(1.08);
}}

.rc-card-name {{
font-size: 1.22rem;
font-weight: 800;
color: #0B132B;
margin-bottom: 10px;
letter-spacing: -0.3px;
}}

.rc-card-desc {{
font-size: 0.84rem;
color: #64748B;
line-height: 1.58;
margin-bottom: 20px;
min-height: 58px;
}}

.rc-card-metric {{
font-size: 2.8rem;
font-weight: 900;
color: #0B132B;
line-height: 1;
letter-spacing: -1px;
margin-bottom: 4px;
}}

.rc-card-metric-lbl {{
font-size: 0.72rem;
font-weight: 700;
color: #94A3B8;
text-transform: uppercase;
letter-spacing: 0.7px;
display: block;
margin-bottom: 20px;
}}

.rc-orange-pill {{
display: block;
width: 100%;
padding: 13px 20px;
background: linear-gradient(135deg, #F97316 0%, #EA580C 100%);
color: #FFFFFF !important;
font-weight: 800;
font-size: 0.94rem;
border-radius: 9999px;
box-shadow: 0 8px 20px -4px rgba(234,88,12,0.38);
transition: all 0.22s ease;
border: none;
cursor: pointer;
text-decoration: none !important;
}}

.rc-role-card:hover .rc-orange-pill {{
background: linear-gradient(135deg, #FB923C 0%, #C2410C 100%);
box-shadow: 0 12px 26px -4px rgba(234,88,12,0.55);
transform: translateY(-2px);
}}
</style>

<div class="rc-cards-wrap">

<div class="rc-role-card{farmer_active}">
<div class="rc-icon-float" style="animation: rcFloatA 4s ease-in-out infinite;">
{farmer_svg}
</div>
<div>
<div class="rc-card-name">{farmer_name}</div>
<div class="rc-card-desc">{farmer_desc}</div>
<div class="rc-card-metric">{hit_rate_pct}%</div>
<span class="rc-card-metric-lbl">{farmer_metric_lbl}</span>
</div>
<div class="rc-orange-pill">{btn_text}</div>
</div>

<div class="rc-role-card{rider_active}">
<div class="rc-icon-float" style="animation: rcFloatB 4.5s ease-in-out infinite;">
{rider_svg}
</div>
<div>
<div class="rc-card-name">{rider_name}</div>
<div class="rc-card-desc">{rider_desc}</div>
<div class="rc-card-metric">&ge; 6h</div>
<span class="rc-card-metric-lbl">{rider_metric_lbl}</span>
</div>
<div class="rc-orange-pill">{btn_text}</div>
</div>

<div class="rc-role-card{trader_active}">
<div class="rc-icon-float" style="animation: rcFloatC 4.2s ease-in-out infinite;">
{trader_svg}
</div>
<div>
<div class="rc-card-name">{trader_name}</div>
<div class="rc-card-desc">{trader_desc}</div>
<div class="rc-card-metric">0 mm</div>
<span class="rc-card-metric-lbl">{trader_metric_lbl}</span>
</div>
<div class="rc-orange-pill">{btn_text}</div>
</div>

</div>"""
    return _clean_html(html)

