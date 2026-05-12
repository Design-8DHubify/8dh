#!/usr/bin/env python3
"""Generate 8D Hubify Design System HTML — v2."""
import base64, os, re

BASE = os.path.dirname(os.path.abspath(__file__))

def b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

def svg(path):
    with open(path, 'r') as f:
        return f.read().strip()

hugein_b64 = b64(os.path.join(BASE, 'assets/fonts/Hugein.woff'))
henju_b64  = b64(os.path.join(BASE, 'assets/fonts/HenjuSans-Variable-new.woff2'))

logo_neg   = svg(os.path.join(BASE, 'assets/logos/svg/8dh-logo-versao-negativa.svg'))
logo_pos   = svg(os.path.join(BASE, 'assets/logos/svg/8dh-logo-versao-positiva.svg'))
logo_sym   = svg(os.path.join(BASE, 'assets/logos/svg/8dh-logo-simbolo.svg'))
logo_sym_n = svg(os.path.join(BASE, 'assets/logos/svg/8dh-logo-simbolo-negativo.svg'))
logo_h_neg = svg(os.path.join(BASE, 'assets/logos/svg/8dh-logo-horizontal-negativa.svg'))
logo_h_pos = svg(os.path.join(BASE, 'assets/logos/svg/8dh-logo-horizontal-positiva.svg'))

# ── Lucide-style icon paths (name: path_d) ───────────────────────────────────
ICONS = {
  "search":        "M11 3a8 8 0 1 0 0 16A8 8 0 0 0 11 3zM2 11a9 9 0 1 1 18 0 9 9 0 0 1-18 0zm15.657 4.243-3.536-3.536",
  "x":             "M18 6 6 18M6 6l12 12",
  "menu":          "M4 6h16M4 12h16M4 18h16",
  "chevron-down":  "m6 9 6 6 6-6",
  "chevron-up":    "m18 15-6-6-6 6",
  "chevron-right": "m9 18 6-6-6-6",
  "chevron-left":  "m15 18-6-6 6-6",
  "arrow-right":   "M5 12h14m-7-7 7 7-7 7",
  "arrow-left":    "M19 12H5m7 7-7-7 7-7",
  "arrow-up":      "M12 19V5m-7 7 7-7 7 7",
  "arrow-down":    "M12 5v14m7-7-7 7-7-7",
  "plus":          "M12 5v14M5 12h14",
  "minus":         "M5 12h14",
  "check":         "m5 12 5 5L20 7",
  "check-circle":  "M22 11.08V12a10 10 0 1 1-5.93-9.14M22 4 12 14.01l-3-3",
  "alert-circle":  "M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10zM12 8v4M12 16h.01",
  "info":          "M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10zM12 16v-4M12 8h.01",
  "play":          "M5 3l14 9-14 9V3z",
  "pause":         "M6 4h4v16H6zM14 4h4v16h-4z",
  "volume-2":      "M11 5 6 9H2v6h4l5 4V5zM19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07",
  "camera":        "M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2zM12 17a4 4 0 1 0 0-8 4 4 0 0 0 0 8z",
  "image":         "M21 19a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2zm-12.5-5.5 2.5 3 3.5-4.5 4.5 6H5z",
  "video":         "M22.54 6.42a2.78 2.78 0 0 0-1.945-1.957C18.88 4 12 4 12 4s-6.88 0-8.6.463A2.78 2.78 0 0 0 1.46 6.42 29 29 0 0 0 1 12a29 29 0 0 0 .46 5.58 2.78 2.78 0 0 0 1.945 1.957C5.12 20 12 20 12 20s6.88 0 8.595-.463a2.78 2.78 0 0 0 1.945-1.957A29 29 0 0 0 23 12a29 29 0 0 0-.46-5.58zM10 15V9l5.2 3z",
  "file":          "M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9zM13 2v7h7",
  "folder":        "M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z",
  "download":      "M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3",
  "upload":        "M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12",
  "copy":          "M20 9H11a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2-2V11a2 2 0 0 0-2-2zM5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1",
  "trash":         "M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M10 11v6M14 11v6",
  "edit":          "M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4z",
  "mail":          "M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2zM22 6l-10 7L2 6",
  "phone":         "M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 13.1 19.79 19.79 0 0 1 1.61 4.5 2 2 0 0 1 3.59 2.32h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L7.91 9.91a16 16 0 0 0 6.16 6.16l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z",
  "message-circle":"M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8z",
  "bell":          "M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9M13.73 21a2 2 0 0 1-3.46 0",
  "share-2":       "M18 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM6 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM18 22a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM8.59 13.51l6.83 3.98M15.41 6.51l-6.82 3.98",
  "user":          "M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z",
  "users":         "M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2M9 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75",
  "settings":      "M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z",
  "lock":          "M19 11H5a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7a2 2 0 0 0-2-2zM7 11V7a5 5 0 0 1 10 0v4",
  "unlock":        "M19 11H5a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7a2 2 0 0 0-2-2zM7 11V7a5 5 0 0 1 9.9-1",
  "eye":           "M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8zM12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6z",
  "eye-off":       "M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24M1 1l22 22",
  "bar-chart":     "M12 20V10M18 20V4M6 20v-4",
  "pie-chart":     "M21.21 15.89A10 10 0 1 1 8 2.83M22 12A10 10 0 0 0 12 2v10z",
  "trending-up":   "M23 6l-9.5 9.5-5-5L1 18M17 6h6v6",
  "trending-down": "M23 18l-9.5-9.5-5 5L1 6M17 18h6v-6",
  "database":      "M12 2C6.48 2 2 4.02 2 6.5v11C2 19.98 6.48 22 12 22s10-2.02 10-4.5v-11C22 4.02 17.52 2 12 2zM2 12c0 2.48 4.48 4.5 10 4.5s10-2.02 10-4.5M2 6.5C2 8.98 6.48 11 12 11s10-2.02 10-4.5",
  "activity":      "M22 12h-4l-3 9L9 3l-3 9H2",
  "star":          "M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01z",
  "heart":         "M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z",
  "bookmark":      "M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z",
  "link":          "M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71",
  "external-link": "M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14 21 3",
  "globe":         "M12 2a10 10 0 1 0 0 20A10 10 0 0 0 12 2zM2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z",
  "map-pin":       "M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0zM12 13a3 3 0 1 0 0-6 3 3 0 0 0 0 6z",
  "clock":         "M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 6v6l4 2",
  "calendar":      "M19 4H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zM16 2v4M8 2v4M3 10h18",
  "sun":           "M12 17a5 5 0 1 0 0-10 5 5 0 0 0 0 10zM12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42",
  "moon":          "M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z",
  "zap":           "M13 2 3 14h9l-1 8 10-12h-9z",
  "shield":        "M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z",
  "code":          "m16 18 6-6-6-6M8 6l-6 6 6 6",
  "terminal":      "m4 17 6-6-6-6M12 19h8",
  "layers":        "M12 2 2 7l10 5 10-5zM2 17l10 5 10-5M2 12l10 5 10-5",
  "grid":          "M3 3h7v7H3zM14 3h7v7h-7zM14 14h7v7h-7zM3 14h7v7H3z",
  "layout":        "M19 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2zM3 9h18M9 21V9",
  "package":       "M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16zM3.27 6.96 12 12.01l8.73-5.05M12 22.08V12",
  "cpu":           "M9 2H6a2 2 0 0 0-2 2v3M15 2h3a2 2 0 0 1 2 2v3M9 22H6a2 2 0 0 1-2-2v-3M15 22h3a2 2 0 0 0 2-2v-3M6 9h12v6H6zM9 9V6M15 9V6M9 18v3M15 18v3",
  "feather":       "M20.24 12.24a6 6 0 0 0-8.49-8.49L5 10.5V19h8.5zM16 8 2 22M17.5 15H9",
  "maximize":      "M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3",
  "minimize":      "M8 3v3a2 2 0 0 1-2 2H3m18 0h-3a2 2 0 0 1-2-2V3m0 18v-3a2 2 0 0 1 2-2h3M3 16h3a2 2 0 0 0 2 2v3",
  "refresh-cw":    "M23 4v6h-6M1 20v-6h6M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15",
  "loader":        "M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83",
  "filter":        "M22 3H2l8 9.46V19l4 2v-8.54z",
  "sliders":       "M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1 14h6M9 8h6M17 16h6",
  "tag":           "M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82zM7 7h.01",
  "toggle-left":   "M16 5H8a7 7 0 0 0 0 14h8a7 7 0 0 0 0-14zM8 15a3 3 0 1 1 0-6 3 3 0 0 1 0 6z",
  "toggle-right":  "M16 5H8a7 7 0 0 0 0 14h8a7 7 0 0 0 0-14zM16 15a3 3 0 1 1 0-6 3 3 0 0 1 0 6z",
  "credit-card":   "M1 4h22v16H1zM1 10h22",
  "dollar-sign":   "M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6",
  "percent":       "M19 5 5 19M6.5 6.5h.01M17.5 17.5h.01M9 4.5a2 2 0 1 0 0 4 2 2 0 0 0 0-4zM15 15.5a2 2 0 1 0 0 4 2 2 0 0 0 0-4z",
  "box":           "M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16zM3.27 6.96 12 12.01l8.73-5.05M12 22.08V12",
  "send":          "M22 2 11 13M22 2l-7 20-4-9-9-4 20-7z",
  "mic":           "M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3zM19 10v2a7 7 0 0 1-14 0v-2M12 19v4M8 23h8",
  "wifi":          "M5 12.55a11 11 0 0 1 14.08 0M1.42 9a16 16 0 0 1 21.16 0M8.53 16.11a6 6 0 0 1 6.95 0M12 20h.01",
  "bluetooth":     "M6.5 6.5l11 11L12 23V1l5.5 5.5-11 11",
}

icons_js = "{\n" + ",\n".join(f'  "{k}": "{v}"' for k, v in ICONS.items()) + "\n}"

HTML = f'''<!DOCTYPE html>
<html lang="pt-BR" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>8D Hubify — Design System</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script>
<style>
/* ── Fonts ─────────────────────────────────────────── */
@font-face {{
  font-family: 'Hugein';
  src: url('data:font/woff;base64,{hugein_b64}') format('woff');
  font-weight: 400; font-style: normal; font-display: block;
}}
@font-face {{
  font-family: 'Henju Sans';
  src: url('data:font/woff2;base64,{henju_b64}') format('woff2');
  font-weight: 100 900; font-style: normal; font-display: block;
}}

/* ── Theme tokens ──────────────────────────────────── */
:root {{
  --cometa:        #6633FF;
  --cometa-dim:    rgba(102,51,255,.15);
  --galaxia:       #000033;
  --via-lactea:    #DADBFD;
  --interestelar:  #FFCE44;
  --nuvem:         #ED694B;
  --solar:         #FFFFFF;

  --font-d: 'Hugein','serif';
  --font-b: 'Henju Sans','sans-serif';
  --font-m: 'JetBrains Mono','Fira Code',ui-monospace,monospace;

  --dur-f: 150ms; --dur-b: 300ms; --dur-s: 600ms;
  --ease-s: cubic-bezier(.25,.46,.45,.94);
  --ease-p: cubic-bezier(.34,1.56,.64,1);
  --ease-e: cubic-bezier(.16,1,.3,1);
}}

[data-theme="dark"] {{
  --bg:       #000033;
  --bg2:      #06063d;
  --bg3:      rgba(255,255,255,.04);
  --surface:  rgba(255,255,255,.06);
  --border:   rgba(255,255,255,.08);
  --border2:  rgba(255,255,255,.14);
  --text:     #FFFFFF;
  --text2:    rgba(255,255,255,.6);
  --text3:    rgba(255,255,255,.3);
  --ascii-color: #6633FF;
  --shadow:   0 16px 48px rgba(0,0,51,.6);
}}
[data-theme="light"] {{
  --bg:       #F5F5FF;
  --bg2:      #EEEEFF;
  --bg3:      rgba(0,0,51,.03);
  --surface:  rgba(0,0,51,.04);
  --border:   rgba(0,0,51,.08);
  --border2:  rgba(0,0,51,.16);
  --text:     #000033;
  --text2:    rgba(0,0,51,.6);
  --text3:    rgba(0,0,51,.3);
  --ascii-color: #6633FF;
  --shadow:   0 16px 48px rgba(0,0,51,.12);
}}

/* ── Reset ─────────────────────────────────────────── */
*,*::before,*::after{{ box-sizing:border-box; margin:0; padding:0; }}
html{{ font-size:16px; scroll-behavior:smooth; }}
body{{
  font-family:var(--font-b); font-weight:400; font-style:normal;
  background:var(--bg); color:var(--text);
  -webkit-font-smoothing:antialiased;
  transition: background var(--dur-s) var(--ease-s), color var(--dur-s) var(--ease-s);
  overflow-x:hidden;
}}

/* ── Layout ─────────────────────────────────────────── */
.wrap{{ width:100%; max-width:1400px; margin-inline:auto; padding-inline:clamp(24px,5vw,80px); }}
.wrap-wide{{ width:100%; max-width:1600px; margin-inline:auto; padding-inline:clamp(24px,4vw,64px); }}

.section{{ padding-block:clamp(80px,12vh,160px); border-top:1px solid var(--border); position:relative; }}
.section-head{{
  display:grid; grid-template-columns:1fr; gap:20px;
  margin-bottom:clamp(48px,8vh,96px); position:relative;
}}
.section-num{{
  font-family:var(--font-d); font-size:clamp(5rem,16vw,14rem); font-weight:400;
  line-height:.85; letter-spacing:-.04em; color:var(--text);
  opacity:.06; pointer-events:none; user-select:none;
  position:absolute; top:-.4em; right:0; z-index:0;
}}
.section-eyebrow{{
  font-family:var(--font-m); font-size:.7rem; color:var(--cometa);
  letter-spacing:.22em; text-transform:uppercase; font-weight:600;
  display:flex; align-items:center; gap:14px; position:relative; z-index:1;
}}
.section-eyebrow::before{{
  content:''; width:32px; height:1px; background:var(--cometa);
}}
.section-title{{
  font-family:var(--font-d); font-size:clamp(2.4rem,6vw,5rem); font-weight:400;
  line-height:.95; letter-spacing:-.03em; color:var(--text);
  position:relative; z-index:1; max-width:14ch;
}}
.section-title em{{ font-style:normal; color:var(--cometa); }}
.section-desc{{
  font-family:var(--font-b); font-size:clamp(1rem,1.5vw,1.15rem); font-weight:300;
  line-height:1.55; color:var(--text2); max-width:50ch; position:relative; z-index:1;
}}

/* ── Loader ─────────────────────────────────────────── */
#loader{{
  position:fixed; inset:0; z-index:9999;
  background:var(--galaxia);
  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:24px;
  transition:opacity .7s var(--ease-e), visibility .7s;
}}
#loader.gone{{ opacity:0; visibility:hidden; pointer-events:none; }}
.l-bar{{ width:100px; height:1px; background:rgba(255,255,255,.1); position:relative; overflow:hidden; }}
.l-bar::after{{ content:''; position:absolute; inset-block:0; left:-100%; width:50%;
  background:var(--cometa); animation:lbar .9s var(--ease-e) forwards; }}
@keyframes lbar{{ to{{ left:100%; }} }}

/* ── Cursor ─────────────────────────────────────────── */
#cursor{{
  position:fixed; top:0; left:0; pointer-events:none; z-index:9990;
  width:14px; height:14px; border-radius:50%; background:var(--cometa);
  transform:translate(-50%,-50%); mix-blend-mode:exclusion;
  will-change:transform; transition:width var(--dur-b) var(--ease-p), height var(--dur-b) var(--ease-p);
}}
#cursor.big{{ width:48px; height:48px; }}

/* ── Grain noise overlay ─────────────────────────────── */
body::before{{
  content:''; position:fixed; inset:0; z-index:9980; pointer-events:none;
  opacity:.025; background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-size:200px 200px;
  animation:grainAnim .4s steps(1) infinite;
}}
@keyframes grainAnim{{
  0%{{ background-position:0 0; }} 20%{{ background-position:-30px 10px; }}
  40%{{ background-position:20px -15px; }} 60%{{ background-position:-10px 25px; }}
  80%{{ background-position:30px -5px; }} 100%{{ background-position:5px 20px; }}
}}
[data-theme="light"] body::before{{ opacity:.015; }}

/* ── Nav ─────────────────────────────────────────────── */
nav{{
  position:fixed; top:0; left:0; right:0; z-index:100;
  padding:18px 0;
  background:rgba(0,0,51,.75);
  backdrop-filter:blur(24px); -webkit-backdrop-filter:blur(24px);
  border-bottom:1px solid var(--border);
  transition:background var(--dur-s);
}}
[data-theme="light"] nav{{ background:rgba(245,245,255,.85); }}
.nav-inner{{ display:flex; align-items:center; justify-content:space-between; }}
.nav-logo{{ width:110px; display:block; }}
.nav-links{{ display:flex; gap:32px; list-style:none; align-items:center; }}
.nav-links a{{
  color:var(--text2); text-decoration:none; font-size:.8rem;
  font-weight:500; letter-spacing:.08em; text-transform:uppercase;
  transition:color var(--dur-b);
}}
.nav-links a:hover{{ color:var(--text); }}
#theme-btn{{
  width:36px; height:36px; border-radius:50%; border:1px solid var(--border2);
  background:var(--surface); color:var(--text); cursor:pointer;
  display:flex; align-items:center; justify-content:center;
  transition:background var(--dur-b), border-color var(--dur-b);
}}
#theme-btn:hover{{ background:var(--cometa-dim); border-color:var(--cometa); }}
#theme-btn svg{{ width:16px; height:16px; stroke:currentColor; fill:none; stroke-width:2; stroke-linecap:round; stroke-linejoin:round; }}

/* ── Hero ────────────────────────────────────────────── */
.hero{{
  min-height:100vh; position:relative; overflow:hidden;
  padding:120px clamp(24px,5vw,80px) 60px;
  display:grid; grid-template-rows:auto 1fr auto; gap:0;
}}
.hero-top{{
  display:flex; align-items:flex-start; justify-content:space-between;
  font-family:var(--font-m); font-size:.68rem; letter-spacing:.18em;
  text-transform:uppercase; color:var(--text2);
  opacity:0; animation:fadeUp .8s .2s var(--ease-e) forwards;
}}
.hero-top-l{{ display:flex; flex-direction:column; gap:6px; }}
.hero-top-r{{ display:flex; flex-direction:column; gap:6px; text-align:right; }}
.hero-top em{{ font-style:normal; color:var(--cometa); }}
.hero-top-r .pulse{{
  display:inline-flex; align-items:center; gap:8px;
}}
.hero-top-r .pulse::before{{
  content:''; width:6px; height:6px; border-radius:50%; background:#5fff8a;
  box-shadow:0 0 12px rgba(95,255,138,.8); animation:pulse 1.4s ease-in-out infinite;
}}
@keyframes pulse{{ 0%,100%{{opacity:1}} 50%{{opacity:.35}} }}

.hero-center{{
  display:grid; grid-template-columns:1fr; align-items:center; gap:32px;
  position:relative; padding:60px 0;
}}
@media(min-width:900px){{ .hero-center{{ grid-template-columns:1.1fr 1fr; gap:48px; }} }}

.hero-headline{{
  position:relative; z-index:2;
  opacity:0; animation:fadeUp 1s .5s var(--ease-e) forwards;
}}
.hero-kicker{{
  display:inline-flex; align-items:center; gap:10px;
  font-family:var(--font-m); font-size:.65rem; letter-spacing:.22em;
  text-transform:uppercase; color:var(--cometa); margin-bottom:32px;
  padding:6px 14px; border:1px solid rgba(102,51,255,.35); border-radius:9999px;
  background:rgba(102,51,255,.06);
}}
.hero-kicker::before{{
  content:''; width:5px; height:5px; border-radius:50%; background:var(--cometa);
}}
.hero-h1{{
  font-family:var(--font-d); font-weight:400;
  font-size:clamp(4rem,11vw,11rem); line-height:.88;
  letter-spacing:-.045em; color:var(--text);
}}
.hero-h1 .line{{ display:block; overflow:hidden; }}
.hero-h1 .line span{{ display:inline-block; }}
.hero-h1 em{{ font-style:normal; color:var(--cometa); position:relative; }}
.hero-h1 em::after{{
  content:''; position:absolute; left:0; right:0; bottom:.08em; height:.05em;
  background:var(--cometa); opacity:.35;
}}
.hero-lede{{
  font-family:var(--font-b); font-size:clamp(1rem,1.4vw,1.15rem);
  color:var(--text2); margin-top:32px; max-width:42ch; line-height:1.55;
  font-weight:300;
}}
.hero-cta-row{{
  display:flex; gap:14px; margin-top:40px; flex-wrap:wrap; align-items:center;
}}

.hero-ascii-col{{
  position:relative; min-height:380px;
  display:flex; align-items:center; justify-content:center;
  opacity:0; animation:fadeUp 1.2s .8s var(--ease-e) forwards;
}}
.ascii-hero-wrap{{
  position:relative; width:100%;
  border:1px solid var(--border); border-radius:24px; overflow:hidden;
  background:linear-gradient(135deg, rgba(102,51,255,.04), rgba(0,0,0,0) 60%);
}}
.ascii-hero-wrap::before{{
  content:'01 / ASCII ENGINE'; position:absolute; top:14px; left:18px; z-index:2;
  font-family:var(--font-m); font-size:.6rem; color:var(--text3);
  letter-spacing:.18em; text-transform:uppercase;
}}
.ascii-hero-wrap::after{{
  content:'MOVE MOUSE →'; position:absolute; bottom:14px; right:18px; z-index:2;
  font-family:var(--font-m); font-size:.6rem; color:var(--text3);
  letter-spacing:.18em;
}}
#ascii-canvas{{
  display:block; width:100%; height:auto; cursor:crosshair;
}}

.hero-bottom{{
  display:grid; grid-template-columns:repeat(4,1fr); gap:24px;
  padding-top:48px; border-top:1px solid var(--border);
  opacity:0; animation:fadeUp .8s 1.2s var(--ease-e) forwards;
}}
.hero-stat{{ display:flex; flex-direction:column; gap:4px; }}
.hero-stat-num{{
  font-family:var(--font-d); font-size:clamp(2rem,4vw,3rem); font-weight:400;
  letter-spacing:-.02em; line-height:1; color:var(--text);
}}
.hero-stat-num em{{ font-style:normal; color:var(--cometa); }}
.hero-stat-label{{
  font-family:var(--font-m); font-size:.6rem; color:var(--text3);
  letter-spacing:.18em; text-transform:uppercase;
}}
@media(max-width:700px){{ .hero-bottom{{ grid-template-columns:repeat(2,1fr); }} }}

@keyframes fadeUp{{ from{{opacity:0;transform:translateY(30px)}} to{{opacity:1;transform:none}} }}

/* ── Marquee ─────────────────────────────────────────── */
.marquee{{
  overflow:hidden; padding:24px 0; border-block:1px solid var(--border);
  background:var(--bg2);
  position:relative;
}}
.marquee-track{{
  display:flex; gap:48px; white-space:nowrap; width:max-content;
  animation:marqueeScroll 38s linear infinite;
  will-change:transform;
}}
.marquee-track:hover{{ animation-play-state:paused; }}
.marquee span{{
  font-family:var(--font-d); font-size:clamp(2rem,5vw,4rem); font-weight:400;
  letter-spacing:-.02em; color:var(--text);
  display:flex; align-items:center; gap:48px;
}}
.marquee span em{{
  font-style:normal; color:var(--cometa);
  font-size:.6em; display:inline-block; transform:translateY(-.1em);
}}
@keyframes marqueeScroll{{
  from{{ transform:translateX(0); }}
  to{{ transform:translateX(-50%); }}
}}

/* ── Colors ──────────────────────────────────────────── */
.color-grid{{ display:grid; grid-template-columns:repeat(auto-fill,minmax(150px,1fr)); gap:12px; }}
.color-chip{{ border-radius:16px; overflow:hidden; border:1px solid var(--border); }}
.color-swatch{{ height:110px; }}
.color-meta{{ padding:12px 14px; background:var(--surface); }}
.color-name{{ font-family:var(--font-m); font-size:.7rem; color:var(--text); font-weight:600; letter-spacing:.05em; text-transform:uppercase; }}
.color-hex{{ font-family:var(--font-m); font-size:.65rem; color:var(--text3); margin-top:2px; }}

/* ── Color (refined) ──────────────────────────────── */
.color-feature{{
  display:grid; grid-template-columns:1.2fr 1fr; gap:0;
  border-radius:28px; overflow:hidden; border:1px solid var(--border);
  margin-bottom:32px; min-height:340px;
}}
@media(max-width:800px){{ .color-feature{{ grid-template-columns:1fr; }} }}
.color-feature-swatch{{
  background:#6633FF; position:relative; display:flex; flex-direction:column;
  justify-content:space-between; padding:32px 36px; color:#fff;
}}
.color-feature-swatch::after{{
  content:'✦'; position:absolute; right:-40px; bottom:-80px;
  font-family:var(--font-d); font-size:24rem; line-height:.8;
  color:rgba(255,255,255,.08); pointer-events:none;
}}
.color-feature-num{{
  font-family:var(--font-m); font-size:.65rem; letter-spacing:.2em;
  text-transform:uppercase; opacity:.7;
}}
.color-feature-name{{
  font-family:var(--font-d); font-size:clamp(3rem,6vw,5rem); font-weight:400;
  letter-spacing:-.03em; line-height:.95; position:relative; z-index:1;
}}
.color-feature-hex{{
  font-family:var(--font-m); font-size:.85rem; letter-spacing:.08em; opacity:.85;
}}
.color-feature-meta{{
  padding:32px 36px; display:flex; flex-direction:column; gap:18px;
  background:var(--bg2); justify-content:center;
}}
.color-feature-meta h4{{
  font-family:var(--font-m); font-size:.65rem; letter-spacing:.18em;
  text-transform:uppercase; color:var(--text3); font-weight:600;
}}
.color-feature-meta p{{
  font-family:var(--font-b); font-size:1rem; color:var(--text2);
  line-height:1.65; font-weight:300;
}}
.color-feature-vals{{
  display:grid; grid-template-columns:repeat(2,1fr); gap:14px;
  margin-top:8px; padding-top:18px; border-top:1px solid var(--border);
}}
.color-val{{ font-family:var(--font-m); font-size:.7rem; }}
.color-val-k{{ color:var(--text3); display:block; margin-bottom:3px; letter-spacing:.1em; text-transform:uppercase; }}
.color-val-v{{ color:var(--text); }}

.color-grid{{ display:grid; grid-template-columns:repeat(auto-fill,minmax(180px,1fr)); gap:14px; }}
.color-chip{{
  border-radius:20px; overflow:hidden; border:1px solid var(--border);
  transition:transform var(--dur-b) var(--ease-p), border-color var(--dur-b);
  cursor:default;
}}
.color-chip:hover{{ transform:translateY(-4px); border-color:var(--border2); }}
.color-swatch{{ height:140px; position:relative; }}
.color-swatch-tag{{
  position:absolute; top:12px; right:12px;
  font-family:var(--font-m); font-size:.55rem; letter-spacing:.15em;
  text-transform:uppercase; padding:4px 8px; border-radius:6px;
  background:rgba(0,0,0,.35); color:#fff; backdrop-filter:blur(4px);
}}
.color-swatch-tag.dark{{ background:rgba(255,255,255,.85); color:#000; }}
.color-meta{{ padding:16px 18px; background:var(--surface); }}
.color-name{{ font-family:var(--font-d); font-size:1.3rem; color:var(--text); font-weight:400; letter-spacing:-.01em; }}
.color-role{{ font-family:var(--font-m); font-size:.6rem; color:var(--cometa); margin-top:6px; letter-spacing:.15em; text-transform:uppercase; font-weight:600; }}
.color-hex{{ font-family:var(--font-m); font-size:.7rem; color:var(--text3); margin-top:6px; }}

/* Color pairings */
.pairings{{ margin-top:32px; display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:14px; }}
.pair{{
  border-radius:18px; overflow:hidden; border:1px solid var(--border);
  display:grid; grid-template-columns:1fr 1fr; min-height:120px;
  position:relative;
}}
.pair-label{{
  position:absolute; top:12px; left:14px; z-index:2;
  font-family:var(--font-m); font-size:.55rem; letter-spacing:.15em;
  text-transform:uppercase; padding:4px 8px; border-radius:6px;
  background:rgba(0,0,0,.35); color:#fff; backdrop-filter:blur(4px);
}}

/* ── Type ────────────────────────────────────────────── */
.type-specimens{{
  display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-bottom:40px;
}}
@media(max-width:800px){{ .type-specimens{{ grid-template-columns:1fr; }} }}
.type-specimen{{
  position:relative; border-radius:24px; padding:40px 36px;
  border:1px solid var(--border); background:var(--bg2);
  overflow:hidden; min-height:340px;
  display:flex; flex-direction:column; justify-content:space-between;
}}
.type-specimen-tag{{
  font-family:var(--font-m); font-size:.6rem; color:var(--cometa);
  letter-spacing:.18em; text-transform:uppercase; font-weight:600;
}}
.type-specimen-Aa{{
  font-family:var(--font-d); font-size:clamp(8rem,18vw,16rem); line-height:.85;
  font-weight:400; letter-spacing:-.04em; color:var(--text);
  margin:8px 0;
}}
.type-specimen-Aa.henju{{ font-family:var(--font-b); font-weight:400; }}
.type-specimen-name{{
  font-family:var(--font-d); font-size:2rem; font-weight:400;
  letter-spacing:-.02em; color:var(--text);
}}
.type-specimen-meta{{
  display:flex; gap:24px; margin-top:8px;
  font-family:var(--font-m); font-size:.65rem;
  color:var(--text3); letter-spacing:.1em; text-transform:uppercase;
}}
.type-specimen-meta b{{ color:var(--text); font-weight:600; display:block; margin-top:3px; font-family:var(--font-d); font-size:.95rem; letter-spacing:0; text-transform:none; }}

.type-scale{{ display:flex; flex-direction:column; border-radius:24px; overflow:hidden; border:1px solid var(--border); }}
.type-row{{
  display:grid; grid-template-columns:130px 1fr;
  gap:24px; align-items:center;
  padding:24px 28px; border-bottom:1px solid var(--border);
  transition:background var(--dur-b);
}}
.type-row:last-child{{ border-bottom:none; }}
.type-row:hover{{ background:var(--surface); }}
.type-meta{{ font-family:var(--font-m); font-size:.6rem; color:var(--text3); line-height:1.8; letter-spacing:.05em; }}
.type-meta b{{ color:var(--cometa); font-weight:600; text-transform:uppercase; letter-spacing:.15em; font-size:.6rem; display:block; margin-bottom:4px; }}

.weights-demo{{ display:flex; flex-direction:column; gap:2px; margin-top:32px; padding:24px; border-radius:24px; border:1px solid var(--border); background:var(--bg2); }}
.weights-head{{ font-family:var(--font-m); font-size:.6rem; color:var(--cometa); letter-spacing:.2em; text-transform:uppercase; padding:8px 16px; font-weight:600; }}
.weight-row{{
  display:flex; align-items:center; gap:24px; padding:14px 16px;
  border-radius:10px; transition:background var(--dur-b);
}}
.weight-row:hover{{ background:var(--surface); }}
.weight-num{{ font-family:var(--font-m); font-size:.65rem; color:var(--text3); width:60px; letter-spacing:.1em; }}
.weight-text{{ font-family:var(--font-b); font-size:1.4rem; font-style:normal; color:var(--text); flex:1; }}

.pangram{{
  margin-top:32px; padding:48px 40px; border-radius:24px;
  background:linear-gradient(135deg, var(--cometa), #2200cc);
  color:#fff;
}}
.pangram-tag{{
  font-family:var(--font-m); font-size:.6rem; letter-spacing:.2em;
  text-transform:uppercase; opacity:.7; margin-bottom:16px;
}}
.pangram-text{{
  font-family:var(--font-d); font-size:clamp(1.8rem,4vw,3rem);
  font-weight:400; letter-spacing:-.02em; line-height:1.05;
}}

/* ── Logos ───────────────────────────────────────────── */
.logo-feature{{
  display:grid; grid-template-columns:1.4fr 1fr; gap:0;
  border-radius:28px; overflow:hidden; border:1px solid var(--border);
  margin-bottom:16px; min-height:360px;
}}
@media(max-width:800px){{ .logo-feature{{ grid-template-columns:1fr; }} }}
.logo-feature-display{{
  background:var(--galaxia); padding:60px;
  display:flex; align-items:center; justify-content:center;
  position:relative; overflow:hidden;
}}
.logo-feature-display::before{{
  content:''; position:absolute; inset:-50%;
  background:radial-gradient(circle at 30% 40%, rgba(102,51,255,.25), transparent 50%);
  pointer-events:none;
}}
.logo-feature-display svg{{ max-width:380px; max-height:140px; width:100%; position:relative; z-index:1; }}
.logo-feature-info{{
  padding:36px; display:flex; flex-direction:column; gap:14px;
  background:var(--bg2); justify-content:center;
}}
.logo-feature-info h4{{ font-family:var(--font-m); font-size:.6rem; letter-spacing:.18em; text-transform:uppercase; color:var(--cometa); font-weight:600; }}
.logo-feature-info .name{{ font-family:var(--font-d); font-size:2.2rem; font-weight:400; letter-spacing:-.02em; color:var(--text); }}
.logo-feature-info p{{ font-family:var(--font-b); font-size:.95rem; color:var(--text2); line-height:1.65; font-weight:300; }}
.logo-feature-rules{{
  margin-top:10px; padding-top:18px; border-top:1px solid var(--border);
  display:flex; flex-direction:column; gap:8px;
}}
.logo-rule{{ display:flex; gap:14px; font-family:var(--font-m); font-size:.7rem; color:var(--text2); }}
.logo-rule::before{{ content:'✓'; color:var(--cometa); font-weight:bold; }}

.logo-grid{{ display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:12px; }}
.logo-card{{
  border-radius:20px; padding:36px 28px;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  gap:18px; min-height:180px; border:1px solid var(--border);
  transition:border-color var(--dur-b), transform var(--dur-b) var(--ease-p);
  cursor:default;
}}
.logo-card:hover{{ transform:translateY(-4px); border-color:var(--cometa); }}
.logo-card.on-dark{{ background:#000033; }}
.logo-card.on-light{{ background:#FFFFFF; }}
.logo-card.on-surface{{ background:var(--surface); }}
.logo-card svg{{ max-width:160px; max-height:60px; width:100%; }}
.logo-label{{ font-family:var(--font-m); font-size:.6rem; letter-spacing:.18em; text-transform:uppercase; color:var(--text3); font-weight:600; }}
.logo-card.on-light .logo-label{{ color:rgba(0,0,51,.35); }}
.logo-card.on-dark .logo-label{{ color:rgba(255,255,255,.35); }}

/* ── Components ──────────────────────────────────────── */
.comp-group{{ margin-bottom:56px; }}
.comp-label{{
  font-family:var(--font-m); font-size:.65rem; color:var(--text3);
  letter-spacing:.12em; text-transform:uppercase;
  margin-bottom:16px; padding-bottom:10px; border-bottom:1px solid var(--border);
}}
.comp-row{{
  display:flex; flex-wrap:wrap; align-items:center; gap:12px;
  padding:24px; background:var(--surface); border-radius:16px; border:1px solid var(--border);
}}

/* Buttons */
.btn{{
  display:inline-flex; align-items:center; gap:8px;
  padding:13px 28px; font-family:var(--font-b);
  font-size:.875rem; font-weight:600; letter-spacing:.02em;
  border-radius:9999px; border:2px solid transparent;
  cursor:pointer; text-decoration:none; line-height:1;
  transition:background var(--dur-b) var(--ease-s), box-shadow var(--dur-b) var(--ease-s), transform var(--dur-f) var(--ease-p), border-color var(--dur-b), color var(--dur-b);
  position:relative; overflow:hidden;
}}
.btn:active{{ transform:scale(.96); }}
.btn-primary{{ background:var(--cometa); color:#fff; border-color:var(--cometa); }}
.btn-primary:hover{{ background:#7a4fff; box-shadow:0 0 32px rgba(102,51,255,.45); }}
.btn-secondary{{ background:transparent; color:var(--cometa); border-color:var(--cometa); }}
.btn-secondary:hover{{ background:var(--cometa); color:#fff; }}
.btn-ghost{{ background:transparent; color:var(--text2); border-color:var(--border2); }}
.btn-ghost:hover{{ border-color:var(--text); color:var(--text); background:var(--surface); }}
.btn-warm{{ background:var(--interestelar); color:var(--galaxia); font-weight:700; border-color:var(--interestelar); }}
.btn-warm:hover{{ filter:brightness(1.1); }}
.btn-sm{{ padding:8px 18px; font-size:.78rem; }}
.btn-lg{{ padding:17px 36px; font-size:1rem; }}

/* Magnetic btn wrapper */
.mag-wrap{{ display:inline-block; position:relative; }}

/* Badges */
.badge{{
  display:inline-flex; align-items:center; padding:4px 11px;
  font-family:var(--font-m); font-size:.65rem; font-weight:600;
  letter-spacing:.1em; text-transform:uppercase; border-radius:9999px; border:1px solid transparent;
}}
.badge-cometa{{ background:var(--cometa-dim); color:var(--cometa); border-color:rgba(102,51,255,.2); }}
.badge-solar{{ background:var(--surface); color:var(--text); border-color:var(--border2); }}
.badge-warm{{ background:rgba(255,206,68,.12); color:var(--interestelar); border-color:rgba(255,206,68,.25); }}
.badge-coral{{ background:rgba(237,105,75,.12); color:var(--nuvem); border-color:rgba(237,105,75,.2); }}
.badge-new{{ background:var(--cometa); color:#fff; }}

/* Cards */
.card-grid{{ display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:12px; }}
.card{{
  border-radius:20px; padding:28px; border:1px solid var(--border);
  transition:transform var(--dur-b) var(--ease-p), box-shadow var(--dur-b) var(--ease-s), border-color var(--dur-b);
  cursor:default;
}}
.card:hover{{ transform:translateY(-5px); box-shadow:var(--shadow); border-color:var(--border2); }}
.card-dark{{ background:var(--surface); color:var(--text); }}
.card-accent{{ background:linear-gradient(135deg,var(--cometa),#2200cc); color:#fff; border-color:rgba(102,51,255,.35); }}
.card-glass{{ background:var(--surface); backdrop-filter:blur(20px); color:var(--text); }}
.card-warm{{ background:linear-gradient(135deg,rgba(255,206,68,.1),rgba(255,206,68,.03)); border-color:rgba(255,206,68,.18); color:var(--text); }}
.card-tag{{ font-family:var(--font-m); font-size:.62rem; letter-spacing:.12em; text-transform:uppercase; opacity:.45; margin-bottom:10px; }}
.card-title{{ font-weight:700; font-size:1.1rem; margin-bottom:8px; }}
.card-body{{ font-size:.875rem; opacity:.6; line-height:1.65; }}

/* Input */
.input{{
  width:100%; padding:13px 18px; font-family:var(--font-b); font-size:1rem;
  color:var(--text); background:var(--surface); border:2px solid var(--border);
  border-radius:10px; outline:none;
  transition:border-color var(--dur-b), box-shadow var(--dur-b), background var(--dur-b);
}}
.input::placeholder{{ color:var(--text3); }}
.input:focus{{ border-color:var(--cometa); box-shadow:0 0 0 4px rgba(102,51,255,.12); background:var(--bg); }}
.input-label{{ font-family:var(--font-m); font-size:.65rem; color:var(--text3); letter-spacing:.1em; text-transform:uppercase; margin-bottom:6px; display:block; }}

/* ── Effects Showcase ─────────────────────────────────── */
.effects-grid{{ display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:16px; }}
.effect-card{{
  border-radius:20px; padding:32px; border:1px solid var(--border);
  background:var(--surface); position:relative; overflow:hidden; min-height:160px;
  display:flex; flex-direction:column; justify-content:flex-end; gap:12px;
}}
.effect-label{{ font-family:var(--font-m); font-size:.65rem; letter-spacing:.12em; text-transform:uppercase; color:var(--cometa); }}
.effect-title{{ font-family:var(--font-b); font-size:1rem; font-weight:600; color:var(--text); }}

/* Effect 1 — Gradient mesh */
.fx-mesh{{
  background:linear-gradient(-45deg,var(--cometa),#3300cc,var(--nuvem),var(--interestelar));
  background-size:400% 400%; animation:meshAnim 6s ease infinite;
}}
@keyframes meshAnim{{ 0%{{background-position:0 50%}} 50%{{background-position:100% 50%}} 100%{{background-position:0 50%}} }}
.fx-mesh .effect-label,.fx-mesh .effect-title{{ color:#fff; }}

/* Effect 2 — Morphing blob */
.fx-blob{{ background:var(--bg2); }}
.blob-shape{{
  position:absolute; top:-20px; right:-20px;
  width:120px; height:120px; background:var(--cometa); opacity:.5;
  animation:blobMorph 6s ease-in-out infinite;
}}
@keyframes blobMorph{{
  0%{{ border-radius:60% 40% 30% 70%/60% 30% 70% 40%; }}
  50%{{ border-radius:30% 60% 70% 40%/50% 60% 30% 60%; }}
  100%{{ border-radius:60% 40% 30% 70%/60% 30% 70% 40%; }}
}}

/* Effect 3 — Marquee */
.fx-marquee{{ padding:0; overflow:hidden; }}
.marquee-track{{
  display:flex; width:max-content; gap:40px;
  animation:marquee 14s linear infinite;
  padding:32px 0;
}}
.fx-marquee:hover .marquee-track{{ animation-play-state:paused; }}
@keyframes marquee{{ to{{ transform:translateX(-50%); }} }}
.marquee-item{{ font-family:var(--font-d); font-size:1.4rem; color:var(--text); white-space:nowrap; display:flex; align-items:center; gap:20px; }}
.marquee-dot{{ width:6px; height:6px; border-radius:50%; background:var(--cometa); display:inline-block; }}

/* Effect 4 — Spotlight */
.fx-spotlight{{ cursor:none; }}
.spotlight-hole{{
  position:absolute; inset:0;
  background:radial-gradient(circle 80px at var(--mx,50%) var(--my,50%), transparent 0%, rgba(0,0,30,.85) 100%);
  border-radius:20px; pointer-events:none;
}}

/* Effect 5 — Glitch text */
.glitch{{ position:relative; font-family:var(--font-d); font-size:2.2rem; color:var(--text); cursor:default; }}
.glitch::before,.glitch::after{{
  content:attr(data-text); position:absolute; top:0; left:0;
  width:100%; overflow:hidden;
}}
.glitch::before{{ color:var(--cometa); animation:glitch1 3s infinite; clip-path:polygon(0 0,100% 0,100% 35%,0 35%); }}
.glitch::after{{ color:var(--nuvem); animation:glitch2 3s infinite; clip-path:polygon(0 65%,100% 65%,100% 100%,0 100%); }}
@keyframes glitch1{{
  0%,90%{{ transform:none; opacity:0; }} 92%{{ transform:translate(-2px,1px); opacity:.8; }}
  94%{{ transform:translate(2px,-1px); opacity:.8; }} 96%{{ transform:none; opacity:0; }}
}}
@keyframes glitch2{{
  0%,92%{{ transform:none; opacity:0; }} 94%{{ transform:translate(2px,1px); opacity:.7; }}
  96%{{ transform:translate(-2px,-1px); opacity:.7; }} 98%{{ transform:none; opacity:0; }}
}}

/* Effect 6 — Parallax tilt card */
.fx-tilt{{ transform-style:preserve-3d; perspective:800px; transition:transform .05s; }}
.tilt-inner{{ transform-style:preserve-3d; transition:transform .05s; }}
.tilt-shine{{
  position:absolute; inset:0; border-radius:20px;
  background:radial-gradient(circle at var(--tx,50%) var(--ty,50%), rgba(255,255,255,.12) 0%, transparent 60%);
  pointer-events:none;
}}

/* Effect 7 — Scramble text */
.scramble{{ font-family:var(--font-m); font-size:1.3rem; color:var(--cometa); cursor:pointer; letter-spacing:.05em; }}

/* Effect 8 — Gradient border */
.fx-gborder{{
  position:relative; background:var(--bg);
  border-radius:20px; padding:32px; min-height:160px;
  display:flex; flex-direction:column; justify-content:flex-end; gap:12px;
}}
.fx-gborder::before{{
  content:''; position:absolute; inset:-1.5px; border-radius:21px; z-index:-1;
  background:conic-gradient(from var(--border-angle,0deg), var(--cometa), var(--interestelar), var(--nuvem), var(--cometa));
  animation:borderSpin 4s linear infinite;
}}
@keyframes borderSpin{{ to{{ --border-angle:360deg; }} }}
@property --border-angle{{ syntax:'<angle>'; inherits:false; initial-value:0deg; }}

/* Effect 9 — Reveal stagger */
.reveal-grid{{ display:grid; grid-template-columns:repeat(3,1fr); gap:12px; }}
.reveal-item{{
  height:80px; border-radius:12px; background:var(--cometa-dim);
  border:1px solid rgba(102,51,255,.2); display:flex; align-items:center;
  justify-content:center; font-family:var(--font-m); font-size:.7rem;
  color:var(--cometa); letter-spacing:.1em;
  opacity:0; transform:translateY(16px);
  transition:opacity .5s var(--ease-e), transform .5s var(--ease-e);
}}
.reveal-item.visible{{ opacity:1; transform:none; }}

/* Effect 10 — Count up */
.counters{{ display:flex; gap:40px; flex-wrap:wrap; }}
.counter-item{{ display:flex; flex-direction:column; gap:4px; }}
.counter-num{{ font-family:var(--font-d); font-size:2.8rem; color:var(--cometa); line-height:1; }}
.counter-label{{ font-family:var(--font-m); font-size:.65rem; color:var(--text3); letter-spacing:.12em; text-transform:uppercase; }}

/* Effect 11 — Liquid bg */
.fx-liquid{{
  background:var(--bg2);
  --lx: 50%; --ly: 50%;
}}
.fx-liquid::after{{
  content:''; position:absolute; inset:0; border-radius:20px;
  background:radial-gradient(ellipse 120px 100px at var(--lx) var(--ly), rgba(102,51,255,.25) 0%, transparent 70%);
  pointer-events:none; transition:background .1s;
}}

/* Effect 12 — Chromatic */
.chromatic{{
  font-family:var(--font-d); font-size:2.2rem; color:var(--text);
  cursor:pointer; transition:filter .2s;
  display:inline-block;
}}
.chromatic:hover{{
  filter: drop-shadow(-3px 0 0 rgba(255,0,80,.6)) drop-shadow(3px 0 0 rgba(0,200,255,.6));
  animation:chromShake .15s ease infinite;
}}
@keyframes chromShake{{
  0%,100%{{transform:none}} 50%{{transform:skewX(-1deg)}}
}}

/* ── Icons ───────────────────────────────────────────── */
.icon-toolbar{{
  display:flex; flex-wrap:wrap; gap:12px; align-items:center;
  margin-bottom:24px; padding:20px; background:var(--surface);
  border-radius:16px; border:1px solid var(--border);
}}
.icon-search{{
  flex:1; min-width:200px; padding:10px 16px;
  font-family:var(--font-b); font-size:.9rem; color:var(--text);
  background:var(--bg); border:1.5px solid var(--border); border-radius:9999px;
  outline:none; transition:border-color var(--dur-b), box-shadow var(--dur-b);
}}
.icon-search::placeholder{{ color:var(--text3); }}
.icon-search:focus{{ border-color:var(--cometa); box-shadow:0 0 0 3px rgba(102,51,255,.12); }}
.icon-color-wrap{{ display:flex; align-items:center; gap:8px; }}
.icon-color-label{{ font-family:var(--font-m); font-size:.65rem; color:var(--text3); letter-spacing:.08em; text-transform:uppercase; }}
#icon-color{{ width:32px; height:32px; border-radius:50%; border:2px solid var(--border); background:none; cursor:pointer; padding:0; overflow:hidden; }}
.icon-size-wrap{{ display:flex; align-items:center; gap:8px; }}
.icon-size-label{{ font-family:var(--font-m); font-size:.65rem; color:var(--text3); letter-spacing:.08em; text-transform:uppercase; white-space:nowrap; }}
#icon-size{{ width:90px; padding:8px 12px; font-family:var(--font-m); font-size:.8rem; color:var(--text); background:var(--bg); border:1.5px solid var(--border); border-radius:8px; outline:none; text-align:center; }}
.icon-count{{ font-family:var(--font-m); font-size:.65rem; color:var(--text3); margin-left:auto; }}
.icon-grid{{
  display:grid; grid-template-columns:repeat(auto-fill,minmax(88px,1fr)); gap:8px;
  max-height:520px; overflow-y:auto; padding:4px;
}}
.icon-grid::-webkit-scrollbar{{ width:4px; }}
.icon-grid::-webkit-scrollbar-track{{ background:transparent; }}
.icon-grid::-webkit-scrollbar-thumb{{ background:var(--border2); border-radius:2px; }}
.icon-item{{
  display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px;
  padding:14px 8px; border-radius:14px; border:1px solid transparent;
  cursor:pointer; transition:background var(--dur-b), border-color var(--dur-b), transform var(--dur-f) var(--ease-p);
  position:relative;
}}
.icon-item:hover{{ background:var(--surface); border-color:var(--border2); transform:scale(1.06); }}
.icon-item.selected{{ background:var(--cometa-dim); border-color:rgba(102,51,255,.4); }}
.icon-svg{{ display:block; }}
.icon-name{{ font-family:var(--font-m); font-size:.55rem; color:var(--text3); letter-spacing:.04em; text-align:center; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; width:100%; }}
.icon-actions{{
  margin-top:16px; display:none; flex-wrap:wrap; gap:10px; align-items:center;
  padding:16px; background:var(--surface); border-radius:14px; border:1px solid var(--border);
}}
.icon-actions.show{{ display:flex; }}
.icon-preview{{ display:flex; align-items:center; gap:16px; margin-right:auto; }}
.icon-preview-label{{ font-family:var(--font-m); font-size:.65rem; color:var(--text3); letter-spacing:.08em; text-transform:uppercase; }}
.icon-selected-name{{ font-family:var(--font-b); font-weight:600; font-size:.9rem; color:var(--text); }}

/* ── Tokens ──────────────────────────────────────────── */
.tokens-cols{{ display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:32px; }}
.token-group h3{{ font-family:var(--font-m); font-size:.65rem; color:var(--cometa); letter-spacing:.15em; text-transform:uppercase; margin-bottom:12px; }}
.token-list{{ display:flex; flex-direction:column; gap:2px; }}
.token-row{{
  display:flex; justify-content:space-between; padding:8px 12px;
  border-radius:6px; transition:background var(--dur-b);
}}
.token-row:hover{{ background:var(--surface); }}
.tk{{ font-family:var(--font-m); font-size:.7rem; }}
.tk-k{{ color:var(--text2); }} .tk-v{{ color:var(--text); }}

/* ── ASCII Studio ───────────────────────────────────── */
.studio-layout{{ display:grid; grid-template-columns:1fr 340px; gap:24px; align-items:start; }}
@media(max-width:900px){{ .studio-layout{{ grid-template-columns:1fr; }} }}
.studio-canvas-wrap{{
  position:relative; border-radius:20px; overflow:hidden;
  border:1px solid var(--border); background:#000; aspect-ratio:16/9;
  display:flex; align-items:center; justify-content:center;
}}
#studio-canvas{{ display:block; max-width:100%; max-height:100%; cursor:none; }}
.studio-drop{{
  position:absolute; inset:0; display:flex; flex-direction:column;
  align-items:center; justify-content:center; gap:12px; cursor:pointer;
  transition:background var(--dur-b);
}}
.studio-drop.hidden{{ display:none; }}
.studio-drop-icon{{ font-size:2.5rem; opacity:.4; }}
.studio-drop-text{{ font-family:var(--font-m); font-size:.75rem; color:var(--text2); letter-spacing:.08em; text-align:center; }}
.studio-drop:hover{{ background:var(--surface); }}
.studio-panel{{
  display:flex; flex-direction:column; gap:12px;
}}
.studio-ctrl{{ display:flex; flex-direction:column; gap:6px; }}
.studio-ctrl label{{ font-family:var(--font-m); font-size:.65rem; color:var(--text3); letter-spacing:.1em; text-transform:uppercase; display:flex; justify-content:space-between; }}
.studio-ctrl input[type=range]{{ width:100%; accent-color:var(--cometa); }}
.studio-ctrl input[type=text]{{ width:100%; padding:7px 12px; border-radius:8px; border:1px solid var(--border2); background:var(--bg2); color:var(--text); font-family:var(--font-m); font-size:.8rem; outline:none; }}
.studio-ctrl input[type=text]:focus{{ border-color:var(--cometa); }}
.studio-export{{ display:flex; gap:8px; margin-top:4px; }}
.studio-export .btn{{ flex:1; justify-content:center; }}

/* ── GSAP Gallery ───────────────────────────────────── */
.gsap-grid{{ display:grid; grid-template-columns:repeat(auto-fill,minmax(320px,1fr)); gap:16px; }}
.gsap-card{{
  border-radius:20px; overflow:hidden; border:1px solid var(--border);
  background:var(--bg2); display:flex; flex-direction:column;
}}
.gsap-stage{{
  height:220px; display:flex; align-items:center; justify-content:center;
  position:relative; overflow:hidden; background:var(--bg);
  flex-shrink:0; cursor:default;
}}
.gsap-footer{{
  padding:16px 20px; display:flex; align-items:center; justify-content:space-between;
  border-top:1px solid var(--border);
}}
.gsap-name{{ font-family:var(--font-m); font-size:.7rem; color:var(--text2); letter-spacing:.08em; text-transform:uppercase; }}
.gsap-replay{{
  padding:5px 14px; font-family:var(--font-m); font-size:.65rem; font-weight:600;
  letter-spacing:.08em; text-transform:uppercase; border-radius:9999px;
  border:1px solid var(--border2); background:transparent; color:var(--text2);
  cursor:pointer; transition:all var(--dur-b);
}}
.gsap-replay:hover{{ background:var(--cometa); color:#fff; border-color:var(--cometa); }}
</style>
</head>
<body>

<!-- Loader -->
<div id="loader">
  <div style="width:56px;opacity:.6">{logo_sym}</div>
  <div class="l-bar"></div>
</div>

<!-- Cursor -->
<div id="cursor"></div>

<!-- Nav -->
<nav>
  <div class="wrap nav-inner">
    <a href="#" class="nav-logo" id="nav-logo-el">{logo_neg}</a>
    <ul class="nav-links">
      <li><a href="#cores">Cores</a></li>
      <li><a href="#tipo">Tipo</a></li>
      <li><a href="#logos">Logos</a></li>
      <li><a href="#comps">Comps</a></li>
      <li><a href="#efeitos">Efeitos</a></li>
      <li><a href="#icones">Ícones</a></li>
      <li><a href="#studio">Studio</a></li>
      <li><a href="#gsap">GSAP</a></li>
      <li>
        <button id="theme-btn" title="Alternar tema">
          <svg viewBox="0 0 24 24" id="theme-icon"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        </button>
      </li>
    </ul>
  </div>
</nav>

<!-- ── Hero ───────────────────────────────────────────── -->
<section class="hero">
  <div class="hero-top wrap-wide">
    <div class="hero-top-l">
      <span>8D Hubify ✦ Design System</span>
      <span><em>v3.0</em> — Edição 2025</span>
    </div>
    <div class="hero-top-r">
      <span class="pulse">Status: Live</span>
      <span>SP / BR ↘ 22°C</span>
    </div>
  </div>

  <div class="hero-center wrap-wide">
    <div class="hero-headline">
      <span class="hero-kicker">Fundação Visual da Agência</span>
      <h1 class="hero-h1">
        <span class="line"><span>Design</span></span>
        <span class="line"><span>do <em>Cosmos</em></span></span>
        <span class="line"><span>Digital.</span></span>
      </h1>
      <p class="hero-lede">
        Um sistema vivo de cores, tipografia, componentes e movimento.
        Construído para escalar a presença da 8D Hubify do pixel ao planeta.
      </p>
      <div class="hero-cta-row">
        <span class="mag-wrap"><a class="btn btn-primary btn-lg" href="#cores">Explorar Sistema →</a></span>
        <span class="mag-wrap"><a class="btn btn-ghost btn-lg" href="#studio">ASCII Studio</a></span>
      </div>
    </div>
    <div class="hero-ascii-col">
      <div class="ascii-hero-wrap">
        <canvas id="ascii-canvas"></canvas>
      </div>
    </div>
  </div>

  <div class="hero-bottom wrap-wide">
    <div class="hero-stat"><div class="hero-stat-num"><em>06</em></div><div class="hero-stat-label">Cores Base</div></div>
    <div class="hero-stat"><div class="hero-stat-num"><em>09</em></div><div class="hero-stat-label">Pesos de Tipo</div></div>
    <div class="hero-stat"><div class="hero-stat-num"><em>86</em></div><div class="hero-stat-label">Ícones</div></div>
    <div class="hero-stat"><div class="hero-stat-num"><em>∞</em></div><div class="hero-stat-label">Movimentos</div></div>
  </div>
</section>

<!-- ── Marquee ─────────────────────────────────────── -->
<div class="marquee">
  <div class="marquee-track">
    <span>AGÊNCIA <em>✦</em> COMETA <em>✦</em> GALÁXIA <em>✦</em> VIA LÁCTEA <em>✦</em> INTERESTELAR <em>✦</em> NUVEM <em>✦</em> SOLAR <em>✦</em></span>
    <span>AGÊNCIA <em>✦</em> COMETA <em>✦</em> GALÁXIA <em>✦</em> VIA LÁCTEA <em>✦</em> INTERESTELAR <em>✦</em> NUVEM <em>✦</em> SOLAR <em>✦</em></span>
  </div>
</div>

<!-- ── 01 Cores ───────────────────────────────────────── -->
<section class="section" id="cores">
  <div class="wrap">
    <div class="section-head">
      <span class="section-num">01</span>
      <span class="section-eyebrow">Capítulo 01 / Paleta</span>
      <h2 class="section-title">Cores do <em>Cosmos</em>.</h2>
      <p class="section-desc">Seis tons que orbitam a identidade da 8D Hubify — do violeta cometa ao branco solar. Cada cor tem uma função clara no sistema.</p>
    </div>
    <!-- Featured: Cometa -->
    <div class="color-feature">
      <div class="color-feature-swatch">
        <div class="color-feature-num">01 / Cor primária</div>
        <div>
          <div class="color-feature-name">Cometa</div>
          <div class="color-feature-hex" style="margin-top:10px">#6633FF</div>
        </div>
        <div></div>
      </div>
      <div class="color-feature-meta">
        <h4>Sobre essa cor</h4>
        <p>Violeta vibrante. A assinatura da marca. Usada em CTAs, links, destaques e qualquer momento de protagonismo na interface.</p>
        <div class="color-feature-vals">
          <div class="color-val"><span class="color-val-k">HEX</span><span class="color-val-v">#6633FF</span></div>
          <div class="color-val"><span class="color-val-k">RGB</span><span class="color-val-v">102 51 255</span></div>
          <div class="color-val"><span class="color-val-k">HSL</span><span class="color-val-v">252° 100% 60%</span></div>
          <div class="color-val"><span class="color-val-k">Contraste</span><span class="color-val-v">AAA</span></div>
        </div>
      </div>
    </div>

    <div class="color-grid">
      <div class="color-chip">
        <div class="color-swatch" style="background:#000033"><span class="color-swatch-tag">Background</span></div>
        <div class="color-meta"><div class="color-name">Galáxia</div><div class="color-role">Fundo Principal</div><div class="color-hex">#000033</div></div>
      </div>
      <div class="color-chip">
        <div class="color-swatch" style="background:#DADBFD"><span class="color-swatch-tag dark">Tint</span></div>
        <div class="color-meta"><div class="color-name">Via Láctea</div><div class="color-role">Luz Suave</div><div class="color-hex">#DADBFD</div></div>
      </div>
      <div class="color-chip">
        <div class="color-swatch" style="background:#FFCE44"><span class="color-swatch-tag dark">Accent</span></div>
        <div class="color-meta"><div class="color-name">Interestelar</div><div class="color-role">Destaque Quente</div><div class="color-hex">#FFCE44</div></div>
      </div>
      <div class="color-chip">
        <div class="color-swatch" style="background:#ED694B"><span class="color-swatch-tag">Accent</span></div>
        <div class="color-meta"><div class="color-name">Nuvem</div><div class="color-role">Energia / Erro</div><div class="color-hex">#ED694B</div></div>
      </div>
      <div class="color-chip">
        <div class="color-swatch" style="background:#FFFFFF;box-shadow:inset 0 0 0 1px rgba(0,0,0,.08)"><span class="color-swatch-tag dark">Neutral</span></div>
        <div class="color-meta"><div class="color-name">Solar</div><div class="color-role">Branco Base</div><div class="color-hex">#FFFFFF</div></div>
      </div>
    </div>

    <!-- Pairings -->
    <div class="pairings">
      <div class="pair"><span class="pair-label">Cometa × Galáxia</span><div style="background:#6633FF"></div><div style="background:#000033"></div></div>
      <div class="pair"><span class="pair-label">Cometa × Solar</span><div style="background:#6633FF"></div><div style="background:#FFFFFF"></div></div>
      <div class="pair"><span class="pair-label">Interestelar × Galáxia</span><div style="background:#FFCE44"></div><div style="background:#000033"></div></div>
      <div class="pair"><span class="pair-label">Nuvem × Via Láctea</span><div style="background:#ED694B"></div><div style="background:#DADBFD"></div></div>
    </div>
  </div>
</section>

<!-- ── 02 Tipografia ──────────────────────────────────── -->
<section class="section" id="tipo">
  <div class="wrap">
    <div class="section-head">
      <span class="section-num">02</span>
      <span class="section-eyebrow">Capítulo 02 / Tipografia</span>
      <h2 class="section-title">Hugein <em>×</em> Henju.</h2>
      <p class="section-desc">Display serif para impacto editorial, sans variable para corpo. Um par tipográfico construído para escalar.</p>
    </div>
    <!-- Specimens -->
    <div class="type-specimens">
      <div class="type-specimen">
        <div class="type-specimen-tag">Display Serif</div>
        <div class="type-specimen-Aa">Aa</div>
        <div>
          <div class="type-specimen-name">Hugein</div>
          <div class="type-specimen-meta">
            <div>WEIGHT<b>400 regular</b></div>
            <div>USO<b>Headlines, hero, números</b></div>
          </div>
        </div>
      </div>
      <div class="type-specimen">
        <div class="type-specimen-tag">Variable Sans</div>
        <div class="type-specimen-Aa henju">Aa</div>
        <div>
          <div class="type-specimen-name">Henju Sans</div>
          <div class="type-specimen-meta">
            <div>WEIGHT<b>100 — 900 variable</b></div>
            <div>USO<b>Corpo, UI, labels</b></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Scale -->
    <div class="type-scale">
      <div class="type-row">
        <div class="type-meta"><b>Hero</b>Hugein 400<br>clamp(3–6rem)</div>
        <div style="font-family:var(--font-d);font-size:clamp(3rem,7vw,6rem);font-weight:400;line-height:.9;letter-spacing:-.03em;color:var(--text)">Cometa</div>
      </div>
      <div class="type-row">
        <div class="type-meta"><b>H1</b>Hugein 400<br>3.8rem</div>
        <div style="font-family:var(--font-d);font-size:clamp(2.4rem,5vw,3.8rem);font-weight:400;letter-spacing:-.02em;color:var(--text)">Via Láctea</div>
      </div>
      <div class="type-row">
        <div class="type-meta"><b>H2</b>Hugein 400<br>3rem</div>
        <div style="font-family:var(--font-d);font-size:clamp(1.8rem,4vw,3rem);font-weight:400;letter-spacing:-.01em;color:var(--text)">8D Hubify</div>
      </div>
      <div class="type-row">
        <div class="type-meta"><b>H3</b>Henju 700<br>2rem</div>
        <div style="font-family:var(--font-b);font-size:clamp(1.4rem,3vw,2rem);font-weight:700;font-style:normal;color:var(--text)">Interestelar</div>
      </div>
      <div class="type-row">
        <div class="type-meta"><b>Lead</b>Henju 300<br>1.1rem</div>
        <div style="font-family:var(--font-b);font-size:1.1rem;font-weight:300;font-style:normal;color:var(--text2);line-height:1.6">Conectamos marcas ao cosmos digital com estratégia, dados e criatividade.</div>
      </div>
      <div class="type-row">
        <div class="type-meta"><b>Body</b>Henju 400<br>1rem</div>
        <div style="font-family:var(--font-b);font-size:1rem;font-weight:400;font-style:normal;color:var(--text2);line-height:1.7">A 8D Hubify é especialista em tráfego pago, automação e performance de marketing digital.</div>
      </div>
      <div class="type-row">
        <div class="type-meta"><b>Label</b>Mono 600<br>.7rem</div>
        <div style="font-family:var(--font-m);font-size:.7rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--cometa)">Design System — v3.0</div>
      </div>
    </div>

    <!-- Pangram -->
    <div class="pangram">
      <div class="pangram-tag">Pangram em Hugein</div>
      <div class="pangram-text">Mil novas galáxias surgem no horizonte digital. Conectamos marcas ao cosmos da performance.</div>
    </div>

    <!-- Weights -->
    <div class="weights-demo">
      <div class="weights-head">Pesos — Henju Sans Variable</div>
      {''.join(f'<div class="weight-row"><span class="weight-num">{w}</span><span class="weight-text" style="font-weight:{w}">8D Hubify Agência Digital</span></div>' for w in [100,200,300,400,500,600,700,800,900])}
    </div>
  </div>
</section>

<!-- ── 03 Logos ────────────────────────────────────────── -->
<section class="section" id="logos">
  <div class="wrap">
    <div class="section-head">
      <span class="section-num">03</span>
      <span class="section-eyebrow">Capítulo 03 / Marca</span>
      <h2 class="section-title">Identidade <em>aplicada</em>.</h2>
      <p class="section-desc">Seis variações para qualquer contexto: claro, escuro, vertical, horizontal e símbolo isolado.</p>
    </div>
    <!-- Featured logo -->
    <div class="logo-feature">
      <div class="logo-feature-display">{logo_neg}</div>
      <div class="logo-feature-info">
        <h4>Logo Principal</h4>
        <div class="name">8D Hubify</div>
        <p>A versão completa da marca em sua aplicação primária. Use em fundos escuros, materiais institucionais, capas e cabeçalhos.</p>
        <div class="logo-feature-rules">
          <div class="logo-rule">Mínimo 32px de altura digital</div>
          <div class="logo-rule">Margem livre = altura do símbolo</div>
          <div class="logo-rule">Sempre em escala proporcional</div>
        </div>
      </div>
    </div>

    <div class="logo-grid">
      <div class="logo-card on-light">{logo_pos}<span class="logo-label">Positiva</span></div>
      <div class="logo-card on-dark">{logo_h_neg}<span class="logo-label">Horizontal Negativa</span></div>
      <div class="logo-card on-light">{logo_h_pos}<span class="logo-label">Horizontal Positiva</span></div>
      <div class="logo-card on-surface">{logo_sym}<span class="logo-label">Símbolo</span></div>
      <div class="logo-card on-dark">{logo_sym_n}<span class="logo-label">Símbolo Negativo</span></div>
    </div>
  </div>
</section>

<!-- ── 04 Componentes ─────────────────────────────────── -->
<section class="section" id="comps">
  <div class="wrap">
    <div class="section-head">
      <span class="section-num">04</span>
      <span class="section-eyebrow">Capítulo 04 / Sistema</span>
      <h2 class="section-title">Componentes <em>vivos</em>.</h2>
      <p class="section-desc">Botões, badges, cards e inputs com hover states reais. Tudo construído com CSS custom properties para temas claros e escuros.</p>
    </div>
    <div class="comp-group">
      <div class="comp-label">Botões</div>
      <div class="comp-row">
        <div class="mag-wrap"><button class="btn btn-primary">Primary</button></div>
        <div class="mag-wrap"><button class="btn btn-secondary">Secondary</button></div>
        <div class="mag-wrap"><button class="btn btn-ghost">Ghost</button></div>
        <div class="mag-wrap"><button class="btn btn-warm">Warm</button></div>
      </div>
      <div class="comp-row" style="margin-top:10px">
        <button class="btn btn-primary btn-sm">Small</button>
        <button class="btn btn-primary">Default</button>
        <button class="btn btn-primary btn-lg">Large</button>
      </div>
    </div>
    <div class="comp-group">
      <div class="comp-label">Badges</div>
      <div class="comp-row">
        <span class="badge badge-cometa">Cometa</span>
        <span class="badge badge-solar">Solar</span>
        <span class="badge badge-warm">Interestelar</span>
        <span class="badge badge-coral">Nuvem</span>
        <span class="badge badge-new">Novo</span>
      </div>
    </div>
    <div class="comp-group">
      <div class="comp-label">Cards</div>
      <div class="card-grid">
        <div class="card card-dark">
          <div class="card-tag">Performance</div>
          <div class="card-title">Tráfego Pago</div>
          <div class="card-body">Gestão avançada de campanhas em Meta, Google e DSPs.</div>
        </div>
        <div class="card card-accent">
          <div class="card-tag" style="color:rgba(255,255,255,.5)">Destaque</div>
          <div class="card-title" style="color:#fff">Automação</div>
          <div class="card-body" style="color:rgba(255,255,255,.7)">Fluxos inteligentes que trabalham enquanto você dorme.</div>
        </div>
        <div class="card card-glass">
          <div class="card-tag">Glass</div>
          <div class="card-title">Estratégia</div>
          <div class="card-body">Planejamento orientado a dados para crescimento.</div>
        </div>
        <div class="card card-warm">
          <div class="card-tag">Warm</div>
          <div class="card-title">Conteúdo</div>
          <div class="card-body">Narrativas que constroem autoridade de marca.</div>
        </div>
      </div>
    </div>
    <div class="comp-group">
      <div class="comp-label">Inputs</div>
      <div class="comp-row" style="gap:20px">
        <div style="flex:1;min-width:220px;display:flex;flex-direction:column;gap:6px">
          <label class="input-label">Email</label>
          <input class="input" type="email" placeholder="seu@email.com">
        </div>
        <div style="flex:1;min-width:220px;display:flex;flex-direction:column;gap:6px">
          <label class="input-label">Empresa</label>
          <input class="input" type="text" placeholder="Nome da empresa">
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ── 05 Efeitos ─────────────────────────────────────── -->
<section class="section" id="efeitos">
  <div class="wrap">
    <div class="section-head">
      <span class="section-num">05</span>
      <span class="section-eyebrow">Capítulo 05 / Motion</span>
      <h2 class="section-title">Efeitos em <em>tempo real</em>.</h2>
      <p class="section-desc">Doze interações modernas — spotlight, parallax tilt, ASCII rain, glitch, chromatic split, liquid cursor — todas em vanilla JS.</p>
    </div>
    <div class="effects-grid">

      <!-- 01 Gradient Mesh -->
      <div class="effect-card fx-mesh">
        <div class="effect-label">01 — Gradient Mesh</div>
        <div class="effect-title">Fundo animado multi-cor</div>
      </div>

      <!-- 02 Morphing Blob -->
      <div class="effect-card fx-blob">
        <div class="blob-shape"></div>
        <div class="effect-label">02 — Morphing Blob</div>
        <div class="effect-title">Forma orgânica em loop</div>
      </div>

      <!-- 03 Marquee ticker -->
      <div class="effect-card fx-marquee" style="grid-column:span 2">
        <div class="marquee-track" id="marquee-track">
          <div class="marquee-item">Performance <span class="marquee-dot"></span></div>
          <div class="marquee-item">Automação <span class="marquee-dot"></span></div>
          <div class="marquee-item">Estratégia <span class="marquee-dot"></span></div>
          <div class="marquee-item">Dados <span class="marquee-dot"></span></div>
          <div class="marquee-item">Criatividade <span class="marquee-dot"></span></div>
          <div class="marquee-item">Performance <span class="marquee-dot"></span></div>
          <div class="marquee-item">Automação <span class="marquee-dot"></span></div>
          <div class="marquee-item">Estratégia <span class="marquee-dot"></span></div>
          <div class="marquee-item">Dados <span class="marquee-dot"></span></div>
          <div class="marquee-item">Criatividade <span class="marquee-dot"></span></div>
        </div>
        <div class="effect-label" style="padding:0 32px 24px">03 — Marquee</div>
      </div>

      <!-- 04 Spotlight -->
      <div class="effect-card fx-spotlight" id="fx-spotlight"
           style="background:var(--bg2);cursor:crosshair">
        <div class="spotlight-hole" id="spotlight-hole"></div>
        <div class="effect-label" style="position:relative">04 — Spotlight</div>
        <div class="effect-title" style="position:relative">Mova o mouse aqui</div>
      </div>

      <!-- 05 Glitch -->
      <div class="effect-card" style="background:var(--bg2)">
        <div class="glitch" data-text="8D Hubify">8D Hubify</div>
        <div class="effect-label" style="margin-top:auto">05 — Glitch Text</div>
        <div class="effect-title">Distorção cromática em loop</div>
      </div>

      <!-- 06 Parallax tilt -->
      <div class="effect-card fx-tilt" id="fx-tilt"
           style="background:linear-gradient(135deg,var(--cometa),#2200cc);cursor:pointer">
        <div class="tilt-shine" id="tilt-shine"></div>
        <div class="tilt-inner" id="tilt-inner">
          <div class="effect-label" style="color:rgba(255,255,255,.6)">06 — Parallax Tilt</div>
          <div class="effect-title" style="color:#fff">Hover com perspectiva 3D</div>
        </div>
      </div>

      <!-- 07 Scramble -->
      <div class="effect-card" style="background:var(--bg2)">
        <div class="scramble" id="scramble-el" data-text="DESIGN SYSTEM" title="Clique para scramble">DESIGN SYSTEM</div>
        <div class="effect-label" style="margin-top:auto">07 — Scramble Text</div>
        <div class="effect-title">Clique para embaralhar</div>
      </div>

      <!-- 08 Gradient Border -->
      <div class="fx-gborder">
        <div class="effect-label">08 — Gradient Border</div>
        <div class="effect-title">Borda conica giratória</div>
      </div>

      <!-- 09 Reveal Stagger -->
      <div class="effect-card" style="background:var(--bg2);display:block;min-height:auto">
        <div class="reveal-grid" id="reveal-grid">
          <div class="reveal-item">01</div><div class="reveal-item">02</div><div class="reveal-item">03</div>
          <div class="reveal-item">04</div><div class="reveal-item">05</div><div class="reveal-item">06</div>
        </div>
        <div style="margin-top:16px">
          <div class="effect-label">09 — Stagger Reveal</div>
          <div class="effect-title">Animação em cascata</div>
        </div>
      </div>

      <!-- 10 Counters -->
      <div class="effect-card" style="background:var(--bg2)">
        <div class="counters" id="counters">
          <div class="counter-item"><div class="counter-num" data-target="320">0</div><div class="counter-label">Clientes</div></div>
          <div class="counter-item"><div class="counter-num" data-target="98">0</div><div class="counter-label">NPS</div></div>
          <div class="counter-item"><div class="counter-num" data-target="12">0</div><div class="counter-label">Anos</div></div>
        </div>
        <div class="effect-label" style="margin-top:auto">10 — Count Up</div>
        <div class="effect-title">Scroll aciona contagem</div>
      </div>

      <!-- 11 Liquid cursor -->
      <div class="effect-card fx-liquid" id="fx-liquid">
        <div class="effect-label">11 — Liquid Cursor</div>
        <div class="effect-title">Luz segue o ponteiro</div>
      </div>

      <!-- 12 Chromatic -->
      <div class="effect-card" style="background:var(--bg2)">
        <div class="chromatic">Agência</div>
        <div class="effect-label" style="margin-top:auto">12 — Chromatic Split</div>
        <div class="effect-title">Aberração cromática no hover</div>
      </div>

    </div>
  </div>
</section>

<!-- ── 06 Ícones ──────────────────────────────────────── -->
<section class="section" id="icones">
  <div class="wrap">
    <div class="section-head">
      <span class="section-num">06</span>
      <span class="section-eyebrow">Capítulo 06 / Ícones</span>
      <h2 class="section-title">Biblioteca <em>customizável</em>.</h2>
      <p class="section-desc">86 ícones em estilo Lucide. Busque, ajuste cor e tamanho, baixe em SVG ou PNG em qualquer resolução.</p>
    </div>
    <div class="icon-toolbar">
      <input class="icon-search" type="search" id="icon-search" placeholder="Buscar ícone..." autocomplete="off">
      <div class="icon-color-wrap">
        <span class="icon-color-label">Cor</span>
        <input type="color" id="icon-color" value="#6633FF">
      </div>
      <div class="icon-size-wrap">
        <span class="icon-size-label">Tamanho (px)</span>
        <input class="input" id="icon-size" type="number" value="24" min="8" max="512" style="padding:8px 12px;border-radius:8px;font-family:var(--font-m);font-size:.8rem;width:80px">
      </div>
      <span class="icon-count" id="icon-count"></span>
    </div>
    <div class="icon-actions" id="icon-actions">
      <div class="icon-preview">
        <svg id="icon-preview-svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke-linecap="round" stroke-linejoin="round"></svg>
        <div>
          <div class="icon-preview-label">Selecionado</div>
          <div class="icon-selected-name" id="icon-selected-name">—</div>
        </div>
      </div>
      <button class="btn btn-secondary btn-sm" onclick="downloadSVG()">↓ SVG</button>
      <button class="btn btn-primary btn-sm" onclick="downloadPNG()">↓ PNG</button>
    </div>
    <div class="icon-grid" id="icon-grid"></div>
  </div>
</section>

<!-- ── 07 Tokens ──────────────────────────────────────── -->
<section class="section" id="tokens">
  <div class="wrap">
    <div class="section-head">
      <span class="section-num">07</span>
      <span class="section-eyebrow">Capítulo 07 / Tokens</span>
      <h2 class="section-title">Tokens de <em>design</em>.</h2>
      <p class="section-desc">Espaçamento, escala tipográfica, raios e easings — toda a fundação técnica do sistema em variáveis CSS.</p>
    </div>
    <div class="tokens-cols">
      <div class="token-group">
        <h3>Espaçamento</h3>
        <div class="token-list">
          {''.join(f'<div class="token-row"><span class="tk tk-k">--space-{k}</span><span class="tk tk-v">{v}px</span></div>' for k,v in [(1,4),(2,8),(3,12),(4,16),(5,20),(6,24),(8,32),(10,40),(12,48),(16,64),(20,80),(24,96),(32,128)])}
        </div>
      </div>
      <div class="token-group">
        <h3>Escala Tipográfica</h3>
        <div class="token-list">
          {''.join(f'<div class="token-row"><span class="tk tk-k">--text-{k}</span><span class="tk tk-v">{v}</span></div>' for k,v in [('xs','.75rem'),('sm','.875rem'),('base','1rem'),('lg','1.25rem'),('xl','1.563rem'),('2xl','1.953rem'),('3xl','2.441rem'),('4xl','3.052rem'),('5xl','3.815rem'),('hero','6rem')])}
        </div>
      </div>
      <div class="token-group">
        <h3>Border Radius</h3>
        <div class="token-list">
          {''.join(f'<div class="token-row"><span class="tk tk-k">--radius-{k}</span><span class="tk tk-v">{v}</span></div>' for k,v in [('sm','4px'),('md','8px'),('lg','16px'),('xl','24px'),('2xl','32px'),('full','9999px')])}
        </div>
      </div>
      <div class="token-group">
        <h3>Easings</h3>
        <div class="token-list">
          {''.join(f'<div class="token-row"><span class="tk tk-k">{k}</span><span class="tk tk-v" style="font-size:.62rem">{v}</span></div>' for k,v in [('--ease-s','cubic-bezier(.25,.46,.45,.94)'),('--ease-p','cubic-bezier(.34,1.56,.64,1)'),('--ease-e','cubic-bezier(.16,1,.3,1)')])}
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ── 08 ASCII Art Studio ─────────────────────────────── -->
<section class="section" id="studio">
  <div class="wrap">
    <div class="section-head">
      <span class="section-num">08</span>
      <span class="section-eyebrow">Capítulo 08 / Studio</span>
      <h2 class="section-title">ASCII <em>Studio</em>.</h2>
      <p class="section-desc">Transforme qualquer imagem, vídeo ou modelo 3D em arte ASCII interativa. Mova o mouse, ajuste parâmetros e exporte pronto para a web.</p>
    </div>
    <div class="studio-layout">
      <div class="studio-canvas-wrap" id="studio-drop-zone">
        <canvas id="studio-canvas"></canvas>
        <div class="studio-drop" id="studio-drop-overlay">
          <div class="studio-drop-icon">✦</div>
          <div class="studio-drop-text">Arraste imagem, vídeo ou arquivo .OBJ<br><span style="opacity:.5">ou clique para selecionar</span></div>
        </div>
        <input type="file" id="studio-file-input" accept="image/*,video/*,.obj" style="display:none">
      </div>
      <div class="studio-panel">
        <div class="studio-ctrl">
          <label>Charset <span id="studio-charset-val"></span></label>
          <input type="text" id="studio-charset" value="█8DHubify✦ ">
        </div>
        <div class="studio-ctrl">
          <label>Font Size <span id="studio-fs-val">12</span>px</label>
          <input type="range" id="studio-fontsize" min="6" max="24" value="12" step="1">
        </div>
        <div class="studio-ctrl">
          <label>Detail <span id="studio-detail-val">50</span></label>
          <input type="range" id="studio-detail" min="10" max="100" value="50" step="5">
        </div>
        <div class="studio-ctrl">
          <label>Mouse Radius <span id="studio-radius-val">50</span>px</label>
          <input type="range" id="studio-radius" min="0" max="120" value="50" step="5">
        </div>
        <div class="studio-ctrl">
          <label>Contraste <span id="studio-contrast-val">100</span>%</label>
          <input type="range" id="studio-contrast" min="50" max="200" value="100" step="5">
        </div>
        <div class="studio-ctrl">
          <label>Brilho <span id="studio-brightness-val">100</span>%</label>
          <input type="range" id="studio-brightness" min="50" max="200" value="100" step="5">
        </div>
        <div class="studio-export">
          <button class="btn btn-secondary btn-sm" id="studio-export-png">↓ PNG</button>
          <button class="btn btn-primary btn-sm" id="studio-export-svg">↓ SVG Texto</button>
        </div>
        <p style="font-family:var(--font-m);font-size:.6rem;color:var(--text3);line-height:1.6">
          Mova o mouse no canvas para repelir os caracteres.<br>
          Suporta imagem (JPG/PNG/GIF), vídeo (MP4/WebM) e modelo 3D (.OBJ).
        </p>
      </div>
    </div>
  </div>
</section>

<!-- ── 09 GSAP Gallery ────────────────────────────────── -->
<section class="section" id="gsap">
  <div class="wrap">
    <div class="section-head">
      <span class="section-num">09</span>
      <span class="section-eyebrow">Capítulo 09 / Galeria</span>
      <h2 class="section-title">Animações <em>GSAP</em>.</h2>
      <p class="section-desc">Dez demos para uso real no produto. Cada animação é replayable e copy-pasteable.</p>
    </div>
    <div class="gsap-grid" id="gsap-grid">

      <!-- 1 Text Reveal -->
      <div class="gsap-card">
        <div class="gsap-stage" id="g1-stage">
          <div id="g1-text" style="font-family:var(--font-d);font-size:3rem;font-weight:400;color:var(--text);overflow:hidden;clip-path:inset(0)">
            <span id="g1-a" style="display:inline-block">8D</span><span id="g1-b" style="display:inline-block"> Hubify</span>
          </div>
        </div>
        <div class="gsap-footer"><span class="gsap-name">01 — Text Reveal</span><button class="gsap-replay" data-anim="1">Replay</button></div>
      </div>

      <!-- 2 Stagger Grid -->
      <div class="gsap-card">
        <div class="gsap-stage" id="g2-stage">
          <div id="g2-grid" style="display:grid;grid-template-columns:repeat(4,44px);gap:8px">
            {''.join(f'<div class="g2-item" style="width:44px;height:44px;border-radius:10px;background:var(--cometa);opacity:0;transform:scale(0)"></div>' for _ in range(8))}
          </div>
        </div>
        <div class="gsap-footer"><span class="gsap-name">02 — Stagger Grid</span><button class="gsap-replay" data-anim="2">Replay</button></div>
      </div>

      <!-- 3 Scroll Counter (runs once on view) -->
      <div class="gsap-card">
        <div class="gsap-stage" id="g3-stage">
          <div style="text-align:center">
            <div id="g3-num" style="font-family:var(--font-d);font-size:4rem;font-weight:400;color:var(--cometa)">0</div>
            <div style="font-family:var(--font-m);font-size:.65rem;color:var(--text3);letter-spacing:.15em">CLIENTES</div>
          </div>
        </div>
        <div class="gsap-footer"><span class="gsap-name">03 — Counter GSAP</span><button class="gsap-replay" data-anim="3">Replay</button></div>
      </div>

      <!-- 4 Elastic Scale -->
      <div class="gsap-card">
        <div class="gsap-stage" id="g4-stage">
          <div id="g4-box" style="width:80px;height:80px;border-radius:20px;background:linear-gradient(135deg,var(--cometa),var(--nuvem));transform:scale(0)"></div>
        </div>
        <div class="gsap-footer"><span class="gsap-name">04 — Elastic Scale</span><button class="gsap-replay" data-anim="4">Replay</button></div>
      </div>

      <!-- 5 Path Draw SVG -->
      <div class="gsap-card">
        <div class="gsap-stage" id="g5-stage">
          <svg width="200" height="100" viewBox="0 0 200 100" fill="none">
            <path id="g5-path" d="M10,90 C40,10 80,80 100,50 S160,20 190,50" stroke="var(--cometa)" stroke-width="3" stroke-linecap="round" fill="none" stroke-dasharray="300" stroke-dashoffset="300"/>
          </svg>
        </div>
        <div class="gsap-footer"><span class="gsap-name">05 — SVG Path Draw</span><button class="gsap-replay" data-anim="5">Replay</button></div>
      </div>

      <!-- 6 Flip Card -->
      <div class="gsap-card">
        <div class="gsap-stage" id="g6-stage">
          <div id="g6-card" style="width:120px;height:80px;border-radius:14px;background:var(--cometa);display:flex;align-items:center;justify-content:center;font-family:var(--font-d);font-size:1.4rem;color:#fff">8D</div>
        </div>
        <div class="gsap-footer"><span class="gsap-name">06 — 3D Flip</span><button class="gsap-replay" data-anim="6">Replay</button></div>
      </div>

      <!-- 7 Morph Color -->
      <div class="gsap-card">
        <div class="gsap-stage" id="g7-stage">
          <div id="g7-orb" style="width:100px;height:100px;border-radius:50%;background:var(--cometa)"></div>
        </div>
        <div class="gsap-footer"><span class="gsap-name">07 — Morph Color</span><button class="gsap-replay" data-anim="7">Replay</button></div>
      </div>

      <!-- 8 Timeline Sequence -->
      <div class="gsap-card">
        <div class="gsap-stage" id="g8-stage">
          <div style="display:flex;flex-direction:column;gap:10px;width:200px">
            <div id="g8-a" style="height:8px;border-radius:4px;background:var(--cometa);transform-origin:left;transform:scaleX(0)"></div>
            <div id="g8-b" style="height:8px;border-radius:4px;background:var(--interestelar);transform-origin:left;transform:scaleX(0)"></div>
            <div id="g8-c" style="height:8px;border-radius:4px;background:var(--nuvem);transform-origin:left;transform:scaleX(0)"></div>
          </div>
        </div>
        <div class="gsap-footer"><span class="gsap-name">08 — Timeline</span><button class="gsap-replay" data-anim="8">Replay</button></div>
      </div>

      <!-- 9 Scramble Text (GSAP) -->
      <div class="gsap-card">
        <div class="gsap-stage" id="g9-stage">
          <div id="g9-text" style="font-family:var(--font-d);font-size:1.8rem;font-weight:400;color:var(--text);text-align:center">Hubify</div>
        </div>
        <div class="gsap-footer"><span class="gsap-name">09 — Scramble Text</span><button class="gsap-replay" data-anim="9">Replay</button></div>
      </div>

      <!-- 10 Particle Burst -->
      <div class="gsap-card">
        <div class="gsap-stage" id="g10-stage" style="cursor:pointer">
          <div id="g10-particles" style="position:relative;width:200px;height:180px"></div>
          <div style="position:absolute;font-family:var(--font-m);font-size:.6rem;color:var(--text3);bottom:12px;letter-spacing:.1em">CLIQUE PARA EXPLODIR</div>
        </div>
        <div class="gsap-footer"><span class="gsap-name">10 — Particle Burst</span><button class="gsap-replay" data-anim="10">Replay</button></div>
      </div>

    </div>
  </div>
</section>

<!-- ── Outro marquee ─────────────────────────────────── -->
<div class="marquee">
  <div class="marquee-track">
    <span>DESIGN <em>✦</em> SYSTEM <em>✦</em> 8D HUBIFY <em>✦</em> v3.0 <em>✦</em> 2025 <em>✦</em></span>
    <span>DESIGN <em>✦</em> SYSTEM <em>✦</em> 8D HUBIFY <em>✦</em> v3.0 <em>✦</em> 2025 <em>✦</em></span>
  </div>
</div>

<footer style="padding:80px 0 48px;border-top:1px solid var(--border);background:var(--bg)">
  <div class="wrap-wide">
    <div style="display:grid;grid-template-columns:1fr auto;align-items:end;gap:48px;margin-bottom:48px">
      <div>
        <div style="font-family:var(--font-d);font-size:clamp(3rem,7vw,6rem);font-weight:400;line-height:.95;letter-spacing:-.03em;color:var(--text)">
          Pronto para <em style="font-style:normal;color:var(--cometa)">construir</em>.
        </div>
        <p style="font-family:var(--font-b);font-size:1.1rem;color:var(--text2);margin-top:24px;max-width:50ch;line-height:1.55;font-weight:300">
          Esse design system é a base viva da 8D Hubify. Use os tokens, copie os componentes, adapte o movimento — e mantenha a coerência.
        </p>
      </div>
      <div style="width:120px;opacity:.85">{logo_sym}</div>
    </div>
    <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:24px;padding-top:32px;border-top:1px solid var(--border);font-family:var(--font-m);font-size:.65rem;color:var(--text3);letter-spacing:.15em;text-transform:uppercase">
      <span>© 8D Hubify — 2025</span>
      <span>Design System — v3.0</span>
      <span>Made with ✦ for the cosmos</span>
    </div>
  </div>
</footer>

<script>
/* ── Icon data ─────────────────────────────────────────── */
const ICONS = {icons_js};

/* ── State ─────────────────────────────────────────────── */
let selectedIcon = null;
let iconColor = '#6633FF';
let iconSize = 24;

/* ── Theme toggle ──────────────────────────────────────── */
const html = document.documentElement;
const themeBtn = document.getElementById('theme-btn');
const themeIcon = document.getElementById('theme-icon');
const navLogo = document.getElementById('nav-logo-el');
const SUN_PATH = 'M12 17a5 5 0 1 0 0-10 5 5 0 0 0 0 10zM12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42';
const MOON_PATH = 'M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z';
themeBtn.onclick = () => {{
  const isDark = html.dataset.theme === 'dark';
  html.dataset.theme = isDark ? 'light' : 'dark';
  themeIcon.querySelector('path') && (themeIcon.querySelector('path').setAttribute('d', isDark ? SUN_PATH : MOON_PATH));
  asciiDraw();
}};

/* ── Loader ─────────────────────────────────────────────── */
window.addEventListener('load', () => {{
  setTimeout(() => document.getElementById('loader').classList.add('gone'), 900);
}});

/* ── Custom cursor ─────────────────────────────────────── */
const cursor = document.getElementById('cursor');
let cx = 0, cy = 0, tx = 0, ty = 0;
document.addEventListener('mousemove', e => {{ tx = e.clientX; ty = e.clientY; }});
(function animCursor() {{
  cx += (tx - cx) * .18; cy += (ty - cy) * .18;
  cursor.style.transform = `translate(${{cx}}px,${{cy}}px) translate(-50%,-50%)`;
  requestAnimationFrame(animCursor);
}})();
document.querySelectorAll('a,button,.card,.icon-item,.effect-card,.logo-card').forEach(el => {{
  el.addEventListener('mouseenter', () => cursor.classList.add('big'));
  el.addEventListener('mouseleave', () => cursor.classList.remove('big'));
}});

/* ══════════════════════════════════════════════════════════
   ASCII ENGINE — promptcache.com style
   charSet "█8DHubify✦", mouse repel + spring return + jiggle
   ══════════════════════════════════════════════════════════ */
(function initHeroAscii() {{
  const canvas = document.getElementById('ascii-canvas');
  const ctx = canvas.getContext('2d');

  const cfg = {{
    mouseRadius: 75, intensity: 4, fontSize: 14,
    charSpacing: 0.6, lineHeight: 1.05,
    mousePersistence: 0.96, returnSpeed: 0.08,
    returnWhenStill: true, enableJiggle: true,
    jiggleIntensity: 0.2, detailFactor: 50,
    contrast: 115, brightness: 105, saturation: 120,
    useTransparentBackground: false
  }};
  const charSet = '█8DHubify✦ ';

  /* Build source image — gradient-filled "8DH" symbol */
  const srcCanvas = document.createElement('canvas');
  const W = 600, H = 420;
  srcCanvas.width = W; srcCanvas.height = H;
  const sCtx = srcCanvas.getContext('2d');
  sCtx.fillStyle = '#000';
  sCtx.fillRect(0, 0, W, H);
  // Big "8D" centered
  const grad = sCtx.createLinearGradient(0, 0, W, H);
  grad.addColorStop(0, '#ffffff');
  grad.addColorStop(0.5, '#b9a3ff');
  grad.addColorStop(1, '#6633FF');
  sCtx.fillStyle = grad;
  sCtx.font = `400 ${{H * .82}}px "Hugein", serif`;
  sCtx.textAlign = 'center';
  sCtx.textBaseline = 'middle';
  sCtx.fillText('8D', W / 2, H / 2 + 8);

  canvas.width  = W;
  canvas.height = H;

  function applyContrastAndBrightness(imageData) {{
    const d = imageData.data;
    const c = cfg.contrast / 100, b = (cfg.brightness / 100 - 1) * 255;
    for (let i = 0; i < d.length; i += 4) {{
      d[i]   = Math.max(0, Math.min(255, d[i]   * c + b));
      d[i+1] = Math.max(0, Math.min(255, d[i+1] * c + b));
      d[i+2] = Math.max(0, Math.min(255, d[i+2] * c + b));
    }}
    return imageData;
  }}

  function colorScheme(r, g, b) {{
    const sat = cfg.saturation / 100;
    const gray = 0.299*r + 0.587*g + 0.114*b;
    const nr = Math.round(gray + (r - gray) * sat);
    const ng = Math.round(gray + (g - gray) * sat);
    const nb = Math.round(gray + (b - gray) * sat);
    return `rgb(${{nr}},${{ng}},${{nb}})`;
  }}

  let chars = [], particles = [], velocities = [], originalPositions = [];
  let mouseX = -9999, mouseY = -9999, lastMoveTime = 0;
  let heroRafId;

  function generateAsciiArt() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    chars = []; particles = []; velocities = []; originalPositions = [];

    const offW = Math.floor(canvas.width  / cfg.detailFactor * 10);
    const offH = Math.floor(canvas.height / cfg.detailFactor * 10);
    const off = document.createElement('canvas');
    off.width = offW; off.height = offH;
    const offCtx = off.getContext('2d');
    offCtx.drawImage(srcCanvas, 0, 0, offW, offH);
    let imgData = offCtx.getImageData(0, 0, offW, offH);
    imgData = applyContrastAndBrightness(imgData);
    const data = imgData.data;

    const colStep = Math.max(1, Math.floor(offW / (canvas.width  / (cfg.fontSize * cfg.charSpacing))));
    const rowStep = Math.max(1, Math.floor(offH / (canvas.height / (cfg.fontSize * cfg.lineHeight))));

    for (let row = 0; row < offH; row += rowStep) {{
      for (let col = 0; col < offW; col += colStep) {{
        const i = (row * offW + col) * 4;
        const r = data[i], g = data[i+1], b = data[i+2];
        const brightness = (r * 0.299 + g * 0.587 + b * 0.114) / 255;
        if (brightness < 0.04) continue;
        const charIdx = Math.floor(brightness * (charSet.length - 1));
        const ch = charSet[charIdx];
        if (!ch || ch === ' ') continue;

        const x = (col / offW) * canvas.width;
        const y = (row / offH) * canvas.height;
        chars.push({{ ch, color: colorScheme(r, g, b), brightness }});
        originalPositions.push({{ x, y }});
        particles.push({{ x, y }});
        velocities.push({{ x: 0, y: 0 }});
      }}
    }}
  }}

  function animate() {{
    const isDark = html.dataset.theme === 'dark';
    ctx.fillStyle = isDark ? '#000033' : '#F5F5FF';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width  / rect.width;
    const scaleY = canvas.height / rect.height;
    const localMX = (mouseX - rect.left) * scaleX;
    const localMY = (mouseY - rect.top)  * scaleY;
    const still = (Date.now() - lastMoveTime) > 150;

    ctx.font = `${{cfg.fontSize}}px monospace`;
    ctx.textAlign = 'left';
    ctx.textBaseline = 'top';

    for (let i = 0; i < particles.length; i++) {{
      const p = particles[i];
      const v = velocities[i];
      const orig = originalPositions[i];
      const info = chars[i];

      // Mouse repel
      const dx = p.x - localMX, dy = p.y - localMY;
      const dist = Math.sqrt(dx*dx + dy*dy);
      if (dist < cfg.mouseRadius && dist > 0) {{
        const force = (cfg.mouseRadius - dist) / cfg.mouseRadius * cfg.intensity;
        v.x += (dx / dist) * force;
        v.y += (dy / dist) * force;
      }}

      // Jiggle
      if (cfg.enableJiggle) {{
        v.x += (Math.random() - 0.5) * cfg.jiggleIntensity;
        v.y += (Math.random() - 0.5) * cfg.jiggleIntensity;
      }}

      // Damping
      v.x *= cfg.mousePersistence;
      v.y *= cfg.mousePersistence;

      // Spring return
      if (!still || cfg.returnWhenStill) {{
        v.x += (orig.x - p.x) * cfg.returnSpeed;
        v.y += (orig.y - p.y) * cfg.returnSpeed;
      }}

      p.x += v.x;
      p.y += v.y;

      // Use per-pixel color from source (gradient produces brand colors)
      ctx.fillStyle = info.color;
      ctx.globalAlpha = 0.6 + info.brightness * 0.4;
      ctx.fillText(info.ch, p.x, p.y);
    }}
    ctx.globalAlpha = 1;
    heroRafId = requestAnimationFrame(animate);
  }}

  canvas.addEventListener('mousemove', e => {{
    mouseX = e.clientX; mouseY = e.clientY; lastMoveTime = Date.now();
  }});
  canvas.addEventListener('mouseleave', () => {{ mouseX = -9999; mouseY = -9999; }});

  /* Wait for Hugein font, then generate */
  document.fonts.ready.then(() => {{
    generateAsciiArt();
    animate();
  }});

  /* Pause off-screen */
  new IntersectionObserver(entries => {{
    entries.forEach(e => {{
      if (!e.isIntersecting) cancelAnimationFrame(heroRafId);
      else animate();
    }});
  }}).observe(canvas);
}})();

/* Stub so theme-btn onclick doesn't error */
function asciiDraw() {{}}


/* ── Magnetic buttons ──────────────────────────────────── */
document.querySelectorAll('.mag-wrap').forEach(wrap => {{
  const btn = wrap.querySelector('.btn');
  wrap.addEventListener('mousemove', e => {{
    const r = wrap.getBoundingClientRect();
    const dx = (e.clientX - r.left - r.width / 2) * 0.3;
    const dy = (e.clientY - r.top - r.height / 2) * 0.3;
    btn.style.transform = `translate(${{dx}}px,${{dy}}px)`;
  }});
  wrap.addEventListener('mouseleave', () => {{ btn.style.transform = ''; }});
}});

/* ── Spotlight ─────────────────────────────────────────── */
const spotCard = document.getElementById('fx-spotlight');
const spotHole = document.getElementById('spotlight-hole');
spotCard.addEventListener('mousemove', e => {{
  const r = spotCard.getBoundingClientRect();
  const x = ((e.clientX - r.left) / r.width * 100).toFixed(1) + '%';
  const y = ((e.clientY - r.top) / r.height * 100).toFixed(1) + '%';
  spotHole.style.background = `radial-gradient(circle 90px at ${{x}} ${{y}}, transparent 0%, rgba(0,0,30,.88) 100%)`;
}});
spotCard.addEventListener('mouseleave', () => {{
  spotHole.style.background = `radial-gradient(circle 90px at 50% 50%, transparent 0%, rgba(0,0,30,.88) 100%)`;
}});

/* ── Parallax tilt ─────────────────────────────────────── */
const tiltCard = document.getElementById('fx-tilt');
const tiltInner = document.getElementById('tilt-inner');
const tiltShine = document.getElementById('tilt-shine');
tiltCard.addEventListener('mousemove', e => {{
  const r = tiltCard.getBoundingClientRect();
  const x = (e.clientX - r.left) / r.width;
  const y = (e.clientY - r.top) / r.height;
  const rx = (y - 0.5) * -18;
  const ry = (x - 0.5) * 18;
  tiltInner.style.transform = `rotateX(${{rx}}deg) rotateY(${{ry}}deg) translateZ(20px)`;
  tiltShine.style.background = `radial-gradient(circle at ${{x*100}}% ${{y*100}}%, rgba(255,255,255,.18) 0%, transparent 60%)`;
}});
tiltCard.addEventListener('mouseleave', () => {{
  tiltInner.style.transform = '';
  tiltShine.style.background = '';
}});

/* ── Liquid cursor effect ──────────────────────────────── */
const liqCard = document.getElementById('fx-liquid');
liqCard.addEventListener('mousemove', e => {{
  const r = liqCard.getBoundingClientRect();
  liqCard.style.setProperty('--lx', ((e.clientX - r.left) / r.width * 100) + '%');
  liqCard.style.setProperty('--ly', ((e.clientY - r.top) / r.height * 100) + '%');
}});

/* ── Scramble text ─────────────────────────────────────── */
const scrambleEl = document.getElementById('scramble-el');
const scrambleChars = '!@#$%^&*()_+-=[]{{}}|;:,.<>?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
let scrambleRunning = false;
function runScramble() {{
  if (scrambleRunning) return;
  scrambleRunning = true;
  const target = scrambleEl.dataset.text;
  let iter = 0;
  const iv = setInterval(() => {{
    scrambleEl.textContent = target.split('').map((ch, i) => {{
      if (i < iter) return target[i];
      if (ch === ' ') return ' ';
      return scrambleChars[Math.floor(Math.random() * scrambleChars.length)];
    }}).join('');
    if (iter >= target.length) {{ clearInterval(iv); scrambleRunning = false; }}
    iter += 0.4;
  }}, 30);
}}
scrambleEl.addEventListener('click', runScramble);
setInterval(runScramble, 4000);

/* ── Stagger reveal (IntersectionObserver) ─────────────── */
const revItems = document.querySelectorAll('.reveal-item');
const revObs = new IntersectionObserver(entries => {{
  entries.forEach(e => {{
    if (e.isIntersecting) {{
      revItems.forEach((el, i) => setTimeout(() => el.classList.add('visible'), i * 80));
      revObs.disconnect();
    }}
  }});
}}, {{ threshold: 0.3 }});
revObs.observe(document.getElementById('reveal-grid'));

/* ── Count up ──────────────────────────────────────────── */
const counters = document.querySelectorAll('.counter-num');
const countObs = new IntersectionObserver(entries => {{
  entries.forEach(e => {{
    if (e.isIntersecting) {{
      counters.forEach(el => {{
        const target = +el.dataset.target;
        const dur = 1500;
        const start = performance.now();
        (function tick(now) {{
          const t = Math.min((now - start) / dur, 1);
          const ease = 1 - Math.pow(1 - t, 3);
          el.textContent = Math.floor(ease * target);
          if (t < 1) requestAnimationFrame(tick);
          else el.textContent = target;
        }})(performance.now());
      }});
      countObs.disconnect();
    }}
  }});
}}, {{ threshold: 0.5 }});
countObs.observe(document.getElementById('counters'));

/* ── Icon library ──────────────────────────────────────── */
const iconGrid = document.getElementById('icon-grid');
const iconSearch = document.getElementById('icon-search');
const iconColorPicker = document.getElementById('icon-color');
const iconSizeInput = document.getElementById('icon-size');
const iconActions = document.getElementById('icon-actions');
const iconPreviewSvg = document.getElementById('icon-preview-svg');
const iconSelectedName = document.getElementById('icon-selected-name');
const iconCount = document.getElementById('icon-count');

function makeSvg(path, color, size) {{
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${{size}}" height="${{size}}" viewBox="0 0 24 24" fill="none" stroke="${{color}}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="${{path}}"/></svg>`;
}}

function renderIcons(filter) {{
  const q = filter.toLowerCase().trim();
  const entries = Object.entries(ICONS).filter(([n]) => !q || n.includes(q));
  iconCount.textContent = `${{entries.length}} ícones`;
  iconGrid.innerHTML = entries.map(([name, path]) => `
    <div class="icon-item${{selectedIcon === name ? ' selected' : ''}}" data-name="${{name}}" title="${{name}}">
      <svg class="icon-svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="${{iconColor}}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <path d="${{path}}"/>
      </svg>
      <span class="icon-name">${{name}}</span>
    </div>
  `).join('');
  iconGrid.querySelectorAll('.icon-item').forEach(el => {{
    el.addEventListener('click', () => selectIcon(el.dataset.name));
    el.addEventListener('mouseenter', () => cursor.classList.add('big'));
    el.addEventListener('mouseleave', () => cursor.classList.remove('big'));
  }});
}}

function selectIcon(name) {{
  selectedIcon = name;
  const path = ICONS[name];
  iconActions.classList.add('show');
  iconPreviewSvg.innerHTML = `<path d="${{path}}"/>`;
  iconPreviewSvg.setAttribute('stroke', iconColor);
  iconPreviewSvg.setAttribute('stroke-width', '1.8');
  iconPreviewSvg.setAttribute('stroke-linecap', 'round');
  iconPreviewSvg.setAttribute('stroke-linejoin', 'round');
  iconSelectedName.textContent = name;
  renderIcons(iconSearch.value);
}}

function downloadSVG() {{
  if (!selectedIcon) return;
  const size = +iconSizeInput.value || 24;
  const svgStr = makeSvg(ICONS[selectedIcon], iconColor, size);
  const blob = new Blob([svgStr], {{type: 'image/svg+xml'}});
  const a = Object.assign(document.createElement('a'), {{
    href: URL.createObjectURL(blob), download: selectedIcon + '.svg'
  }});
  a.click(); URL.revokeObjectURL(a.href);
}}

function downloadPNG() {{
  if (!selectedIcon) return;
  const size = +iconSizeInput.value || 24;
  const svgStr = makeSvg(ICONS[selectedIcon], iconColor, size);
  const img = new Image();
  const blob = new Blob([svgStr], {{type:'image/svg+xml'}});
  const url = URL.createObjectURL(blob);
  img.onload = () => {{
    const c = Object.assign(document.createElement('canvas'), {{width:size, height:size}});
    const cx2 = c.getContext('2d');
    cx2.drawImage(img, 0, 0, size, size);
    c.toBlob(b => {{
      const a = Object.assign(document.createElement('a'), {{
        href: URL.createObjectURL(b), download: selectedIcon + `-${{size}}px.png`
      }});
      a.click(); URL.revokeObjectURL(a.href);
    }}, 'image/png');
    URL.revokeObjectURL(url);
  }};
  img.src = url;
}}

iconSearch.addEventListener('input', () => renderIcons(iconSearch.value));
iconColorPicker.addEventListener('input', e => {{
  iconColor = e.target.value;
  iconPreviewSvg.setAttribute('stroke', iconColor);
  renderIcons(iconSearch.value);
}});
iconSizeInput.addEventListener('change', () => {{ iconSize = +iconSizeInput.value; }});
renderIcons('');

/* ══════════════════════════════════════════════════════════
   ASCII ART STUDIO
   ══════════════════════════════════════════════════════════ */
(function initStudio() {{
  const stCanvas   = document.getElementById('studio-canvas');
  const stCtx      = stCanvas.getContext('2d');
  const dropZone   = document.getElementById('studio-drop-zone');
  const dropOvl    = document.getElementById('studio-drop-overlay');
  const fileInput  = document.getElementById('studio-file-input');

  // Controls
  const charsetEl   = document.getElementById('studio-charset');
  const fontsizeEl  = document.getElementById('studio-fontsize');
  const detailEl    = document.getElementById('studio-detail');
  const radiusEl    = document.getElementById('studio-radius');
  const contrastEl  = document.getElementById('studio-contrast');
  const brightnessEl= document.getElementById('studio-brightness');

  // Value labels
  const ids = ['fs','detail','radius','contrast','brightness'];
  ids.forEach(id => {{
    const el = document.getElementById(`studio-${{id}}`);
    const lbl = document.getElementById(`studio-${{id}}-val`);
    if (el && lbl) el.addEventListener('input', () => {{ lbl.textContent = el.value; studioRegen(); }});
  }});

  let stSource = null, stIsVideo = false;
  let stChars = [], stParticles = [], stVelocities = [], stOrigPos = [];
  let stMouseX = -9999, stMouseY = -9999, stLastMove = 0, stRafId;

  function stApplyContrastBrightness(imageData) {{
    const d = imageData.data;
    const c = +contrastEl.value / 100, b = (+brightnessEl.value / 100 - 1) * 255;
    for (let i = 0; i < d.length; i += 4) {{
      d[i]   = Math.max(0, Math.min(255, d[i]*c + b));
      d[i+1] = Math.max(0, Math.min(255, d[i+1]*c + b));
      d[i+2] = Math.max(0, Math.min(255, d[i+2]*c + b));
    }}
    return imageData;
  }}

  function stGenerate() {{
    if (!stSource) return;
    stChars = []; stParticles = []; stVelocities = []; stOrigPos = [];
    const fs = +fontsizeEl.value;
    const detail = +detailEl.value;
    const charset = charsetEl.value || '█8DHubify✦ ';

    const srcW = stIsVideo ? stSource.videoWidth  : stSource.naturalWidth;
    const srcH = stIsVideo ? stSource.videoHeight : stSource.naturalHeight;
    if (!srcW || !srcH) return;

    const aspect = srcW / srcH;
    const cW = Math.floor(stCanvas.parentElement.clientWidth * 0.92);
    const cH = Math.floor(cW / aspect);
    stCanvas.width = cW; stCanvas.height = cH;

    const offW = Math.floor(cW / detail * 10);
    const offH = Math.floor(cH / detail * 10);
    const off = document.createElement('canvas');
    off.width = offW; off.height = offH;
    const offC = off.getContext('2d');
    offC.drawImage(stSource, 0, 0, offW, offH);
    let imgData = offC.getImageData(0, 0, offW, offH);
    imgData = stApplyContrastBrightness(imgData);
    const data = imgData.data;

    const colStep = Math.max(1, Math.floor(offW / (cW / (fs * 0.62))));
    const rowStep = Math.max(1, Math.floor(offH / (cH / (fs * 1.05))));

    for (let row = 0; row < offH; row += rowStep) {{
      for (let col = 0; col < offW; col += colStep) {{
        const i = (row * offW + col) * 4;
        const r = data[i], g = data[i+1], b = data[i+2];
        const bright = (r * 0.299 + g * 0.587 + b * 0.114) / 255;
        if (bright < 0.04) continue;
        const ch = charset[Math.floor(bright * (charset.length - 1))];
        if (!ch || ch === ' ') continue;
        const x = (col / offW) * cW, y = (row / offH) * cH;
        stChars.push({{ ch, color: `rgb(${{r}},${{g}},${{b}})`, bright }});
        stOrigPos.push({{ x, y }});
        stParticles.push({{ x, y }});
        stVelocities.push({{ x: 0, y: 0 }});
      }}
    }}
  }}

  function stAnimate() {{
    if (!stSource) return;
    if (stIsVideo) stGenerate();  // re-sample each video frame
    const fs = +fontsizeEl.value;
    const radius = +radiusEl.value;
    stCtx.fillStyle = '#000';
    stCtx.fillRect(0, 0, stCanvas.width, stCanvas.height);
    const rect = stCanvas.getBoundingClientRect();
    const sx = stCanvas.width / rect.width, sy = stCanvas.height / rect.height;
    const lmx = (stMouseX - rect.left) * sx, lmy = (stMouseY - rect.top) * sy;
    const still = (Date.now() - stLastMove) > 150;
    stCtx.font = `${{fs}}px monospace`;
    stCtx.textAlign = 'left';
    stCtx.textBaseline = 'top';
    for (let i = 0; i < stParticles.length; i++) {{
      const p = stParticles[i], v = stVelocities[i];
      const orig = stOrigPos[i], info = stChars[i];
      const dx = p.x - lmx, dy = p.y - lmy;
      const dist = Math.sqrt(dx*dx + dy*dy);
      if (dist < radius && dist > 0) {{
        const force = (radius - dist) / radius * 3.5;
        v.x += dx / dist * force; v.y += dy / dist * force;
      }}
      v.x += (Math.random() - 0.5) * 0.18;
      v.y += (Math.random() - 0.5) * 0.18;
      v.x *= 0.96; v.y *= 0.96;
      v.x += (orig.x - p.x) * 0.09; v.y += (orig.y - p.y) * 0.09;
      p.x += v.x; p.y += v.y;
      stCtx.fillStyle = info.color;
      stCtx.globalAlpha = 0.5 + info.bright * 0.5;
      stCtx.fillText(info.ch, p.x, p.y);
    }}
    stCtx.globalAlpha = 1;
    stRafId = requestAnimationFrame(stAnimate);
  }}

  function stLoad(src, isVideo) {{
    cancelAnimationFrame(stRafId);
    stSource = src; stIsVideo = isVideo;
    dropOvl.classList.add('hidden');
    stGenerate();
    stAnimate();
  }}

  function studioRegen() {{
    cancelAnimationFrame(stRafId);
    stGenerate();
    stAnimate();
  }}

  charsetEl.addEventListener('change', studioRegen);

  stCanvas.addEventListener('mousemove', e => {{ stMouseX = e.clientX; stMouseY = e.clientY; stLastMove = Date.now(); }});
  stCanvas.addEventListener('mouseleave', () => {{ stMouseX = -9999; stMouseY = -9999; }});

  function handleFile(file) {{
    if (!file) return;
    if (file.name.toLowerCase().endsWith('.obj')) {{
      handleOBJ(file); return;
    }}
    if (file.type.startsWith('video/')) {{
      const vid = document.createElement('video');
      vid.muted = true; vid.loop = true; vid.autoplay = true;
      vid.oncanplay = () => {{ vid.play(); stLoad(vid, true); }};
      vid.src = URL.createObjectURL(file);
    }} else {{
      const img = new Image();
      img.onload = () => stLoad(img, false);
      img.src = URL.createObjectURL(file);
    }}
  }}

  function handleOBJ(file) {{
    // Render OBJ via Three.js if available, else show placeholder
    if (typeof THREE === 'undefined') {{
      const script = document.createElement('script');
      script.src = 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js';
      script.onload = () => {{
        const s2 = document.createElement('script');
        s2.src = 'https://cdn.jsdelivr.net/npm/three@0.160.0/examples/js/loaders/OBJLoader.js';
        s2.onload = () => renderOBJ(file);
        document.head.appendChild(s2);
      }};
      document.head.appendChild(script);
    }} else {{ renderOBJ(file); }}
  }}

  function renderOBJ(file) {{
    const url = URL.createObjectURL(file);
    const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: false }});
    renderer.setSize(560, 320);
    renderer.setClearColor(0x000000);
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, 560/320, 0.1, 1000);
    camera.position.set(0, 0, 3);
    scene.add(new THREE.AmbientLight(0xffffff, 0.8));
    const dLight = new THREE.DirectionalLight(0xffffff, 0.6);
    dLight.position.set(1, 2, 2);
    scene.add(dLight);
    const loader = new THREE.OBJLoader();
    loader.load(url, obj => {{
      scene.add(obj);
      const box = new THREE.Box3().setFromObject(obj);
      const center = box.getCenter(new THREE.Vector3());
      obj.position.sub(center);
      renderer.render(scene, camera);
      const img = new Image();
      img.onload = () => stLoad(img, false);
      img.src = renderer.domElement.toDataURL();
      URL.revokeObjectURL(url);
    }});
  }}

  dropZone.addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', e => handleFile(e.target.files[0]));
  dropZone.addEventListener('dragover', e => {{ e.preventDefault(); dropZone.style.borderColor = 'var(--cometa)'; }});
  dropZone.addEventListener('dragleave', () => {{ dropZone.style.borderColor = ''; }});
  dropZone.addEventListener('drop', e => {{ e.preventDefault(); dropZone.style.borderColor = ''; handleFile(e.dataTransfer.files[0]); }});

  document.getElementById('studio-export-png').addEventListener('click', () => {{
    if (!stSource) return;
    stCanvas.toBlob(b => {{
      const a = Object.assign(document.createElement('a'), {{ href: URL.createObjectURL(b), download: '8dh-ascii.png' }});
      a.click(); URL.revokeObjectURL(a.href);
    }}, 'image/png');
  }});

  document.getElementById('studio-export-svg').addEventListener('click', () => {{
    if (!stSource) return;
    const fs = +fontsizeEl.value;
    let svgStr = `<svg xmlns="http://www.w3.org/2000/svg" width="${{stCanvas.width}}" height="${{stCanvas.height}}" style="background:#000">`;
    for (let i = 0; i < stParticles.length; i++) {{
      const p = stParticles[i], info = stChars[i];
      svgStr += `<text x="${{p.x.toFixed(1)}}" y="${{(p.y + fs).toFixed(1)}}" font-size="${{fs}}" font-family="monospace" fill="${{info.color}}" opacity="${{(0.5 + info.bright * 0.5).toFixed(2)}}">${{info.ch}}</text>`;
    }}
    svgStr += '</svg>';
    const blob = new Blob([svgStr], {{type:'image/svg+xml'}});
    const a = Object.assign(document.createElement('a'), {{ href: URL.createObjectURL(blob), download: '8dh-ascii.svg' }});
    a.click(); URL.revokeObjectURL(a.href);
  }});
}})();

/* ══════════════════════════════════════════════════════════
   GSAP ANIMATION GALLERY  (GSAP carregado no <head>)
   ══════════════════════════════════════════════════════════ */
(function initGSAP() {{
  if (!window.gsap) {{ console.warn('GSAP não carregou'); return; }}
  if (window.ScrollTrigger) gsap.registerPlugin(ScrollTrigger);

  const scrambleCharsG = '!@#$%^&*ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

  const animations = {{
    1() {{
      gsap.fromTo(['#g1-a','#g1-b'],
        {{ y: 60, opacity: 0, clipPath: 'inset(100% 0 0 0)' }},
        {{ y: 0, opacity: 1, clipPath: 'inset(0% 0 0 0)', duration: 0.8, ease: 'power3.out', stagger: 0.15 }});
    }},
    2() {{
      gsap.fromTo('.g2-item',
        {{ scale: 0, opacity: 0 }},
        {{ scale: 1, opacity: 1, duration: 0.5, ease: 'back.out(1.7)', stagger: 0.07 }});
    }},
    3() {{
      const el = document.getElementById('g3-num');
      el.textContent = '0';
      gsap.to({{ val: 0 }}, {{
        val: 320, duration: 2, ease: 'power2.out',
        onUpdate: function() {{ el.textContent = Math.round(this.targets()[0].val); }}
      }});
    }},
    4() {{
      gsap.fromTo('#g4-box',
        {{ scale: 0, rotation: -180 }},
        {{ scale: 1, rotation: 0, duration: 0.9, ease: 'elastic.out(1,0.5)' }});
    }},
    5() {{
      gsap.fromTo('#g5-path', {{ strokeDashoffset: 300 }}, {{ strokeDashoffset: 0, duration: 1.4, ease: 'power2.inOut' }});
    }},
    6() {{
      gsap.to('#g6-card', {{
        rotationY: 720, duration: 1.2, ease: 'power3.inOut',
        onUpdate: function() {{
          const r = this.targets()[0];
          const angle = gsap.getProperty(r, 'rotationY') % 360;
          r.style.background = angle > 90 && angle < 270
            ? 'linear-gradient(135deg,var(--nuvem),var(--interestelar))'
            : 'var(--cometa)';
        }}
      }});
    }},
    7() {{
      gsap.to('#g7-orb', {{
        backgroundColor: '#ED694B',
        borderRadius: '10%',
        scale: 1.3,
        duration: 0.8, ease: 'power2.inOut',
        yoyo: true, repeat: 1
      }});
    }},
    8() {{
      const tl = gsap.timeline();
      tl.to('#g8-a', {{ scaleX: 1, duration: 0.5, ease: 'power2.out' }})
        .to('#g8-b', {{ scaleX: 0.75, duration: 0.5, ease: 'power2.out' }}, '-=0.2')
        .to('#g8-c', {{ scaleX: 0.5, duration: 0.5, ease: 'power2.out' }}, '-=0.2');
    }},
    9() {{
      const el = document.getElementById('g9-text');
      const target = 'Hubify';
      let iter = 0, running = true;
      const iv = setInterval(() => {{
        el.textContent = target.split('').map((ch, i) => {{
          if (i < iter) return target[i];
          return scrambleCharsG[Math.floor(Math.random() * scrambleCharsG.length)];
        }}).join('');
        if (iter >= target.length) {{ clearInterval(iv); el.textContent = target; }}
        iter += 0.4;
      }}, 40);
    }},
    10() {{
      const container = document.getElementById('g10-particles');
      container.innerHTML = '';
      const cx = 100, cy = 90;
      for (let i = 0; i < 24; i++) {{
        const dot = document.createElement('div');
        dot.style.cssText = `position:absolute;width:8px;height:8px;border-radius:50%;
          left:${{cx}}px;top:${{cy}}px;background:hsl(${{(i/24)*360}},80%,65%);transform:translate(-50%,-50%)`;
        container.appendChild(dot);
        const angle = (i / 24) * Math.PI * 2;
        const dist = 50 + Math.random() * 40;
        gsap.to(dot, {{
          x: Math.cos(angle) * dist, y: Math.sin(angle) * dist,
          scale: 0, opacity: 0, duration: 0.7 + Math.random() * 0.4,
          ease: 'power3.out', delay: Math.random() * 0.1
        }});
      }}
    }}
  }};

  function resetAnimations() {{
    // Reset static positions before replay
    gsap.set(['#g1-a','#g1-b'], {{ y: 60, opacity: 0, clipPath: 'inset(100% 0 0 0)' }});
    gsap.set('.g2-item', {{ scale: 0, opacity: 0 }});
    gsap.set('#g4-box', {{ scale: 0, rotation: -180 }});
    gsap.set('#g5-path', {{ strokeDashoffset: 300 }});
    gsap.set('#g6-card', {{ rotationY: 0 }});
    gsap.set('#g7-orb', {{ backgroundColor: 'var(--cometa)', borderRadius: '50%', scale: 1 }});
    gsap.set(['#g8-a','#g8-b','#g8-c'], {{ scaleX: 0 }});
    document.getElementById('g9-text').textContent = 'Hubify';
    document.getElementById('g3-num').textContent = '0';
  }}

  function runAnim(n) {{
    resetAnimations();
    setTimeout(() => animations[n] && animations[n](), 50);
  }}

  // Wire replay buttons
  document.querySelectorAll('.gsap-replay').forEach(btn => {{
    btn.addEventListener('click', () => runAnim(+btn.dataset.anim));
  }});

  // Wire stage click for particle burst
  document.getElementById('g10-stage').addEventListener('click', () => runAnim(10));

  // Auto-play when section comes into view (com ScrollTrigger se disponível)
  const gsapObs = new IntersectionObserver(entries => {{
    entries.forEach(e => {{
      if (e.isIntersecting) {{
        resetAnimations();
        setTimeout(() => Object.keys(animations).forEach((k, i) => setTimeout(() => animations[k](), i * 100)), 200);
        gsapObs.disconnect();
      }}
    }});
  }}, {{ threshold: 0.15 }});
  gsapObs.observe(document.getElementById('gsap-grid'));
}})();

/* ══════════════════════════════════════════════════════════
   GSAP — SCROLL REVEALS SITE-WIDE
   ══════════════════════════════════════════════════════════ */
(function initScrollReveals() {{
  if (!window.gsap || !window.ScrollTrigger) return;

  // Section heads — split-style reveal
  gsap.utils.toArray('.section-head').forEach(head => {{
    gsap.from(head.querySelectorAll('.section-eyebrow, .section-title, .section-desc'), {{
      y: 40, opacity: 0, duration: 1, ease: 'power3.out', stagger: 0.12,
      scrollTrigger: {{ trigger: head, start: 'top 80%', toggleActions: 'play none none reverse' }}
    }});
    gsap.from(head.querySelector('.section-num'), {{
      y: 80, opacity: 0, duration: 1.4, ease: 'power3.out',
      scrollTrigger: {{ trigger: head, start: 'top 80%', toggleActions: 'play none none reverse' }}
    }});
  }});

  // Generic content reveals
  gsap.utils.toArray('.color-chip, .logo-card, .comp-row, .effect-card, .token-group, .icon-item, .gsap-card').forEach((el, i) => {{
    gsap.from(el, {{
      y: 30, opacity: 0, duration: .8, ease: 'power2.out',
      scrollTrigger: {{ trigger: el, start: 'top 88%', toggleActions: 'play none none reverse' }}
    }});
  }});

  // Type rows
  gsap.utils.toArray('.type-row').forEach((el, i) => {{
    gsap.from(el, {{
      x: -20, opacity: 0, duration: .9, ease: 'power3.out',
      scrollTrigger: {{ trigger: el, start: 'top 85%', toggleActions: 'play none none reverse' }}
    }});
  }});

  // Hero headline lines
  gsap.from('.hero-h1 .line span', {{
    yPercent: 110, duration: 1.1, ease: 'power4.out', stagger: 0.1, delay: 0.3
  }});
}})();
</script>
</body>
</html>'''

out = os.path.join(BASE, 'design-system.html')
with open(out, 'w') as f:
    f.write(HTML)

print(f"Done: {len(HTML):,} bytes — {out}")
