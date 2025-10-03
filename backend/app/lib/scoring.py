# backend/app/lib/scoring.py

import math
from datetime import datetime

def score_indicator(source_rep=0, sightings=1, enrichment_hits=0, first_seen=None):
    score = source_rep

    # sighting weight
    score += int(10 * math.log2(max(sightings, 1)))

    # enrichment hits
    score += 20 * enrichment_hits

    # freshness decay
    if first_seen:
        age_days = (datetime.utcnow() - first_seen).days
        if age_days > 30:
            score -= 2 * (age_days - 30)
        if age_days > 90:
            score -= 5 * (age_days - 90)

    # clamp 0–100
    return max(0, min(100, score))
