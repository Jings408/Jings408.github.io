#!/usr/bin/env python3
"""Generate the website figures and the point-mass animation from recorded data."""
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[2]          # repository root
SITE = Path(__file__).resolve().parents[1]          # website/
FIG = SITE / "assets/figures"
MEDIA = SITE / "assets/media"
FIG.mkdir(parents=True, exist_ok=True)
MEDIA.mkdir(parents=True, exist_ok=True)

font_path = Path("/usr/share/fonts/windows/NotoSansSC-VF.ttf")
if font_path.exists():
    font_manager.fontManager.addfont(str(font_path))
    family = font_manager.FontProperties(fname=str(font_path)).get_name()
else:
    family = "sans-serif"

TEAL, BLUE, AMBER, GREY, INK = "#16877e", "#385e85", "#c9822f", "#9caeb9", "#25364a"
plt.rcParams.update({
    "font.family": family,
    "font.size": 11.0,
    "axes.unicode_minus": False,
    "svg.fonttype": "path",
    "text.color": INK,
    "axes.labelcolor": INK,
    "xtick.color": "#536476",
    "ytick.color": "#536476",
    "axes.edgecolor": "#cbd7db",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "grid.color": "#e4ebee",
})


def clean(ax):
    ax.grid(axis="y", color="#e4ebee", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)


# ---------------------------------------------------------------- book disk
disk = ROOT / "runs/non_rgb_overnight_20261101_HIhnEVgJ/book_disk/training_curves.csv"
fit = json.load((ROOT / "runs/non_rgb_overnight_20261101_HIhnEVgJ/book_disk/fit_diagnostics.json").open())
rows = [r for r in csv.DictReader(disk.open(encoding="utf-8-sig")) if r["dataset"] == "ordinary"]
scenarios = ["constant_n128", "constant_n512", "constant_n2048",
             "varying_n128", "varying_n512", "varying_n2048"]
routes = [("direct_D", "Direct D", TEAL), ("identified_model", "Identified", BLUE), ("GMM", "GMM", AMBER)]

fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.0), layout="constrained")
const_last = {}
for prefix, linestyle in [("constant", "-"), ("varying", "--")]:
    for route, label, color in routes:
        xs, ys = [], []
        for sc in scenarios:
            if not sc.startswith(prefix):
                continue
            for x in fit:
                if x["scenario"] == sc and x["route"] == route and x["dataset"] == "ordinary":
                    info = x["diagnostics"].get("information", {})
                    if "condition_number" in info:
                        xs.append(x["samples"])
                        ys.append(info["condition_number"])
        if not xs:
            continue
        order = np.argsort(xs)
        xs = np.array(xs)[order]
        ys = np.array(ys)[order]
        axes[0].plot(xs, ys, marker="o", markersize=4.5, linewidth=2.0,
                     linestyle=linestyle, color=color)
        if prefix == "constant":
            const_last[route] = (xs[-1], ys[-1])
axes[0].set_xscale("log", base=2)
axes[0].set_yscale("log")
axes[0].set_xticks([128, 512, 2048], ["128", "512", "2048"])
axes[0].set_xlabel("训练转移数 (s, a, s')")
axes[0].set_ylabel("条件数")
axes[0].set_title("条件数（实线 constant / 虚线 varying）", fontsize=10.5, pad=8)
clean(axes[0])
for route, label, color in routes:
    x, y = const_last[route]
    axes[0].annotate(label, (x, y), xytext=(6, 0), textcoords="offset points",
                     va="center", fontsize=9, color=color)
axes[0].set_xlim(105, 3600)

for route, label, color in routes:
    xs, ys = [], []
    for sc in scenarios:
        if not sc.startswith("varying"):
            continue
        for r in rows:
            if r["scenario"] == sc and r["route"] == route:
                xs.append(int(r["samples"]))
                ys.append(float(r["validation_true_D_rmse"]))
    order = np.argsort(xs)
    axes[1].plot(np.array(xs)[order], np.array(ys)[order], marker="o", markersize=4.5,
                 linewidth=2.0, color=color)
axes[1].set_xscale("log", base=2)
axes[1].set_yscale("log")
axes[1].set_xticks([128, 512, 2048], ["128", "512", "2048"])
axes[1].set_xlabel("训练转移数 (s, a, s')")
axes[1].set_ylabel("验证 D RMSE")
axes[1].set_title("varying：验证 D RMSE", fontsize=10.5, pad=8)
clean(axes[1])

fig.suptitle("圆盘：数据预算、条件数与验证误差", fontsize=13, color=INK, y=1.03)
fig.text(0.5, -0.02, "每档 128 / 512 / 2048 条转移；验证集独立采样",
         ha="center", va="bottom", fontsize=9.5, color="#5f7180")
fig.savefig(FIG / "book_disk_training.svg", bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- book grid
pi = json.load((ROOT / "runs/non_rgb_overnight_20261101_HIhnEVgJ/book_grid/POLICY_ITERATION.json").open())
fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.5), layout="constrained")
for key, label, color in [("reward", "Reward", TEAL), ("constrained", "Constrained", AMBER)]:
    it = [p["iteration"] for p in pi[key]]
    axes[0].plot(it, [p["mean_value"] for p in pi[key]], marker="o", linewidth=2.2,
                 markersize=5, color=color, label=label)
    axes[1].plot(it, [p["bellman_improvement_residual"] for p in pi[key]], marker="o",
                 linewidth=2.2, markersize=5, color=color, label=label)
axes[0].set_xlabel("迭代轮次")
axes[0].set_ylabel("平均价值")
axes[0].set_title("Mean value", fontsize=11, pad=8)
axes[1].set_xlabel("迭代轮次")
axes[1].set_ylabel("Bellman 改进残差")
axes[1].set_yscale("log")
axes[1].set_title("Bellman residual", fontsize=11, pad=8)
for ax in axes:
    clean(ax)
axes[1].legend(frameon=False, fontsize=9, loc="center right")
fig.suptitle("95 状态网格：策略迭代", fontsize=13, color=INK, y=1.03)
fig.savefig(FIG / "book_grid_policy_iteration.svg", bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- RGB validation
prov = json.load((ROOT / "runs/rgb_representation_v2_20261030_z9RNX5Ou/figures_01/PROVENANCE.json").open())
fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.7), layout="constrained")
for key, label, color in [("old", "旧 AE", BLUE), ("new", "新 AE", TEAL)]:
    pts = prov[key]["points"]
    x = [p["round"] for p in pts]
    succ = [p["successes"] for p in pts]
    axes[0].plot(x, succ, marker="o", linewidth=2.2, markersize=5, color=color)
    axes[1].plot(x, [p["mean_integrated_error"] for p in pts], marker="o", linewidth=2.2,
                 markersize=5, color=color)
    axes[0].annotate(label, (x[-1], succ[-1]), xytext=(6, 0), textcoords="offset points",
                     va="center", fontsize=9, color=color)
axes[0].set_xlabel("训练轮次")
axes[0].set_ylabel("成功数 / 24")
axes[0].set_title("验证成功数", fontsize=11, pad=8)
axes[0].set_xlim(2, 29)
axes[1].set_xlabel("训练轮次")
axes[1].set_ylabel("平均积分误差")
axes[1].set_title("平均积分误差", fontsize=11, pad=8)
for ax in axes:
    clean(ax)
fig.suptitle("RGB 验证曲线：旧 / 新 AE", fontsize=13, color=INK, y=1.03)
fig.savefig(FIG / "rgb_validation.svg", bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- Push PPO return
from matplotlib.lines import Line2D

push_root = ROOT / "runs/non_rgb_overnight_20261101_HIhnEVgJ"
push_seeds = [
    ("seed81", push_root / "push_so101/train/TRAINING.json",
     push_root / "push_so101/train/FROZEN.json", TEAL),
    ("seed82", push_root / "push_extra_seeds/train_seed82/TRAINING.json",
     push_root / "push_extra_seeds/train_seed82/FROZEN.json", BLUE),
    ("seed83", push_root / "push_extra_seeds/train_seed83/TRAINING.json",
     push_root / "push_extra_seeds/train_seed83/FROZEN.json", AMBER),
]


def rolling(y, w=25):
    return np.convolve(y, np.ones(w) / w, mode="valid")


fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.2))
fig.subplots_adjust(top=0.80, bottom=0.20, left=0.08, right=0.98, wspace=0.28)
handles, labels = [], []
for name, train_path, frozen_path, color in push_seeds:
    data = json.load(train_path.open())
    steps = np.arange(1, len(data) + 1) * 2048
    ret = np.array([np.mean([e["reward"] for e in u["episodes"]]) for u in data])
    sec = np.array([np.mean([e["seconds"] for e in u["episodes"]]) for u in data])

    axes[0].plot(steps, ret, color=color, alpha=0.18, linewidth=0.8)
    axes[1].plot(steps, sec, color=color, alpha=0.18, linewidth=0.8)
    line, = axes[0].plot(steps[24:], rolling(ret), color=color, linewidth=2.2)
    axes[1].plot(steps[24:], rolling(sec), color=color, linewidth=2.2)
    handles.append(line)
    labels.append(name)

    selected = json.load(frozen_path.open())["selected_update"]
    sel_step = selected * 2048
    for ax in axes:
        ax.axvline(sel_step, color=color, linestyle=":", linewidth=1.1, alpha=0.55)
    idx = min(max(selected - 25, 0), len(rolling(ret)) - 1)
    axes[0].scatter([sel_step], [rolling(ret)[idx]], color=color, s=38, zorder=5,
                    edgecolors="white", linewidths=0.8)

for ax, title, ylabel in [
        (axes[0], "平均回合回报", "回报"),
        (axes[1], "平均回合时长", "秒")]:
    ax.set_xlabel("环境步数")
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontsize=11, pad=8)
    ax.set_xlim(0, 2_100_000)
    ax.set_xticks([0, 500_000, 1_000_000, 1_500_000, 2_000_000],
                  ["0", "0.5M", "1.0M", "1.5M", "2.0M"])
    clean(ax)
axes[0].set_ylim(160, 178)
axes[1].set_ylim(22, 36)
fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.92),
           ncol=3, frameon=False, fontsize=9.5)
fig.suptitle("Push Full-M PPO：步数 vs 回报", fontsize=13, color=INK, y=0.99)
fig.savefig(FIG / "push_ppo_return.svg", bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- point-mass animation
from matplotlib.animation import FFMpegWriter

plt.rcParams["animation.ffmpeg_path"] = "/usr/bin/ffmpeg"
dt, T = 0.05, 6.0
steps = int(T / dt)
kp, kd, umax = 4.0, 3.4, 1.6
x = np.array([2.0, 1.2])
v = np.array([0.0, 0.0])
traj = [x.copy()]
for _ in range(steps):
    u = np.clip(-kp * x - kd * v, -umax, umax)
    v = v + u * dt
    x = x + v * dt
    traj.append(x.copy())
traj = np.array(traj)

fig, ax = plt.subplots(figsize=(9.6, 5.4), dpi=100, facecolor="#f6fafb")
ax.set_facecolor("#f6fafb")
ax.set_xlim(-0.4, 2.4)
ax.set_ylim(-0.4, 1.7)
ax.set_aspect("equal", adjustable="box")
ax.set_xticks([]); ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)
ax.axhline(0, color="#d7e0e4", linewidth=1.0)
ax.axvline(0, color="#d7e0e4", linewidth=1.0)
ax.scatter([0], [0], s=90, facecolors="none", edgecolors=AMBER, linewidths=2.0, zorder=3)
ax.scatter([traj[0, 0]], [traj[0, 1]], s=70, facecolors="none", edgecolors=BLUE,
           linewidths=2.0, zorder=3)
ax.text(0.03, 0.06, "目标", color=AMBER, fontsize=11)
ax.text(traj[0, 0] + 0.05, traj[0, 1] + 0.07, "起点", color=BLUE, fontsize=11)
ax.text(0.03, 1.54, "二维双积分器 · PD 控制示意", color=INK, fontsize=15, weight="bold")
ax.text(0.03, 1.38, "x'' = u,  u = -Kp x - Kd v", color="#536476", fontsize=11)
point, = ax.plot([], [], "o", color=TEAL, markersize=12, zorder=4)
trail, = ax.plot([], [], color=TEAL, linewidth=2.2, alpha=0.6, zorder=2)


def init():
    point.set_data([], [])
    trail.set_data([], [])
    return point, trail


def update(i):
    point.set_data([traj[i, 0]], [traj[i, 1]])
    start = max(0, i - 60)
    trail.set_data(traj[start:i + 1, 0], traj[start:i + 1, 1])
    return point, trail


anim = matplotlib.animation.FuncAnimation(fig, update, frames=len(traj), init_func=init,
                                         interval=1000 * dt, blit=True)
writer = FFMpegWriter(fps=int(1 / dt), codec="libx264", bitrate=2200,
                      extra_args=["-pix_fmt", "yuv420p", "-movflags", "+faststart"])
anim.save(MEDIA / "point_mass.mp4", writer=writer, dpi=100)
update(30)
fig.savefig(MEDIA / "point_mass_poster.png", dpi=100, bbox_inches="tight")
plt.close(fig)

print("figures:", sorted(p.name for p in FIG.glob("*.svg")))
print("media:", sorted(p.name for p in MEDIA.glob("*")))
