"""
7-threshold objectivity scale and helpers.

X represents OBJECTIVITY (alignment with objective truth).
- X = 1.0: Fully objective (no bias, no noise, no emotion)
- X = 0.0: Fully subjective (maximum bias, noise, emotion)

Provides:
- x_from_observations(noise, emotional_volatility, bias_indicator, weights=...)
- label_x(x)
- thresholds and labels are configurable.
"""
from typing import Tuple, Dict, Iterable, Optional

Number = float

# Define 7 thresholds (edges) dividing the [0,1] interval into 7 buckets.
# X in [0,1], where 0 = fully subjective, 1 = fully objective.
DEFAULT_THRESHOLDS = [0.0, 0.15, 0.33, 0.5, 0.67, 0.85, 1.0]
DEFAULT_LABELS = [
    "apex-subjective",  # 0.0 - 0.15: Maximum subjectivity
    "high-subjective",  # 0.15 - 0.33: High subjectivity
    "mid-dynamic",      # 0.33 - 0.50: Moderate subjectivity
    "base-static",      # 0.50 - 0.67: Slight subjectivity
    "objective",        # 0.67 - 0.85: Mostly objective
    "high-objective",   # 0.85 - 1.0: High objectivity
    "apex-objective",   # ~1.0: Maximum objectivity
]


def _clamp01(v: float) -> float:
    if v != v:  # NaN guard
        return 0.0
    return max(0.0, min(1.0, float(v)))


def x_from_observations(
    noise: float = 0.0,
    emotional_volatility: float = 0.0,
    bias_indicator: float = 0.0,
    *,
    weights: Optional[Dict[str, float]] = None,
    normalize: bool = True,
) -> float:
    """
    Derive an objectivity score X in [0,1] from observation-level signals.

    X represents OBJECTIVITY (inverse of subjectivity).
    Higher noise, emotion, and bias reduce objectivity.

    Parameters
    ----------
    noise : float
        Observational noise; higher noise -> lower objectivity.
    emotional_volatility : float
        Measure of transient affect; higher emotion -> lower objectivity.
    bias_indicator : float
        Measure of detected systemic bias; higher bias -> lower objectivity.
    weights : optional dict to weight components, keys: 'noise', 'emotion', 'bias'
    normalize : if True, scale the computed value to [0,1] by simple heuristic.

    Returns
    -------
    float in [0,1] where 1.0 = fully objective, 0.0 = fully subjective
    """
    # Default weights for subjectivity indicators
    default_weights = {"noise": 0.4, "emotion": 0.35, "bias": 0.25}

    if weights is None:
        weights = default_weights
    else:
        # Use provided weights with defaults for missing keys (fixes Issue #4)
        weights = {
            "noise": weights.get("noise", default_weights["noise"]),
            "emotion": weights.get("emotion", default_weights["emotion"]),
            "bias": weights.get("bias", default_weights["bias"]),
        }

    # Calculate subjectivity score (higher = more subjective)
    subjectivity = (
        weights["noise"] * float(noise) +
        weights["emotion"] * float(emotional_volatility) +
        weights["bias"] * float(bias_indicator)
    )

    if normalize:
        # Normalize to [0,1]
        subjectivity = _clamp01(subjectivity)

    # Return OBJECTIVITY (inverse of subjectivity)
    objectivity = 1.0 - subjectivity

    return float(objectivity)


def label_x(x: float, thresholds: Optional[Iterable[float]] = None, labels: Optional[Iterable[str]] = None) -> str:
    """
    Map numeric x -> qualitative label based on thresholds.

    thresholds: iterable of length 7 giving bucket upper bounds in ascending order.
    labels: iterable of length 7 matching thresholds.
    """
    x = _clamp01(float(x))
    if thresholds is None:
        thresholds = DEFAULT_THRESHOLDS
    if labels is None:
        labels = DEFAULT_LABELS

    thresholds = list(thresholds)
    labels = list(labels)

    if len(thresholds) != len(labels):
        # If thresholds length differs, fall back to default
        thresholds = DEFAULT_THRESHOLDS
        labels = DEFAULT_LABELS

    for bound, label in zip(thresholds, labels):
        if x <= bound:
            return label
    return labels[-1]  # fallback


# Small convenience helper to get both
def x_with_label(**observations) -> Tuple[float, str]:
    x = x_from_observations(
        observations.get("noise", 0.0),
        observations.get("emotional_volatility", 0.0),
        observations.get("bias_indicator", 0.0),
        weights=observations.get("weights"),
        normalize=observations.get("normalize", True),
    )
    return x, label_x(x)
