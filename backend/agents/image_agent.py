"""
Image Evidence + Sampling Trigger Agent
--------------------------------------
Responsibilities:
1. Visual confirmation of construction stage (CNN placeholder)
2. Geo + timestamp validation
3. Decide WHEN, WHERE, HOW MANY samples are needed
4. Trigger human-in-the-loop sampling task
"""

from datetime import datetime




def validate_geo(latitude: float, longitude: float):
    return latitude is not None and longitude is not None


def validate_timestamp(timestamp: str):
    try:
        datetime.fromisoformat(timestamp)
        return True
    except ValueError:
        return False



def cnn_visible_layer_detector(image_bytes: bytes):
    """
    Simulated CNN output.
    Replace with real model in production.
    """
    return {
        "visible_layer": "bituminous_surface",
        "confidence": 0.92
    }




def decide_sampling(
    visible_layer: str,
    segment_index: int,
    contractor_risk_level: str = "NORMAL"
):
    """
    AI logic to decide:
    - WHEN sampling is required
    - WHERE sampling is required
    - HOW MANY samples are needed
    """

    sampling_required = False
    samples_required = 0
    reason = None

    # Rule 1: First appearance of bituminous layer
    if visible_layer == "bituminous_surface" and segment_index == 1:
        sampling_required = True
        samples_required = 1
        reason = "First bituminous layer detected"

    # Rule 2: Every 10th segment
    elif visible_layer == "bituminous_surface" and segment_index % 10 == 0:
        sampling_required = True
        samples_required = 1
        reason = "Periodic quality sampling"

    # Rule 3: High-risk contractor
    if contractor_risk_level == "HIGH":
        sampling_required = True
        samples_required = max(samples_required, 2)
        reason = "High-risk contractor sampling"

    return {
        "sampling_required": sampling_required,
        "samples_required": samples_required,
        "reason": reason
    }




def run_image_sampling_agent(
    image_bytes: bytes,
    segment_id: str,
    segment_index: int,
    latitude: float,
    longitude: float,
    timestamp: str,
    contractor_risk_level: str = "NORMAL"
):
    """
    Image Evidence + Sampling Trigger Agent
    """

    # Step 1: Validation
    geo_valid = validate_geo(latitude, longitude)
    time_valid = validate_timestamp(timestamp)

    # Step 2: Vision analysis
    cnn_result = cnn_visible_layer_detector(image_bytes)

    # Step 3: Sampling decision (AI reasoning)
    sampling_decision = decide_sampling(
        visible_layer=cnn_result["visible_layer"],
        segment_index=segment_index,
        contractor_risk_level=contractor_risk_level
    )

    # Step 4: Final output (evidence + task)
    return {
        "segment_id": segment_id,
        "geo_valid": geo_valid,
        "timestamp_valid": time_valid,

        # Vision evidence
        "visible_layer": cnn_result["visible_layer"],
        "vision_confidence": cnn_result["confidence"],

        # Sampling decision (HITL trigger)
        "sampling_required": sampling_decision["sampling_required"],
        "samples_required": sampling_decision["samples_required"],
        "sampling_reason": sampling_decision["reason"],

        # Human action required if sampling_required == True
        "human_action": "CORE_CUTTING_AND_LAB_TEST"
        if sampling_decision["sampling_required"]
        else None
    }
