"""
illustrations.py - FloodSimple-inspired Humanized 3D Illustrations for RainCheck.

Provides handcrafted, responsive SVG graphics depicting the iconic umbrella boat
floating safely on gentle water waves with humanized characters and 3D floating telemetry cards.
Zero external image dependencies, zero emojis.
"""

from typing import Dict, Any, Optional


def get_floodsimple_hero_illustration(
    live_weather: Optional[Dict[str, Any]] = None,
    hit_rate_pct: int = 82
) -> str:
    """
    Generate the FloodSimple-inspired hero graphic:
    - Soft atmospheric background aura with golden sun and gentle clouds
    - Stylized upside-down umbrella boat floating safely on water waves
    - Happy silhouettes of people and their friendly pet dog inside the umbrella
    - 3D Floating Glassmorphic Telemetry Cards layered with drop-shadows:
        * 82% Verified Accuracy (green checkmark)
        * Live City Temp & Condition
        * Zero Hallucinations AI Shield
    """
    if live_weather is None:
        live_weather = {}

    temp = live_weather.get("temperature_c", 24.0)
    city_name = live_weather.get("city", "Kampala, Uganda").split(",")[0].strip()
    condition = live_weather.get("condition", "Clear Sky")

    svg = f"""
    <div class="hero-illustration-container">
        <!-- 3D Floating Glass Card: Verified Hit Rate -->
        <div class="glass-float-card float-card-1">
            <div class="glass-icon-circle green">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
            </div>
            <div>
                <div class="glass-card-title">{hit_rate_pct}% Accuracy</div>
                <div class="glass-card-sub">Verified Model Hit Rate</div>
            </div>
        </div>

        <!-- 3D Floating Glass Card: Live Weather -->
        <div class="glass-float-card float-card-2">
            <div class="glass-icon-circle blue">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#0284C7" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="5"></circle>
                    <line x1="12" y1="1" x2="12" y2="3"></line>
                    <line x1="12" y1="21" x2="12" y2="23"></line>
                    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
                    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
                </svg>
            </div>
            <div>
                <div class="glass-card-title">{city_name} &bull; {temp}°C</div>
                <div class="glass-card-sub">{condition}</div>
            </div>
        </div>

        <!-- 3D Floating Glass Card: AI Safety -->
        <div class="glass-float-card float-card-3">
            <div class="glass-icon-circle amber">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#F59E0B" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                </svg>
            </div>
            <div>
                <div class="glass-card-title">Safe AI Guard</div>
                <div class="glass-card-sub">0% Hallucinations</div>
            </div>
        </div>

        <!-- The Humanized Umbrella Boat SVG Illustration -->
        <svg viewBox="0 0 540 420" width="100%" height="auto" class="illustration-svg" style="overflow: visible;">
            <defs>
                <linearGradient id="skyGlow" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stop-color="#F0F9FF" stop-opacity="0.8"/>
                    <stop offset="100%" stop-color="#E0F2FE" stop-opacity="0.2"/>
                </linearGradient>
                <linearGradient id="umbrellaBlue" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#0284C7"/>
                    <stop offset="100%" stop-color="#0369A1"/>
                </linearGradient>
                <linearGradient id="waveFront" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#BAE6FD" stop-opacity="0.7"/>
                    <stop offset="50%" stop-color="#7DD3FC" stop-opacity="0.8"/>
                    <stop offset="100%" stop-color="#BAE6FD" stop-opacity="0.7"/>
                </linearGradient>
                <filter id="boat3dShadow" x="-15%" y="-15%" width="130%" height="140%">
                    <feDropShadow dx="0" dy="16" stdDeviation="14" flood-color="#0369A1" flood-opacity="0.18"/>
                </filter>
            </defs>

            <!-- Background Atmosphere -->
            <ellipse cx="270" cy="220" rx="230" ry="170" fill="url(#skyGlow)"/>

            <!-- Golden Sun -->
            <circle cx="430" cy="85" r="38" fill="#FEF3C7" opacity="0.85"/>
            <circle cx="430" cy="85" r="26" fill="#F59E0B"/>

            <!-- Soft Floating Clouds -->
            <path d="M 90 110 Q 110 90 135 105 Q 160 85 185 105 Q 210 115 195 135 L 85 135 Q 70 120 90 110 Z" fill="#FFFFFF" opacity="0.95"/>
            <path d="M 330 140 Q 345 125 365 135 Q 385 120 405 135 Q 420 145 410 160 L 325 160 Q 315 145 330 140 Z" fill="#FFFFFF" opacity="0.85"/>

            <!-- Gentle Background Wave -->
            <path d="M 20 320 Q 140 300 270 320 T 520 320 L 520 390 L 20 390 Z" fill="#E0F2FE" opacity="0.75"/>

            <!-- 3D Elevated Umbrella Boat Group -->
            <g filter="url(#boat3dShadow)">
                <!-- Umbrella Mast / Hook Handle -->
                <path d="M 270 260 L 270 125 C 270 95 245 95 245 115" fill="none" stroke="#0F172A" stroke-width="7" stroke-linecap="round"/>

                <!-- Human Silhouettes inside Umbrella Boat -->
                <!-- Character 1 (Left / Friendly wave) -->
                <circle cx="230" cy="190" r="15" fill="#0B132B"/>
                <path d="M 205 245 C 205 210 255 210 255 245 Z" fill="#0B132B"/>
                <!-- Arm raised waving -->
                <path d="M 208 215 Q 190 200 185 185" fill="none" stroke="#0B132B" stroke-width="5" stroke-linecap="round"/>

                <!-- Character 2 (Right / Looking forward) -->
                <circle cx="295" cy="180" r="16" fill="#0284C7"/>
                <path d="M 270 245 C 270 205 320 205 320 245 Z" fill="#0284C7"/>

                <!-- Friendly Pet Dog Silhouette sitting on right bow -->
                <ellipse cx="355" cy="225" rx="15" ry="12" fill="#64748B"/>
                <circle cx="365" cy="214" r="9" fill="#64748B"/>
                <!-- Dog ears & snout -->
                <polygon points="360,207 364,213 358,213" fill="#475569"/>
                <polygon points="370,214 376,216 370,219" fill="#475569"/>

                <!-- Inverted Umbrella Canopy (Hull) -->
                <!-- Multi-segment 3D scalloped boat shell -->
                <path d="M 70 245 Q 270 375 470 245 
                         Q 420 265 370 245 
                         Q 320 265 270 245 
                         Q 220 265 170 245 
                         Q 120 265 70 245 Z" 
                      fill="url(#umbrellaBlue)"/>

                <!-- Panel 1 (Vibrant Azure) -->
                <path d="M 70 245 Q 170 345 170 245 Q 120 265 70 245 Z" fill="#0284C7"/>
                <!-- Panel 2 (Clean Cream White) -->
                <path d="M 170 245 Q 220 365 270 245 Q 220 265 170 245 Z" fill="#F8FAFC"/>
                <!-- Panel 3 (Deep Midnight) -->
                <path d="M 270 245 Q 320 365 370 245 Q 320 265 270 245 Z" fill="#0B132B"/>
                <!-- Panel 4 (Electric Ocean Blue) -->
                <path d="M 370 245 Q 420 345 470 245 Q 420 265 370 245 Z" fill="#0369A1"/>

                <!-- Canopy Rib Tips -->
                <circle cx="70" cy="245" r="4" fill="#0F172A"/>
                <circle cx="170" cy="245" r="4" fill="#0F172A"/>
                <circle cx="270" cy="245" r="4" fill="#0F172A"/>
                <circle cx="370" cy="245" r="4" fill="#0F172A"/>
                <circle cx="470" cy="245" r="4" fill="#0F172A"/>
            </g>

            <!-- Foreground Animated Water Wave -->
            <path d="M 0 335 Q 130 315 270 335 T 540 335 L 540 420 L 0 420 Z" fill="url(#waveFront)"/>
            <path d="M 0 355 Q 140 340 280 355 T 540 355 L 540 420 L 0 420 Z" fill="#38BDF8" opacity="0.3"/>

            <!-- Playful Little Water Ripple Circles -->
            <ellipse cx="140" cy="350" rx="24" ry="4" fill="#BAE6FD" opacity="0.6"/>
            <ellipse cx="380" cy="365" rx="30" ry="5" fill="#BAE6FD" opacity="0.6"/>
        </svg>
    </div>
    """
    return svg
