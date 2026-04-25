"""
Generate polished visual assets for the Executive Operations Dashboard case study.

Outputs (saved to ../images/):
  01-dashboard-mockup.png    — full dashboard layout (KPI cards + charts + table)
  02-kpi-card-detail.png     — KPI card design close-up
  03-architecture.png        — source-to-dashboard data flow diagram
  04-before-after.png        — process improvement before/after panel
"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
IMG_DIR = ROOT / "images"
IMG_DIR.mkdir(exist_ok=True, parents=True)

# Brand palette
NAVY     = "#1F3A5F"
PRIMARY  = "#1565C0"
TEAL     = "#2980B9"
GOOD     = "#3A9B7A"
ACCENT   = "#F2A93B"
BAD      = "#D13438"
NEUTRAL  = "#605E5C"
LIGHT    = "#F3F2F1"
PAGE_BG  = "#FAFAFA"
CARD_BG  = "#FFFFFF"
TEXT     = "#252423"
TEXT2    = "#605E5C"

plt.rcParams.update({
    "figure.dpi": 110,
    "savefig.dpi": 140,
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def card(ax, x, y, w, h, fill=CARD_BG, edge=LIGHT, lw=0.8):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.005,rounding_size=0.04",
                         linewidth=lw, facecolor=fill, edgecolor=edge)
    ax.add_patch(box)


def text(ax, x, y, s, **kw):
    defaults = dict(ha="left", va="center", color=TEXT, fontsize=10)
    defaults.update(kw)
    ax.text(x, y, s, **defaults)


# ---------------------------------------------------------------------------
# 1. Full dashboard mockup
# ---------------------------------------------------------------------------
def dashboard_mockup():
    fig = plt.figure(figsize=(16, 9), facecolor=PAGE_BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")

    # ---- Header bar ----
    header = Rectangle((0, 8.2), 16, 0.8, facecolor=NAVY, edgecolor="none")
    ax.add_patch(header)
    text(ax, 0.4, 8.6, "Operations Performance Dashboard",
         color="white", fontsize=18, fontweight="bold")
    text(ax, 0.4, 8.32, "Executive view  ·  Refreshed daily  ·  All zones",
         color="#C5D5E8", fontsize=10)
    text(ax, 15.6, 8.6, "Q3 2026", color="white",
         fontsize=12, fontweight="bold", ha="right")
    text(ax, 15.6, 8.32, "Prepared for Operations Leadership",
         color="#C5D5E8", fontsize=9, ha="right")

    # ---- Slicer row ----
    text(ax, 0.4, 7.85, "FILTERS", color=TEXT2, fontsize=8, fontweight="bold")
    slicers = [("Reporting Period", "Last 8 weeks"),
               ("Service Zone", "All zones"),
               ("Priority", "All priorities"),
               ("Status", "Open + Closed")]
    for i, (label, val) in enumerate(slicers):
        x = 0.3 + i * 3.9
        card(ax, x, 7.25, 3.6, 0.45, fill=CARD_BG, edge="#D9D9D9")
        text(ax, x + 0.2, 7.55, label, color=TEXT2, fontsize=8)
        text(ax, x + 0.2, 7.36, val, color=TEXT, fontsize=10, fontweight="bold")

    # ---- KPI row ----
    kpis = [
        ("Total Incidents",       "12,847", "+4.2% WoW",  GOOD),
        ("Open Work Items",        "1,964",  "-2.8% WoW",  GOOD),
        ("Avg Resolution (days)",  "3.2",    "vs 4.0 SLA", GOOD),
        ("Backlog Volume",         "612",    "+1.1% WoW",  ACCENT),
        ("% Completed",            "84.7%",  "+0.6 pts",   GOOD),
        ("Active Locations",       "47",     "of 52",      NEUTRAL),
    ]
    kpi_y = 6.05
    kpi_h = 1.05
    kpi_w = 2.55
    for i, (name, val, delta, color) in enumerate(kpis):
        x = 0.3 + i * 2.62
        card(ax, x, kpi_y, kpi_w, kpi_h, fill=CARD_BG, edge="#E1DFDD")
        text(ax, x + 0.2, kpi_y + 0.85, name.upper(), color=TEXT2, fontsize=8, fontweight="bold")
        text(ax, x + 0.2, kpi_y + 0.48, val, color=PRIMARY, fontsize=22, fontweight="bold")
        text(ax, x + 0.2, kpi_y + 0.18, delta, color=color, fontsize=9, fontweight="bold")

    # ---- Trend chart ----
    chart_y, chart_h = 1.0, 4.65
    card(ax, 0.3, chart_y, 9.9, chart_h, fill=CARD_BG, edge="#E1DFDD")
    text(ax, 0.55, chart_y + chart_h - 0.3, "Weekly Completed Trend",
         color=TEXT, fontsize=12, fontweight="bold")
    text(ax, 0.55, chart_y + chart_h - 0.55, "Closed work items per week  ·  last 8 weeks",
         color=TEXT2, fontsize=9)

    weeks = ["W22", "W23", "W24", "W25", "W26", "W27", "W28", "W29"]
    closed = [820, 945, 1010, 980, 1150, 1240, 1180, 1305]
    opened = [880, 920, 970, 1020, 1080, 1140, 1170, 1240]

    # Chart axes positioned inside card with room above for title/subtitle
    chart_ax = fig.add_axes([0.06, 0.16, 0.55, 0.32])
    chart_ax.plot(weeks, closed, marker="o", color=PRIMARY, linewidth=2.8, label="Closed")
    chart_ax.plot(weeks, opened, marker="o", color=ACCENT, linewidth=2.4, label="Opened",
                  linestyle="--")
    chart_ax.fill_between(weeks, closed, alpha=0.10, color=PRIMARY)
    chart_ax.set_ylim(700, 1380)
    chart_ax.set_yticks([800, 900, 1000, 1100, 1200, 1300])
    chart_ax.tick_params(labelsize=9, colors=TEXT2)
    chart_ax.spines["left"].set_color("#D9D9D9")
    chart_ax.spines["bottom"].set_color("#D9D9D9")
    chart_ax.grid(axis="y", alpha=0.3, linestyle="--")
    chart_ax.legend(frameon=False, loc="lower right", fontsize=10)
    for s in ("top", "right"):
        chart_ax.spines[s].set_visible(False)

    # ---- Zone breakdown ----
    card(ax, 10.4, chart_y, 5.3, chart_h, fill=CARD_BG, edge="#E1DFDD")
    text(ax, 10.65, chart_y + chart_h - 0.3, "Backlog by Service Zone",
         color=TEXT, fontsize=12, fontweight="bold")
    text(ax, 10.65, chart_y + chart_h - 0.55, "Open work items, top 6 zones",
         color=TEXT2, fontsize=9)

    # Short labels — section title establishes the "Service Zone" context
    zones = ["North", "Central", "South", "East", "Coastal", "Inland"]
    backlog = [184, 142, 98, 72, 64, 52]
    bar_ax = fig.add_axes([0.71, 0.16, 0.24, 0.32])
    bars = bar_ax.barh(zones[::-1], backlog[::-1], color=PRIMARY, edgecolor="white", linewidth=1.2)
    for bar, val in zip(bars, backlog[::-1]):
        bar_ax.text(val + 4, bar.get_y() + bar.get_height() / 2,
                    f"{val:,}", va="center", fontsize=9, color=TEXT, fontweight="bold")
    bar_ax.set_xlim(0, 220)
    bar_ax.tick_params(labelsize=9, colors=TEXT2)
    bar_ax.spines["left"].set_color("#D9D9D9")
    bar_ax.spines["bottom"].set_color("#D9D9D9")
    for s in ("top", "right"):
        bar_ax.spines[s].set_visible(False)
    bar_ax.set_xlabel("Open work items", fontsize=8, color=TEXT2)

    # ---- Footer ----
    text(ax, 0.4, 0.55, "MOCKUP  ·  Sample data  ·  not real operational figures",
         color=NEUTRAL, fontsize=8, style="italic")

    fig.savefig(IMG_DIR / "01-dashboard-mockup.png", facecolor=PAGE_BG, bbox_inches=None)
    plt.close(fig)
    print("  saved 01-dashboard-mockup.png")


# ---------------------------------------------------------------------------
# 2. KPI card detail
# ---------------------------------------------------------------------------
def kpi_card_detail():
    fig, ax = plt.subplots(figsize=(11, 5), facecolor=PAGE_BG)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5)
    ax.axis("off")

    title_color = TEXT
    fig.suptitle("KPI Card — Anatomy of a Leadership-Ready Tile",
                 fontsize=14, fontweight="bold", color=title_color, y=0.98)

    # Big card
    card(ax, 1.0, 1.2, 4.0, 2.6, fill=CARD_BG, edge="#D9D9D9", lw=1.5)
    text(ax, 1.3, 3.45, "AVG RESOLUTION (DAYS)", color=TEXT2, fontsize=10, fontweight="bold")
    text(ax, 1.3, 2.75, "3.2", color=PRIMARY, fontsize=46, fontweight="bold", va="center")
    text(ax, 1.3, 2.05, "vs 4.0 SLA target", color=GOOD, fontsize=11, fontweight="bold")
    text(ax, 1.3, 1.75, "▲ 0.8 days improvement", color=GOOD, fontsize=10)

    # Sparkline drawn directly on the main ax inside the card (data coords)
    spark_x = [3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4]
    raw_y = [4.2, 4.0, 3.9, 3.7, 3.5, 3.4, 3.3, 3.2]
    # Scale raw_y (3.2..4.2) to a thin sparkline band y=1.35..1.55 inside the card
    y_min, y_max = min(raw_y), max(raw_y)
    spark_y = [1.35 + (y_max - v) / (y_max - y_min) * 0.20 for v in raw_y]
    ax.plot(spark_x, spark_y, color=PRIMARY, linewidth=2.2, zorder=5)
    ax.scatter([spark_x[-1]], [spark_y[-1]], color=PRIMARY, s=22, zorder=6)

    # Annotations
    annotations = [
        (5.5, 3.65, "Title — business-friendly metric name in caps"),
        (5.5, 3.10, "Hero value — large, brand color, single glance"),
        (5.5, 2.55, "Comparison — vs target / prior period / SLA"),
        (5.5, 2.00, "Delta — direction of movement, color-coded"),
        (5.5, 1.45, "Sparkline — short trend at the corner of the eye"),
    ]
    for ax_x, ay, msg in annotations:
        text(ax, ax_x, ay, msg, color=TEXT, fontsize=10)
        ax.annotate("", xy=(5.0, ay), xytext=(5.4, ay),
                    arrowprops=dict(arrowstyle="-", color=NEUTRAL, lw=1))

    # Design rules box
    text(ax, 1.0, 0.7, "DESIGN RULES",
         color=TEXT2, fontsize=8, fontweight="bold")
    rules = "Brand color reserved for hero value  ·  semantic colors for delta  ·  one comparison only  ·  no decorative borders"
    text(ax, 1.0, 0.38, rules, color=TEXT2, fontsize=9, style="italic")

    fig.savefig(IMG_DIR / "02-kpi-card-detail.png", facecolor=PAGE_BG, bbox_inches=None)
    plt.close(fig)
    print("  saved 02-kpi-card-detail.png")


# ---------------------------------------------------------------------------
# 3. Architecture
# ---------------------------------------------------------------------------
def architecture():
    fig, ax = plt.subplots(figsize=(13, 5.5), facecolor="white")
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 5.5)
    ax.axis("off")

    fig.suptitle("Solution Architecture — Source to Dashboard",
                 fontsize=14, fontweight="bold", y=0.97)

    sources = [
        (0.4, 4.1, "Incident\ntracking system"),
        (0.4, 2.7, "Work order\nsystem"),
        (0.4, 1.3, "Reference\ntables"),
    ]
    for x, y, label in sources:
        card(ax, x, y, 2.6, 0.95, fill=LIGHT, edge="#C8C6C4")
        text(ax, x + 1.3, y + 0.475, label, ha="center", va="center",
             color=TEXT, fontsize=10, fontweight="bold")

    # Stage 2 — transform
    card(ax, 4.0, 2.5, 2.6, 1.4, fill=PRIMARY, edge=PRIMARY)
    text(ax, 5.3, 3.45, "Power Query",
         ha="center", color="white", fontsize=10, fontweight="bold")
    text(ax, 5.3, 3.18, "ETL + cleansing", ha="center", color="#C5D5E8", fontsize=9)
    text(ax, 5.3, 2.85, "▾", ha="center", color="#C5D5E8", fontsize=14)
    text(ax, 5.3, 2.65, "Star schema", ha="center", color="#C5D5E8", fontsize=9)

    # Stage 3 — model
    card(ax, 7.6, 2.5, 2.6, 1.4, fill=TEAL, edge=TEAL)
    text(ax, 8.9, 3.45, "Semantic model",
         ha="center", color="white", fontsize=10, fontweight="bold")
    text(ax, 8.9, 3.18, "DAX measures", ha="center", color="#C5D5E8", fontsize=9)
    text(ax, 8.9, 2.85, "▾", ha="center", color="#C5D5E8", fontsize=14)
    text(ax, 8.9, 2.65, "KPI definitions", ha="center", color="#C5D5E8", fontsize=9)

    # Stage 4 — dashboard
    card(ax, 11.2, 2.5, 1.6, 1.4, fill=GOOD, edge=GOOD)
    text(ax, 12.0, 3.45, "Dashboard",
         ha="center", color="white", fontsize=10, fontweight="bold")
    text(ax, 12.0, 3.18, "Power BI", ha="center", color="#C5E6D8", fontsize=9)
    text(ax, 12.0, 2.85, "▾", ha="center", color="#C5E6D8", fontsize=14)
    text(ax, 12.0, 2.65, "Executive UI", ha="center", color="#C5E6D8", fontsize=9)

    # Arrows from sources to Power Query
    for _, sy, _ in sources:
        arr = FancyArrowPatch((3.0, sy + 0.475), (4.0, 3.2),
                              arrowstyle="->,head_width=0.18,head_length=0.25",
                              color=NEUTRAL, linewidth=1.6, mutation_scale=10)
        ax.add_patch(arr)

    # Arrows between stages
    for x1, x2 in [(6.6, 7.6), (10.2, 11.2)]:
        arr = FancyArrowPatch((x1, 3.2), (x2, 3.2),
                              arrowstyle="->,head_width=0.20,head_length=0.30",
                              color=NEUTRAL, linewidth=2, mutation_scale=12)
        ax.add_patch(arr)

    text(ax, 6.5, 1.5,
         "Source data → ETL → Semantic model → Dashboard",
         ha="center", color=TEXT2, fontsize=11, style="italic")
    text(ax, 6.5, 1.0,
         "Same architecture supports future operational data sources",
         ha="center", color=TEXT2, fontsize=9, style="italic")

    fig.savefig(IMG_DIR / "03-architecture.png", facecolor="white", bbox_inches=None)
    plt.close(fig)
    print("  saved 03-architecture.png")


# ---------------------------------------------------------------------------
# 4. Before / after
# ---------------------------------------------------------------------------
def before_after():
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), facecolor="white")
    fig.suptitle("Before vs After — Operational Reporting Process",
                 fontsize=15, fontweight="bold", y=0.98)

    BEFORE = {
        "color": BAD,
        "title": "BEFORE — Fragmented manual reporting",
        "items": [
            ("LAG",      "2-3 days lag",        "Manual consolidation each cycle"),
            ("FILES",    "5+ source files",     "Spreadsheets, system exports, emails"),
            ("RISK",     "Inconsistent KPIs",   "Each team interpreted metrics differently"),
            ("CADENCE",  "Ad-hoc cadence",      "Reporting timing varied by request"),
            ("VIEW",     "Limited visibility",  "Leadership saw a partial view"),
        ],
    }
    AFTER = {
        "color": GOOD,
        "title": "AFTER — Centralized executive dashboard",
        "items": [
            ("FAST",     "Near-real-time",       "Refresh runs nightly, on-demand available"),
            ("UNIFIED",  "One source of truth",  "All operational data in a single model"),
            ("STANDARD", "Standardized KPIs",    "Consistent definitions across teams"),
            ("CYCLE",    "Repeatable cadence",   "Predictable refresh + delivery cadence"),
            ("VISIBLE",  "Full visibility",      "Leadership sees zones, trends, backlog"),
        ],
    }

    for ax, side in zip(axes, [BEFORE, AFTER]):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis("off")
        ax.set_title(side["title"], fontsize=12, fontweight="bold",
                     color=side["color"], pad=14)

        for i, (tag, headline, detail) in enumerate(side["items"]):
            y = 8.4 - i * 1.55
            card(ax, 0.3, y - 0.55, 9.4, 1.15, fill=LIGHT, edge="#E1DFDD")
            # Tag pill on the left
            card(ax, 0.55, y - 0.25, 1.55, 0.5, fill=side["color"], edge=side["color"])
            text(ax, 1.325, y, tag, ha="center", va="center",
                 color="white", fontsize=10, fontweight="bold")
            text(ax, 2.4, y + 0.20, headline, color=TEXT,
                 fontsize=11, fontweight="bold")
            text(ax, 2.4, y - 0.20, detail, color=TEXT2, fontsize=10)

    fig.savefig(IMG_DIR / "04-before-after.png", facecolor="white", bbox_inches=None)
    plt.close(fig)
    print("  saved 04-before-after.png")


def main():
    print("Generating Executive Operations Dashboard visuals...")
    dashboard_mockup()
    kpi_card_detail()
    architecture()
    before_after()
    print(f"\nAll visuals saved to {IMG_DIR}")


if __name__ == "__main__":
    main()
