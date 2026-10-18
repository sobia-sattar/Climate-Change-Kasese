"""
icons.py - Professional SVG Vector Icons for RainCheck.

Replaces all informal emojis with clean, accessible Feather/Lucide style SVGs.
Ensures crisp rendering on high-DPI displays with configurable dimensions and colors.
"""

def get_svg_icon(name: str, size: int = 20, color: str = "currentColor", stroke_width: float = 2.0) -> str:
    """Return inline SVG XML string for specified icon name."""
    icons = {
        "shield": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>'
        ),
        "cloud-rain": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
            '<line x1="16" y1="13" x2="16" y2="21"></line>'
            '<line x1="8" y1="13" x2="8" y2="21"></line>'
            '<line x1="12" y1="15" x2="12" y2="23"></line>'
            '<path d="M20 16.58A5 5 0 0 0 18 7h-1.26A8 8 0 1 0 4 15.25"></path></svg>'
        ),
        "sun": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
            '<circle cx="12" cy="12" r="5"></circle>'
            '<line x1="12" y1="1" x2="12" y2="3"></line>'
            '<line x1="12" y1="21" x2="12" y2="23"></line>'
            '<line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>'
            '<line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>'
            '<line x1="1" y1="12" x2="3" y2="12"></line>'
            '<line x1="21" y1="12" x2="23" y2="12"></line>'
            '<line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>'
            '<line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>'
        ),
        "cloud-sun": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M12 2v2"></path>'
            '<path d="m4.93 4.93 1.41 1.41"></path>'
            '<path d="M20 12h2"></path>'
            '<path d="m19.07 4.93-1.41 1.41"></path>'
            '<path d="M15.947 12.65a4 4 0 0 0-5.925-4.128"></path>'
            '<path d="M13 22H7a5 5 0 1 1 4.9-6H13a3 3 0 0 1 0 6Z"></path></svg>'
        ),
        "cloud": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"></path></svg>'
        ),
        "cloud-lightning": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M19 16.9A5 5 0 0 0 18 7h-1.26a8 8 0 1 0-11.62 9"></path>'
            '<polyline points="13 11 9 17 15 17 11 23"></polyline></svg>'
        ),
        "droplets": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M7 16.3c2.2 0 4-1.83 4-4.05 0-1.16-.57-2.26-1.71-3.19S7.29 6.75 7 5.3c-.29 1.45-1.14 2.84-2.29 3.76S3 11.09 3 12.25c0 2.22 1.8 4.05 4 4.05z"></path>'
            '<path d="M12.56 6.6A10.97 10.97 0 0 0 14 3.02c.5 2.5 2 4.9 4 6.5s3 3.5 3 5.5a6.98 6.98 0 0 1-11.91 4.97"></path></svg>'
        ),
        "wind": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"></path></svg>'
        ),
        "sprout": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M7 20h10"></path>'
            '<path d="M10 20c5.5-2.5.8-6.4 3-10"></path>'
            '<path d="M9.5 9.4c1.1.8 1.8 2.2 2.3 3.7-2 .4-3.5.4-4.8-.3-1.2-.6-2.3-1.9-3-4.2 2.8-.5 4.4.1 5.5.8z"></path>'
            '<path d="M14.1 6a7 7 0 0 0-1.1 4c1.9-.1 3.3-.6 4.3-1.4 1-1 1.6-2.3 1.7-4.6-2.7.1-4 1-4.9 2z"></path></svg>'
        ),
        "navigation": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
            '<polygon points="3 11 22 2 13 21 11 13 3 11"></polygon></svg>'
        ),
        "store": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="m2 7 4.41-4.41A2 2 0 0 1 7.83 2h8.34a2 2 0 0 1 1.42.59L22 7"></path>'
            '<path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"></path>'
            '<path d="M15 22v-4a2 2 0 0 0-2-2h-2a2 2 0 0 0-2 2v4"></path>'
            '<path d="M2 7h20"></path>'
            '<path d="M22 7a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2"></path></svg>'
        ),
        "check-circle": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>'
            '<polyline points="22 4 12 14.01 9 11.01"></polyline></svg>'
        ),
        "alert-triangle": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"></path>'
            '<line x1="12" y1="9" x2="12" y2="13"></line>'
            '<line x1="12" y1="17" x2="12.01" y2="17"></line></svg>'
        ),
        "bar-chart": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
            '<line x1="18" y1="20" x2="18" y2="10"></line>'
            '<line x1="12" y1="20" x2="12" y2="4"></line>'
            '<line x1="6" y1="20" x2="6" y2="14"></line></svg>'
        ),
        "layers": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
            '<polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>'
            '<polyline points="2 17 12 22 22 17"></polyline>'
            '<polyline points="2 12 12 17 22 12"></polyline></svg>'
        ),
        "arrow-right": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
            '<line x1="5" y1="12" x2="19" y2="12"></line>'
            '<polyline points="12 5 19 12 12 19"></polyline></svg>'
        ),
        "activity": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
            '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>'
        ),
        "globe": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
            '<circle cx="12" cy="12" r="10"></circle>'
            '<line x1="2" y1="12" x2="22" y2="12"></line>'
            '<path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>'
        ),
        "map-pin": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>'
            '<circle cx="12" cy="10" r="3"></circle></svg>'
        ),
        "clock": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
            '<circle cx="12" cy="12" r="10"></circle>'
            '<polyline points="12 6 12 12 16 14"></polyline></svg>'
        ),
        "sliders": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
            '<line x1="4" y1="21" x2="4" y2="14"></line>'
            '<line x1="4" y1="10" x2="4" y2="3"></line>'
            '<line x1="12" y1="21" x2="12" y2="12"></line>'
            '<line x1="12" y1="8" x2="12" y2="3"></line>'
            '<line x1="20" y1="21" x2="20" y2="16"></line>'
            '<line x1="20" y1="12" x2="20" y2="3"></line>'
            '<line x1="1" y1="14" x2="7" y2="14"></line>'
            '<line x1="9" y1="8" x2="15" y2="8"></line>'
            '<line x1="17" y1="16" x2="23" y2="16"></line></svg>'
        ),
        "umbrella": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M23 12a11.05 11.05 0 0 0-22 0zm-5 7a3 3 0 0 1-6 0v-7"></path></svg>'
        ),
        "user": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>'
            '<circle cx="12" cy="7" r="4"></circle></svg>'
        ),
        "sparkles": (
            f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"></path></svg>'
        )
    }
    return icons.get(name, icons["shield"])
