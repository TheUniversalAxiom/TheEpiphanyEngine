"""
Plotting utilities for visualizing axiom computations and simulation results.
"""

try:
    import matplotlib.gridspec as gridspec
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.patches import Rectangle
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

from typing import Dict, List, Optional, Tuple

from engine.timesphere import SimulationResult


def _check_matplotlib():
    """Ensure matplotlib is available."""
    if not HAS_MATPLOTLIB:
        raise ImportError(
            "Matplotlib is required for visualization. "
            "Install it with: pip install matplotlib"
        )


def plot_intelligence_trajectory(
    result: SimulationResult,
    title: str = "Intelligence Evolution",
    figsize: Tuple[int, int] = (12, 6),
    show: bool = True,
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Plot intelligence trajectory over time.

    Args:
        result: SimulationResult from TimeSphere
        title: Plot title
        figsize: Figure size (width, height)
        show: Whether to display the plot
        save_path: Optional path to save figure

    Returns:
        matplotlib Figure object
    """
    _check_matplotlib()

    steps = [h.step for h in result.history]
    intelligence = [h.intelligence for h in result.history]

    fig, ax = plt.subplots(figsize=figsize)

    ax.plot(steps, intelligence, linewidth=2.5, color='darkblue',
            marker='o', markersize=5, label='Intelligence')
    ax.fill_between(steps, intelligence, alpha=0.2, color='darkblue')

    # Add trend line
    if len(steps) > 2:
        z = np.polyfit(steps, intelligence, 1)
        p = np.poly1d(z)
        ax.plot(steps, p(steps), "--", color='red', alpha=0.5,
                linewidth=1.5, label='Trend')

    ax.set_xlabel('Time Step', fontsize=12)
    ax.set_ylabel('Intelligence Score', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    # Add summary text
    initial = intelligence[0]
    final = intelligence[-1]
    growth = ((final / initial - 1) * 100) if initial > 0 else 0

    textstr = f'Initial: {initial:.2f}\nFinal: {final:.2f}\nGrowth: {growth:+.1f}%'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=props)

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')

    if show:
        plt.show()

    return fig


def plot_component_evolution(
    result: SimulationResult,
    components: List[str] = None,
    title: str = "Component Evolution",
    figsize: Tuple[int, int] = (14, 8),
    show: bool = True,
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Plot evolution of axiom components over time.

    Args:
        result: SimulationResult from TimeSphere
        components: List of components to plot (e.g., ['A', 'B', 'C'])
                   If None, plots all available components
        title: Plot title
        figsize: Figure size
        show: Whether to display
        save_path: Optional save path

    Returns:
        matplotlib Figure object
    """
    _check_matplotlib()

    if components is None:
        components = ['A', 'B', 'C', 'X', 'Y', 'Z', 'E_n', 'F_n']

    steps = [h.step for h in result.history]

    # Create subplots
    n_components = len(components)
    n_cols = 3
    n_rows = (n_components + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    if n_rows == 1:
        axes = axes.reshape(1, -1)
    axes = axes.flatten()

    colors = plt.cm.tab10(np.linspace(0, 1, len(components)))

    for idx, component in enumerate(components):
        values = [getattr(h.inputs, component) for h in result.history]

        ax = axes[idx]
        ax.plot(steps, values, linewidth=2, color=colors[idx],
                marker='o', markersize=4)
        ax.fill_between(steps, values, alpha=0.2, color=colors[idx])
        ax.set_xlabel('Step', fontsize=10)
        ax.set_ylabel(f'{component}', fontsize=10)
        ax.set_title(f'{component} Evolution', fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3)

        # Add change indicator
        initial = values[0]
        final = values[-1]
        change = final - initial
        change_pct = (change / initial * 100) if initial > 0 else 0

        color = 'green' if change >= 0 else 'red'
        ax.text(0.98, 0.02, f'{change:+.3f} ({change_pct:+.1f}%)',
                transform=ax.transAxes, fontsize=9,
                horizontalalignment='right', color=color, fontweight='bold')

    # Hide unused subplots
    for idx in range(len(components), len(axes)):
        axes[idx].set_visible(False)

    plt.suptitle(title, fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')

    if show:
        plt.show()

    return fig


def plot_sensitivity_analysis(
    compute_func,
    baseline_config: Dict[str, float],
    param_name: str,
    param_range: np.ndarray = None,
    title: str = None,
    figsize: Tuple[int, int] = (10, 6),
    show: bool = True,
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Plot sensitivity of intelligence to a single parameter.

    Args:
        compute_func: Function that computes intelligence (e.g., compute_intelligence)
        baseline_config: Baseline parameter configuration
        param_name: Name of parameter to vary
        param_range: Range of values to test (default: 0.1 to 1.0)
        title: Plot title
        figsize: Figure size
        show: Whether to display
        save_path: Optional save path

    Returns:
        matplotlib Figure object
    """
    _check_matplotlib()

    if param_range is None:
        param_range = np.linspace(0.1, 1.0, 50)

    if title is None:
        title = f'Sensitivity to {param_name}'

    scores = []
    for value in param_range:
        config = baseline_config.copy()
        config[param_name] = value
        try:
            score, _ = compute_func(**config, return_components=True)
            scores.append(score)
        except TypeError:
            score = compute_func(**config)
            scores.append(score)

    fig, ax = plt.subplots(figsize=figsize)

    ax.plot(param_range, scores, linewidth=2.5, color='steelblue')
    ax.fill_between(param_range, scores, alpha=0.2, color='steelblue')

    # Mark baseline value
    baseline_value = baseline_config[param_name]
    baseline_idx = np.argmin(np.abs(param_range - baseline_value))
    baseline_score = scores[baseline_idx]

    ax.axvline(baseline_value, color='red', linestyle='--', alpha=0.5,
               label=f'Baseline ({baseline_value:.2f})')
    ax.plot(baseline_value, baseline_score, 'ro', markersize=10,
            label=f'Score: {baseline_score:.2f}')

    ax.set_xlabel(f'{param_name} Value', fontsize=12)
    ax.set_ylabel('Intelligence Score', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')

    if show:
        plt.show()

    return fig


def plot_scenario_comparison(
    results: Dict[str, SimulationResult],
    title: str = "Scenario Comparison",
    figsize: Tuple[int, int] = (14, 6),
    show: bool = True,
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Compare intelligence trajectories across multiple scenarios.

    Args:
        results: Dict mapping scenario names to SimulationResults
        title: Plot title
        figsize: Figure size
        show: Whether to display
        save_path: Optional save path

    Returns:
        matplotlib Figure object
    """
    _check_matplotlib()

    fig, ax = plt.subplots(figsize=figsize)

    colors = plt.cm.tab10(np.linspace(0, 1, len(results)))

    for idx, (name, result) in enumerate(results.items()):
        steps = [h.step for h in result.history]
        intelligence = [h.intelligence for h in result.history]

        ax.plot(steps, intelligence, linewidth=2.5, marker='o',
                markersize=4, label=name, color=colors[idx])

    ax.set_xlabel('Time Step', fontsize=12)
    ax.set_ylabel('Intelligence Score', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(fontsize=10, loc='best')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')

    if show:
        plt.show()

    return fig


def plot_heatmap_2d(
    compute_func,
    baseline_config: Dict[str, float],
    param_x: str,
    param_y: str,
    param_x_range: np.ndarray = None,
    param_y_range: np.ndarray = None,
    title: str = None,
    figsize: Tuple[int, int] = (10, 8),
    show: bool = True,
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Create 2D heatmap showing intelligence as function of two parameters.

    Args:
        compute_func: Function that computes intelligence
        baseline_config: Baseline configuration
        param_x: First parameter name
        param_y: Second parameter name
        param_x_range: Range for first parameter
        param_y_range: Range for second parameter
        title: Plot title
        figsize: Figure size
        show: Whether to display
        save_path: Optional save path

    Returns:
        matplotlib Figure object
    """
    _check_matplotlib()

    if param_x_range is None:
        param_x_range = np.linspace(0.1, 1.0, 30)
    if param_y_range is None:
        param_y_range = np.linspace(0.1, 1.0, 30)

    if title is None:
        title = f'Intelligence Heatmap: {param_x} vs {param_y}'

    # Compute intelligence grid
    X, Y = np.meshgrid(param_x_range, param_y_range)
    Z = np.zeros_like(X)

    for i in range(len(param_y_range)):
        for j in range(len(param_x_range)):
            config = baseline_config.copy()
            config[param_x] = X[i, j]
            config[param_y] = Y[i, j]
            try:
                score, _ = compute_func(**config, return_components=True)
                Z[i, j] = score
            except TypeError:
                Z[i, j] = compute_func(**config)

    fig, ax = plt.subplots(figsize=figsize)

    im = ax.contourf(X, Y, Z, levels=20, cmap='viridis')
    contours = ax.contour(X, Y, Z, levels=10, colors='white',
                          alpha=0.3, linewidths=0.5)
    ax.clabel(contours, inline=True, fontsize=8)

    # Mark baseline
    baseline_x = baseline_config[param_x]
    baseline_y = baseline_config[param_y]
    ax.plot(baseline_x, baseline_y, 'r*', markersize=15,
            label='Baseline', markeredgecolor='white', markeredgewidth=1)

    ax.set_xlabel(param_x, fontsize=12)
    ax.set_ylabel(param_y, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')

    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Intelligence Score', fontsize=11)

    ax.legend(fontsize=10)

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')

    if show:
        plt.show()

    return fig


def create_dashboard(
    result: SimulationResult,
    title: str = "Intelligence Evolution Dashboard",
    figsize: Tuple[int, int] = (18, 12),
    show: bool = True,
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Create comprehensive dashboard with multiple visualizations.

    Args:
        result: SimulationResult from TimeSphere
        title: Dashboard title
        figsize: Figure size
        show: Whether to display
        save_path: Optional save path

    Returns:
        matplotlib Figure object
    """
    _check_matplotlib()

    steps = [h.step for h in result.history]
    intelligence = [h.intelligence for h in result.history]

    fig = plt.figure(figsize=figsize)
    gs = gridspec.GridSpec(3, 3, hspace=0.35, wspace=0.3)

    # Main intelligence trajectory (top, full width)
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(steps, intelligence, linewidth=3, color='darkblue',
             marker='o', markersize=6)
    ax1.fill_between(steps, intelligence, alpha=0.2, color='darkblue')
    ax1.set_xlabel('Time Step', fontsize=11)
    ax1.set_ylabel('Intelligence Score', fontsize=11)
    ax1.set_title('Intelligence Evolution', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)

    # ABC components
    ax2 = fig.add_subplot(gs[1, 0])
    a_vals = [h.inputs.A for h in result.history]
    b_vals = [h.inputs.B for h in result.history]
    c_vals = [h.inputs.C for h in result.history]
    ax2.plot(steps, a_vals, label='A', linewidth=2)
    ax2.plot(steps, b_vals, label='B', linewidth=2)
    ax2.plot(steps, c_vals, label='C', linewidth=2)
    ax2.set_xlabel('Step', fontsize=10)
    ax2.set_ylabel('Value', fontsize=10)
    ax2.set_title('ABC Components', fontsize=11, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)

    # XYZ components
    ax3 = fig.add_subplot(gs[1, 1])
    x_vals = [h.inputs.X for h in result.history]
    y_vals = [h.inputs.Y for h in result.history]
    z_vals = [h.inputs.Z for h in result.history]
    ax3.plot(steps, x_vals, label='X', linewidth=2)
    ax3.plot(steps, y_vals, label='Y', linewidth=2)
    ax3.plot(steps, z_vals, label='Z', linewidth=2)
    ax3.set_xlabel('Step', fontsize=10)
    ax3.set_ylabel('Value', fontsize=10)
    ax3.set_title('XYZ Components', fontsize=11, fontweight='bold')
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3)

    # E_n and F_n
    ax4 = fig.add_subplot(gs[1, 2])
    e_vals = [h.inputs.E_n for h in result.history]
    f_vals = [h.inputs.F_n for h in result.history]
    ax4_twin = ax4.twinx()
    ax4.plot(steps, e_vals, label='E_n', linewidth=2, color='blue')
    ax4_twin.plot(steps, f_vals, label='F_n', linewidth=2, color='orange')
    ax4.set_xlabel('Step', fontsize=10)
    ax4.set_ylabel('E_n', fontsize=10, color='blue')
    ax4_twin.set_ylabel('F_n', fontsize=10, color='orange')
    ax4.set_title('Evolution Factors', fontsize=11, fontweight='bold')
    ax4.tick_params(axis='y', labelcolor='blue')
    ax4_twin.tick_params(axis='y', labelcolor='orange')
    ax4.grid(True, alpha=0.3)

    # Growth rate
    ax5 = fig.add_subplot(gs[2, :2])
    growth_rates = [0] + [(intelligence[i] - intelligence[i-1]) / intelligence[i-1] * 100
                           for i in range(1, len(intelligence))]
    colors = ['green' if g > 0 else 'red' for g in growth_rates]
    ax5.bar(steps, growth_rates, color=colors, alpha=0.6)
    ax5.axhline(0, color='black', linewidth=0.8)
    ax5.set_xlabel('Step', fontsize=10)
    ax5.set_ylabel('Growth Rate (%)', fontsize=10)
    ax5.set_title('Step-by-Step Growth Rate', fontsize=11, fontweight='bold')
    ax5.grid(True, alpha=0.3, axis='y')

    # Summary statistics
    ax6 = fig.add_subplot(gs[2, 2])
    ax6.axis('off')

    summary_stats = result.summary
    stats_text = (
        f"Summary Statistics:\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"Min: {summary_stats['min_intelligence']:.2f}\n"
        f"Max: {summary_stats['max_intelligence']:.2f}\n"
        f"Avg: {summary_stats['avg_intelligence']:.2f}\n"
        f"Final: {summary_stats['final_intelligence']:.2f}\n\n"
        f"Growth: {summary_stats['total_growth_pct']:.1f}%\n"
        f"Volatility: {summary_stats['volatility']:.2f}\n"
    )

    ax6.text(0.1, 0.9, stats_text, transform=ax6.transAxes,
             fontsize=10, verticalalignment='top',
             fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5))

    plt.suptitle(title, fontsize=15, fontweight='bold', y=0.995)

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')

    if show:
        plt.show()

    return fig
