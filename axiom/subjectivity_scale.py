"""
7-threshold subjectivity → objectivity scale and helpers.

Provides:
- x_from_observations(noise, emotional_volatility, bias_indicator, weights=...)
- label_x(x)
- thresholds and labels are configurable.
"""
import warnings
from typing import Dict, Iterable, Optional, Tuple

Number = float

# Define 7 thresholds (edges) dividing the [0,1] interval into 7 buckets.
# We will treat x in [0,1], where 0 = fully objective, 1 = fully subjective.
DEFAULT_THRESHOLDS = [0.0, 0.15, 0.33, 0.5, 0.67, 0.85, 1.0]
DEFAULT_LABELS = [
    "apex-objective",  # 0.0 - 0.15
    "objective",       # 0.15 - 0.33
    "base-static",     # 0.33 - 0.50
    "mid-dynamic",     # 0.50 - 0.67
    "high-subjective", # 0.67 - 0.85
    "apex-dynamic",    # 0.85 - 1.0
    "apex-subjective", # exact 1.0 (optional)
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
    Derive a subjectivity score X in [0,1] from observation-level signals.

    Parameters
    ----------
    noise : float
        Observational noise; higher noise -> more subjectivity.
    emotional_volatility : float
        Measure of transient affect; higher -> more subjectivity.
    bias_indicator : float
        Measure of detected systemic bias; higher -> more subjectivity.
    weights : optional dict to weight components, expected keys: 'noise', 'emotion', 'bias'
    normalize : if True, scale the computed value to [0,1] by simple heuristic.

    Returns
    -------
    float in [0,1]
    """
    default_weights = {"noise": 0.4, "emotion": 0.35, "bias": 0.25}
    provided_weights = weights or {}
    unknown_keys = set(provided_weights) - set(default_weights)
    if unknown_keys:
        warnings.warn(
            f"Unknown weight keys provided: {sorted(unknown_keys)}",
            UserWarning,
            stacklevel=2,
        )
    weights = {**default_weights, **provided_weights}

    # Basic linear combination; input signals can be any non-negative number.
    score = weights["noise"] * float(noise) + weights["emotion"] * float(emotional_volatility) + weights["bias"] * float(bias_indicator)

    if normalize:
        # Heuristic normalization: assume typical input ranges on [0,1]; if sum exceeds 1, compress
        score = _clamp01(score)

    return float(score)


def determine_subjectivity(
    noise: float = 0.0,
    emotional_volatility: float = 0.0,
    bias_indicator: float = 0.0,
    *,
    weights: Optional[Dict[str, float]] = None,
    normalize: bool = True,
) -> Tuple[float, str]:
    """
    Derive subjectivity score and label from observation-level signals.

    Returns a tuple of (x, label).
    """
    x = x_from_observations(
        noise=noise,
        emotional_volatility=emotional_volatility,
        bias_indicator=bias_indicator,
        weights=weights,
        normalize=normalize,
    )
    return x, label_x(x)


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
