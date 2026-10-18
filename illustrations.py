"""
illustrations.py — High-impact, responsive 3D vector illustrations for RainCheck.
Features custom animated graphics for:
1. Hero / General (Iconic Umbrella Boat with floating telemetry badges)
2. Farmer (Crops, agricultural fields, weather radar pill)
3. Rider (Motorcycle courier on route, road conditions, safety badge)
4. Trader (Open-air market stall canopy, inventory protection)

Strictly zero leading line indentation and zero HTML comments to prevent markdown code-block bleeding.
"""
from typing import Dict, Any, Optional

def _clean_html(html: str) -> str:
    """Strip leading spaces from each line so CommonMark never treats HTML as pre/code."""
    return "\n".join(line.strip() for line in html.strip().splitlines() if line.strip())

def get_role_illustration(
    role: str = "Farmer",
    live_weather: Optional[Dict[str, Any]] = None,
    hit_rate_pct: int = 82
) -> str:
    """Return the dedicated 3D illustration based on active persona."""
    if role == "Rider":
        return get_rider_illustration(live_weather, hit_rate_pct)
    elif role == "Trader":
        return get_trader_illustration(live_weather, hit_rate_pct)
    else:
        return get_farmer_illustration(live_weather, hit_rate_pct)

def get_farmer_illustration(live_weather: Optional[Dict[str, Any]] = None, hit_rate_pct: int = 82) -> str:
    if live_weather is None:
        live_weather = {}
    temp = live_weather.get("temperature_c", 28.5)
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

def get_rider_illustration(live_weather: Optional[Dict[str, Any]] = None, hit_rate_pct: int = 82) -> str:
    if live_weather is None:
        live_weather = {}
    temp = live_weather.get("temperature_c", 28.5)
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

def get_trader_illustration(live_weather: Optional[Dict[str, Any]] = None, hit_rate_pct: int = 82) -> str:
    if live_weather is None:
        live_weather = {}
    temp = live_weather.get("temperature_c", 28.5)
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

def get_floodsimple_hero_illustration(live_weather: Optional[Dict[str, Any]] = None, hit_rate_pct: int = 82) -> str:
    """Default umbrella boat illustration."""
    return get_farmer_illustration(live_weather, hit_rate_pct)
