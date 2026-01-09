"""
Universal Axiom Prism - Introspective Framework

This module provides semantic wrappers and tools for applying the EPIPHANY
framework introspectively, using the language of the Universal Axiom Prism.

Components:
- Impulses (A): Driving forces (positive/negative motivations)
- Elements (B): Resources (energy, matter, state)
- Pressure (C): Direction and integrity (constructive/destructive)
- Exponential Growth (E_n): Rapid, compounded expansion
- Fibonacci Growth (F_n): Balanced, stable development
- Objectivity Scale (X): Alignment with truth (inverse of subjectivity)
- Why Axis (Y): Motivational alignment with long-term goals
- TimeSphere (Z): Temporal evolution and progress
"""
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
from epiphany_engine.engine.state import AxiomInputs
from epiphany_engine.axiom.core_equation import compute_intelligence


@dataclass
class PrismComponents:
    """
    Semantic representation of the Universal Axiom Prism components.

    Maps the abstract variables to their conceptual meanings for
    introspective application.
    """
    # ABC - The Foundation
    impulses: float  # A: Driving forces (motivations, desires, fears)
    elements: float  # B: Resources (skills, knowledge, energy, state)
    pressure: float  # C: Direction & integrity (external/internal pressures)

    # XYZ - The Context
    objectivity: float  # X: Alignment with truth (0=subjective, 1=objective)
    why_alignment: float  # Y: Motivational alignment with long-term goals
    time_progress: float  # Z: Temporal development and maturity

    # Evolution
    energy: float  # E_n: Current energy/momentum
    feedback: float  # F_n: Feedback loops and iteration count

    def to_axiom_inputs(self) -> AxiomInputs:
        """Convert semantic prism components to technical axiom inputs."""
        return AxiomInputs(
            A=self.impulses,
            B=self.elements,
            C=self.pressure,
            X=self.objectivity,
            Y=self.why_alignment,
            Z=self.time_progress,
            E_n=self.energy,
            F_n=self.feedback,
        )

    @classmethod
    def from_axiom_inputs(cls, inputs: AxiomInputs) -> "PrismComponents":
        """Convert technical axiom inputs to semantic prism components."""
        return cls(
            impulses=inputs.A,
            elements=inputs.B,
            pressure=inputs.C,
            objectivity=inputs.X,
            why_alignment=inputs.Y,
            time_progress=inputs.Z,
            energy=inputs.E_n,
            feedback=inputs.F_n,
        )


class IntrospectivePrism:
    """
    Tools for introspective application of the Universal Axiom Prism.

    Provides semantic analysis and guidance for personal development,
    career analysis, organizational assessment, etc.
    """

    @staticmethod
    def calculate_why_alignment(
        current_score: float,
        maximum_score: float,
    ) -> float:
        """
        Calculate Why Axis (Y) as alignment ratio.

        Y = Y_s / Y_max

        Where:
        - Y_s is the current motivational score
        - Y_max is the maximum possible alignment

        Returns value in [0, 1] where:
        - 0 = completely misaligned with long-term goals
        - 1 = perfectly aligned with long-term goals
        """
        if maximum_score <= 0:
            return 0.0
        return min(1.0, max(0.0, current_score / maximum_score))

    @staticmethod
    def assess_impulses(
        positive_impulses: Dict[str, float],
        negative_impulses: Dict[str, float],
        weights: Optional[Dict[str, float]] = None,
    ) -> Tuple[float, Dict[str, float]]:
        """
        Assess impulses (A) from positive and negative drivers.

        Parameters
        ----------
        positive_impulses : dict
            Positive driving forces (e.g., {"passion": 0.9, "curiosity": 0.8})
        negative_impulses : dict
            Negative driving forces (e.g., {"fear": 0.6, "anxiety": 0.4})
        weights : optional dict
            Weights for each impulse type

        Returns
        -------
        (score, breakdown) : tuple
            - score: Overall impulse strength in [0, 1]
            - breakdown: Detailed analysis
        """
        if weights is None:
            weights = {**{k: 1.0 for k in positive_impulses}, **{k: -0.5 for k in negative_impulses}}

        # Positive contributions
        pos_sum = sum(positive_impulses[k] * weights.get(k, 1.0) for k in positive_impulses)
        pos_count = len(positive_impulses) or 1

        # Negative deductions
        neg_sum = sum(negative_impulses[k] * abs(weights.get(k, 0.5)) for k in negative_impulses)
        neg_count = len(negative_impulses) or 1

        # Net impulse score
        net_positive = pos_sum / pos_count
        net_negative = neg_sum / neg_count
        score = max(0.0, min(1.0, net_positive - (net_negative * 0.3)))  # Negatives have 30% impact

        breakdown = {
            "positive_average": net_positive,
            "negative_average": net_negative,
            "net_score": score,
            "positive_details": positive_impulses,
            "negative_details": negative_impulses,
        }

        return score, breakdown

    @staticmethod
    def assess_elements(
        skills: Dict[str, float],
        knowledge: Dict[str, float],
        emotional_state: Dict[str, float],
    ) -> Tuple[float, Dict[str, float]]:
        """
        Assess elements (B) from skills, knowledge, and emotional state.

        Parameters
        ----------
        skills : dict
            Technical skills (e.g., {"programming": 0.8, "communication": 0.7})
        knowledge : dict
            Domain knowledge (e.g., {"ML": 0.9, "business": 0.6})
        emotional_state : dict
            Emotional resources (e.g., {"confidence": 0.7, "resilience": 0.8})

        Returns
        -------
        (score, breakdown) : tuple
        """
        skill_avg = sum(skills.values()) / len(skills) if skills else 0.0
        knowledge_avg = sum(knowledge.values()) / len(knowledge) if knowledge else 0.0
        emotion_avg = sum(emotional_state.values()) / len(emotional_state) if emotional_state else 0.0

        # Weighted combination (skills 40%, knowledge 30%, emotional 30%)
        score = (skill_avg * 0.4) + (knowledge_avg * 0.3) + (emotion_avg * 0.3)

        breakdown = {
            "skills_average": skill_avg,
            "knowledge_average": knowledge_avg,
            "emotional_average": emotion_avg,
            "combined_score": score,
            "skills": skills,
            "knowledge": knowledge,
            "emotional_state": emotional_state,
        }

        return score, breakdown

    @staticmethod
    def assess_pressure(
        constructive: Dict[str, float],
        destructive: Dict[str, float],
    ) -> Tuple[float, Dict[str, float]]:
        """
        Assess pressure (C) from constructive and destructive forces.

        Parameters
        ----------
        constructive : dict
            Positive pressures (e.g., {"career_goals": 0.8, "mentorship": 0.7})
        destructive : dict
            Negative pressures (e.g., {"workload_stress": 0.6, "fear_of_failure": 0.5})

        Returns
        -------
        (score, breakdown) : tuple
        """
        const_avg = sum(constructive.values()) / len(constructive) if constructive else 0.0
        destr_avg = sum(destructive.values()) / len(destructive) if destructive else 0.0

        # Net pressure: constructive pressure is positive, destructive reduces it
        score = max(0.0, min(1.0, const_avg - (destr_avg * 0.4)))  # Destructive has 40% impact

        breakdown = {
            "constructive_average": const_avg,
            "destructive_average": destr_avg,
            "net_score": score,
            "constructive_details": constructive,
            "destructive_details": destructive,
        }

        return score, breakdown


def compute_prism_intelligence(components: PrismComponents) -> float:
    """
    Compute intelligence using semantic prism components.

    This is a convenience wrapper that converts prism components
    to axiom inputs and computes intelligence.
    """
    inputs = components.to_axiom_inputs()
    return compute_intelligence(**inputs.to_dict())


# Example introspective scenario
def example_career_introspection():
    """
    Example: Using the prism for career development analysis.
    """
    print("\n" + "=" * 70)
    print("INTROSPECTIVE PRISM - Career Development Analysis")
    print("=" * 70 + "\n")

    prism = IntrospectivePrism()

    # 1. Assess Impulses
    impulses_score, impulses_breakdown = prism.assess_impulses(
        positive_impulses={
            "passion_for_field": 0.9,
            "ambition": 0.8,
            "curiosity": 0.85,
        },
        negative_impulses={
            "job_security_fear": 0.6,
            "work_life_stress": 0.5,
        }
    )
    print(f"IMPULSES (A): {impulses_score:.3f}")
    print(f"  Positive drivers: {impulses_breakdown['positive_average']:.3f}")
    print(f"  Negative drivers: {impulses_breakdown['negative_average']:.3f}\n")

    # 2. Assess Elements
    elements_score, elements_breakdown = prism.assess_elements(
        skills={
            "technical_expertise": 0.8,
            "problem_solving": 0.85,
            "communication": 0.7,
        },
        knowledge={
            "domain_expertise": 0.9,
            "industry_trends": 0.6,
        },
        emotional_state={
            "confidence": 0.7,
            "resilience": 0.8,
            "focus": 0.75,
        }
    )
    print(f"ELEMENTS (B): {elements_score:.3f}")
    print(f"  Skills: {elements_breakdown['skills_average']:.3f}")
    print(f"  Knowledge: {elements_breakdown['knowledge_average']:.3f}")
    print(f"  Emotional: {elements_breakdown['emotional_average']:.3f}\n")

    # 3. Assess Pressure
    pressure_score, pressure_breakdown = prism.assess_pressure(
        constructive={
            "career_aspirations": 0.9,
            "professional_development": 0.8,
            "mentorship": 0.7,
        },
        destructive={
            "workload_stress": 0.6,
            "fear_of_failure": 0.5,
            "imposter_syndrome": 0.4,
        }
    )
    print(f"PRESSURE (C): {pressure_score:.3f}")
    print(f"  Constructive: {pressure_breakdown['constructive_average']:.3f}")
    print(f"  Destructive: {pressure_breakdown['destructive_average']:.3f}\n")

    # 4. Calculate Why Alignment
    why_score = prism.calculate_why_alignment(
        current_score=7.5,  # Current alignment with goals
        maximum_score=10.0   # Perfect alignment
    )
    print(f"WHY ALIGNMENT (Y): {why_score:.3f}\n")

    # 5. Create full prism assessment
    components = PrismComponents(
        impulses=impulses_score,
        elements=elements_score,
        pressure=pressure_score,
        objectivity=0.8,  # High objectivity in self-assessment
        why_alignment=why_score,
        time_progress=0.6,  # Mid-career
        energy=5.0,  # Current momentum
        feedback=3.0,  # 3 feedback loops established
    )

    intelligence = compute_prism_intelligence(components)

    print("=" * 70)
    print(f"CAREER INTELLIGENCE SCORE: {intelligence:.4f}")
    print("=" * 70 + "\n")

    print("Interpretation:")
    print(f"  Your career intelligence reflects strong impulses ({impulses_score:.2f})")
    print(f"  and solid elements ({elements_score:.2f}), with moderate pressure")
    print(f"  management ({pressure_score:.2f}). Focus on reducing destructive")
    print(f"  pressures and strengthening feedback loops for exponential growth.")
    print()


if __name__ == "__main__":
    example_career_introspection()
