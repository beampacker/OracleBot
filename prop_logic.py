import requests

DVP = {
    "ATL": 22, "BOS": 4, "BKN": 11, "CHA": 28, "CHI": 14,
    "CLE": 6, "DAL": 16, "DEN": 18, "DET": 29, "GSW": 20,
    "HOU": 2, "IND": 26, "LAC": 10, "LAL": 15, "MEM": 12,
    "MIA": 3, "MIL": 26, "MIN": 1, "NOP": 7, "NYK": 8,
    "OKC": 9, "ORL": 5, "PHI": 13, "PHX": 19, "POR": 30,
    "SAC": 24, "SAS": 27, "TOR": 23, "UTA": 25, "WAS": 17,
}

PACE = {
    "FAST": 1.15,
    "MEDIUM": 1.00,
    "SLOW": 0.85
}

# -------------------------------------------------
# ⭐ Season Averages from The Odds API (reliable)
# -------------------------------------------------
def fetch_player_season_avg(name, api_key):
    url = f"https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?regions=us&apiKey={api_key}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return None  # placeholder for future stats
    except:
        return None


# -------------------------------------------------
# ⭐ Core Oracle Projection Engine (No Z-Score)
# -------------------------------------------------
def calculate_proj(player, stat, line, opponent, homeaway):
    stat = stat.upper()

    # Weighted averages (fantasy-style projection)
    # in future: L5/L10 from stat API
    L5 = 0
    L10 = 0
    L15 = 0

    weighted_proj = round((L5 * 0.5) + (L10 * 0.3) + (L15 * 0.2), 2)

    # DVP penalty/boost
    dvp_rank = DVP.get(opponent, 15)

    if dvp_rank <= 5: dvp_adj = -1.75
    elif dvp_rank <= 10: dvp_adj = -1.0
    elif dvp_rank <= 20: dvp_adj = 0.25
    else: dvp_adj = 1.0

    # Pace
    pace_key = "FAST" if stat in ["PTS", "PRA", "3PT"] else "MEDIUM"
    pace_adj = PACE[pace_key] - 1.0

    # Final projection
    final_proj = weighted_proj + dvp_adj + pace_adj
    diff = round(final_proj - line, 2)

    if diff >= 1.5: rec = "OVER — High Confidence 🔥"
    elif diff >= 0.5: rec = "Lean OVER"
    elif diff >= -0.5: rec = "Coinflip"
    else: rec = "UNDER — Risky ❌"

    return {
        "L5": L5,
        "L10": L10,
        "L15": L15,
        "weighted": weighted_proj,
        "projection": final_proj,
        "difference": diff,
        "recommendation": rec,
        "dvp_rank": dvp_rank,
        "pace": pace_key
    }
