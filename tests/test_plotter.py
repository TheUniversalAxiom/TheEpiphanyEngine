"""
Plotting tests for viz/plotter.py
"""


def test_plotting_with_simulation_result():
    """Ensure plotting helpers accept real SimulationResult objects."""
    try:
        import matplotlib
    except ImportError:
        return

    matplotlib.use("Agg")

    import matplotlib.pyplot as plt

    from engine.state import AxiomInputs
    from engine.timesphere import TimeSphere, UpdateRules
    from viz import plot_component_evolution, plot_intelligence_trajectory
    from viz.plotter import create_dashboard

    inputs = AxiomInputs(A=0.4, B=0.4, C=0.4, X=0.6, Y=0.6, Z=0.6, E_n=1.0, F_n=0.0)
    sphere = TimeSphere(initial_inputs=inputs)
    sphere.add_update_rule("A", UpdateRules.linear_growth(rate=0.05, max_val=1.0, variable="A"))
    sphere.add_update_rule("X", UpdateRules.decay(rate=0.02, min_val=0.2, variable="X"))

    result = sphere.simulate(steps=4)

    fig1 = plot_intelligence_trajectory(result, show=False)
    fig2 = plot_component_evolution(result, components=["A", "B", "X"], show=False)
    fig3 = create_dashboard(result, show=False)

    for fig in (fig1, fig2, fig3):
        assert fig is not None
        plt.close(fig)
