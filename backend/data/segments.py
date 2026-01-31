# 10 km road → 100 segments of 100m each
TOTAL_SEGMENTS = 100

ROAD_SEGMENTS = [
    {
        "segment_id": f"S{i+1:03}",
        "verified": False
    }
    for i in range(TOTAL_SEGMENTS)
]
