"""Generate the labelled runtime and offline-evaluation architecture figure."""

from pathlib import Path
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


def main():
    fig, ax = plt.subplots(figsize=(8.6, 5.5))
    ax.set_xlim(-0.15, 11.25)
    ax.set_ylim(-0.45, 6.25)
    ax.axis("off")

    def box(x, y, w, h, t, color="#edf2f5"):
        ax.add_patch(
            FancyBboxPatch(
                (x, y),
                w,
                h,
                boxstyle="round,pad=0.04",
                facecolor=color,
                edgecolor="#405363",
                linewidth=1,
            )
        )
        ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=11)

    def route(points, label=None, at=None):
        xs, ys = zip(*points)
        if len(points) > 2:
            ax.plot(xs[:-1], ys[:-1], color="#405363", lw=1.15)
        ax.annotate(
            "",
            xy=points[-1],
            xytext=points[-2],
            arrowprops={"arrowstyle": "->", "color": "#405363", "lw": 1.15},
        )
        if label:
            ax.text(
                *at,
                label,
                ha="center",
                va="center",
                fontsize=9.3,
                bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.4},
            )

    box(0.05, 4.9, 2.35, 0.9, "Question and\nshared context")
    box(3.6, 4.9, 2.6, 0.9, "Model and tool loop\nExecuted receipts")
    box(7.5, 4.9, 2.6, 0.9, "Candidate answer\nwith citations")
    route([(2.44, 5.35), (3.56, 5.35)])
    route([(6.24, 5.35), (7.46, 5.35)])
    box(7.5, 2.75, 2.6, 0.9, "Evidence validator", color="#e3f0e9")
    route([(8.8, 4.86), (8.8, 3.69)], "Verified", (8.8, 4.2))
    box(3.6, 2.75, 2.6, 0.9, "One correction\nwithin ten-turn limit")
    route([(7.46, 3.2), (6.24, 3.2)], "First failure\nand turn left", (6.85, 3.8))
    route([(4.9, 3.69), (4.9, 4.86)], "Resume loop", (4.9, 4.2))
    box(7.5, 0.65, 2.6, 0.9, "Saved final output")
    route([(8.8, 2.71), (8.8, 1.59)], "Pass", (8.8, 2.14))
    route(
        [(10.14, 5.35), (10.95, 5.35), (10.95, 1.1), (10.14, 1.1)],
        "Baseline\nor prompt\nbypass",
        (10.85, 3.65),
    )
    box(3.6, 0.65, 2.6, 0.9, "Blocked response\nError and null claims", color="#f8ece0")
    route(
        [(7.7, 2.71), (6.9, 2.0), (4.9, 2.0), (4.9, 1.59)],
        "Still invalid or no turn left",
        (5.0, 2.1),
    )
    route([(6.24, 1.1), (7.46, 1.1)])
    box(0.05, 0.65, 2.35, 0.9, "Offline evaluator\nIndependent key", color="#fff2df")
    route(
        [(8.8, 0.61), (8.8, 0.1), (1.22, 0.1), (1.22, 0.61)],
        "Saved records only",
        (4.85, 0.08),
    )
    ax.text(
        5.55,
        -0.32,
        "The answer key never enters the model loop or runtime validator.",
        ha="center",
        fontsize=9.7,
    )
    fig.tight_layout(pad=0.3)
    out = Path(__file__).resolve().parents[1] / "documentation/figures/architecture.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=240)
    plt.close(fig)


if __name__ == "__main__":
    main()
