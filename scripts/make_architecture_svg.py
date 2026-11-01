#!/usr/bin/env python3
"""Generate a five-panel architecture figure for the toolbox (pure SVG)."""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parents[1] / "assets/diagrams"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 2000, 1050
INK = "#25364a"
MUTED = "#5f7180"
TEAL = "#0f766e"
BLUE = "#385e85"
AMBER = "#b7791f"
PURPLE = "#6b4fa0"
BOX_STROKE = "#9fb3c8"
FONT = "Noto Sans SC, Microsoft YaHei, sans-serif"

P = []
P.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">')
P.append('''<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="#5f7180"/>
  </marker>
  <marker id="arrow-teal" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="#0f766e"/>
  </marker>
  <marker id="arrow-amber" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="#b7791f"/>
  </marker>
</defs>''')
P.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')


def txt(x, y, s, size=15, fill=INK, anchor="middle", weight="400", italic=False, opacity=1.0):
    style = ' font-style="italic"' if italic else ''
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{weight}"{style} opacity="{opacity}">{escape(s)}</text>')


def rect(x, y, w, h, fill="#ffffff", stroke=BOX_STROKE, rx=10, sw=1.4, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def panel(x, y, w, h, num, title, fill, border, header):
    out = [rect(x, y, w, h, fill, border, 16, 1.8)]
    out.append(rect(x, y, w, 54, header, border, 16, 1.8))
    out.append(f'<rect x="{x}" y="{y+32}" width="{w}" height="22" fill="{header}"/>')
    out.append(f'<circle cx="{x+30}" cy="{y+27}" r="17" fill="{TEAL}"/>')
    out.append(txt(x + 30, y + 32, str(num), 17, "#ffffff", weight="700"))
    out.append(txt(x + 58, y + 33, title, 20, INK, "start", "700"))
    return "".join(out)


def box(x, y, w, h, lines, fill="#ffffff", stroke=BOX_STROKE, size=14, bold_first=True, accent=None):
    out = [rect(x, y, w, h, fill, stroke, 10, 1.4)]
    if accent:
        out.append(f'<rect x="{x}" y="{y}" width="5" height="{h}" rx="2.5" fill="{accent}"/>')
    if isinstance(lines, str):
        lines = [lines]
    lh = size + 7
    total = len(lines) * lh
    start = y + h / 2 - total / 2 + size
    for i, line in enumerate(lines):
        weight = "700" if (i == 0 and bold_first) else "400"
        color = INK if i == 0 else MUTED
        out.append(txt(x + w / 2, start + i * lh, line, size, color, weight=weight))
    return "".join(out)


def chip(x, y, w, h, label, fill="#ffffff", stroke=BOX_STROKE, color=INK, size=12):
    return (rect(x, y, w, h, fill, stroke, 8, 1.2)
            + txt(x + w / 2, y + h / 2 + 4, label, size, color, weight="600"))


def stack(x, y, w, h, color="#8ec5e8", n=3):
    out = []
    for i in range(n - 1, -1, -1):
        out.append(rect(x + i * 6, y - i * 6, w, h, color, color, 4, 0.8))
        out.append(f'<line x1="{x+i*6}" y1="{y-i*6+h*0.35}" x2="{x+i*6+w}" y2="{y-i*6+h*0.35}" stroke="#ffffff" stroke-width="1" opacity="0.55"/>')
        out.append(f'<line x1="{x+i*6}" y1="{y-i*6+h*0.7}" x2="{x+i*6+w}" y2="{y-i*6+h*0.7}" stroke="#ffffff" stroke-width="1" opacity="0.55"/>')
    return "".join(out)


def arrow(points, label=None, dashed=False, color="#5f7180", marker="arrow", lx=0, ly=0, lsize=12):
    pts = " ".join(f"{x},{y}" for x, y in points)
    d = ' stroke-dasharray="7 5"' if dashed else ''
    out = [f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2" stroke-linejoin="round"{d} marker-end="url(#{marker})"/>']
    if label:
        mx, my = points[len(points) // 2]
        mx += lx
        my += ly
        w = max(38, len(label) * lsize * 0.78)
        out.append(f'<rect x="{mx-w/2}" y="{my-13}" width="{w}" height="18" rx="4" fill="#ffffff" opacity="0.92"/>')
        out.append(txt(mx, my, label, lsize, MUTED, weight="600"))
    return "".join(out)


# ============================================================ panel 1: Env
P.append(panel(24, 24, 590, 610, 1, "环境层 Env：任务、观测与物理", "#eaf3fb", "#b9d4ee", "#d7e8f8"))
P.append(box(50, 100, 120, 80, ["观测 o_t", "状态 / 图像"], accent=BLUE))
P.append(box(190, 100, 120, 80, ["动作 a_t", "连续 / 离散", "动作边界"], accent=BLUE))
P.append(box(330, 100, 240, 80, ["任务注册表", "9 个注册环境", "+ RGB / 网格 / SO101"], accent=BLUE))
P.append(box(50, 240, 250, 110, ["物理步进", "s_{t+1} = f(s_t, a_t)", "reset / step"], accent=TEAL))
P.append(box(330, 240, 250, 110, ["成本与判据", "cost", "terminated / truncated", "success / hold"], accent=TEAL))
P.append(arrow([(110, 180), (110, 240)], "观测"))
P.append(arrow([(250, 180), (250, 240)], "动作"))
P.append(arrow([(450, 180), (450, 240)], "任务"))
P.append(arrow([(300, 295), (330, 295)], "s'"))

P.append(stack(500, 330, 52, 46, "#9ecae1"))
P.append(txt(526, 390, "图像观测", 12, MUTED))

tasks = ["状态控制", "机器人", "观测器", "RGB", "Push", "网格"]
for i, name in enumerate(tasks):
    x = 50 + (i % 3) * 180
    y = 430 + (i // 3) * 58
    P.append(chip(x, y, 160, 40, name))
P.append(arrow([(175, 350), (175, 430)], None, True))
P.append(txt(295, 560, "Env 只负责真实物理与任务判据，不依赖 Algo / Runner", 13, MUTED, "start"))
P.append(txt(295, 582, "所有任务返回正成本；奖励转换放在算法侧", 13, MUTED, "start"))

# ============================================================ panel 2: Algo
P.append(panel(630, 24, 630, 610, 2, "算法层 Algo：度量、策略与证书", "#fdf1e7", "#efcdb0", "#f8e2cf"))
P.append(box(660, 100, 170, 90, ["编码器 φ(o)", "AE / ResNet / ViT"], accent=AMBER))
P.append(stack(850, 118, 54, 46, "#f0b27a"))
P.append(txt(877, 178, "φ(o)", 12, MUTED))
P.append(box(660, 240, 190, 90, ["可学习度量 M", "M = LLᵀ + εI"], accent=TEAL))
P.append(box(880, 240, 170, 90, ["候选函数 V", "V = ½ eᵀ M e"], accent=TEAL))
P.append(box(660, 370, 190, 90, ["策略 π / Critic Q", "动作分布 / 价值"], accent=BLUE))
P.append(box(880, 370, 170, 90, ["一步下降", "D = V(s') − V(s)"], accent=TEAL))
P.append(box(1080, 100, 160, 260, ["损失与更新", "模型梯度", "PPO / SAC", "导数 Critic", "证书约束"], accent=PURPLE))
P.append(arrow([(745, 190), (745, 240)], "φ"))
P.append(arrow([(850, 285), (880, 285)], "M"))
P.append(arrow([(965, 330), (965, 370)], "V"))
P.append(arrow([(850, 415), (880, 415)], "更新"))
P.append(arrow([(1080, 230), (850, 230)], "∇", True, PURPLE, "arrow"))
P.append(arrow([(1080, 415), (850, 415)], "∇", True, PURPLE, "arrow"))
P.append(arrow([(1080, 145), (830, 145)], "∇", True, PURPLE, "arrow"))

backends = ["state_model_gradient", "episode_ppo", "push_discrete_sac",
            "rgb_legacy", "dc_motor_gradient", "observer_model_gradient"]
for i, name in enumerate(backends):
    x = 660 + (i % 2) * 300
    y = 490 + (i // 2) * 42
    P.append(chip(x, y, 280, 32, name, size=11))
P.append(txt(945, 615, "同一套 Algo 接口；不同后端保留各自的物理与梯度契约", 13, MUTED))

# ============================================================ panel 3: Runner
P.append(panel(1276, 24, 700, 610, 3, "调度层 Runner：可复现训练生命周期", "#eaf6ee", "#bfe0c8", "#d8efdf"))
P.append(box(1300, 100, 220, 70, ["配置", "jobs / backend / seeds"], accent=TEAL))
P.append(box(1300, 195, 220, 70, ["preflight", "schema / 资源 / 初始化"], accent=TEAL))
P.append(box(1300, 290, 220, 70, ["采样 / 预热", "replay / warmup"], accent=TEAL))
P.append(box(1300, 385, 220, 70, ["train", "epoch 更新"], accent=TEAL))
P.append(box(1650, 195, 220, 70, ["validate", "验证集选模"], accent=TEAL))
P.append(box(1650, 290, 220, 70, ["freeze", "全组冻结 / 哈希"], accent=TEAL))
P.append(box(1650, 385, 220, 70, ["test", "独立测试"], accent=TEAL))
P.append(box(1650, 480, 220, 70, ["report", "快照 + 曲线 + 审计"], accent=TEAL))
P.append(box(1650, 100, 220, 70, ["资源门限", "minutes / free GiB"], accent=AMBER))
P.append(arrow([(1410, 170), (1410, 195)], "next"))
P.append(arrow([(1410, 265), (1410, 290)]))
P.append(arrow([(1410, 360), (1410, 385)]))
P.append(arrow([(1520, 420), (1600, 420), (1600, 245), (1650, 245)], "验证"))
P.append(arrow([(1760, 265), (1760, 290)]))
P.append(arrow([(1760, 360), (1760, 385)]))
P.append(arrow([(1760, 455), (1760, 480)]))
P.append(txt(1600, 585, "每个实验新目录；全组冻结后才访问测试集", 13, MUTED))

# ============================================================ panel 4: RGB
P.append(panel(24, 660, 980, 370, 4, "书稿 RGB：从图像到解析控制", "#f3edfb", "#d6c5ee", "#e6dbf7"))
for i, label in enumerate(["I_t", "I*"]):
    x = 50
    y = 735 + i * 95
    P.append(rect(x, y, 110, 78, "#ffffff", "#b9c9d4", 6, 1.2))
    P.append(f'<path d="M{x+8} {y+60} L{x+30} {y+38} L{x+48} {y+52} L{x+70} {y+30} L{x+102} {y+58}" fill="none" stroke="{BLUE}" stroke-width="2"/>')
    P.append(f'<rect x="{x+8}" y="{y+8}" width="18" height="18" fill="#dbeaf4"/>')
    P.append(txt(x + 55, y + 94, label, 13, INK, weight="700"))
P.append(box(190, 760, 150, 80, ["共享 AE φ", "ResNet / 16-d"], accent=PURPLE))
P.append(stack(360, 775, 54, 46, "#c9b6e8"))
P.append(txt(387, 835, "φ(I), φ(I*)", 12, MUTED))
P.append(arrow([(160, 770), (190, 790)], "图像"))
P.append(arrow([(160, 865), (190, 830)], "目标"))
P.append(box(360, 870, 180, 62, ["特征差 e", "e = (φ(I) − φ(I*))/4"], accent=PURPLE, size=13))
P.append(box(360, 950, 150, 62, ["FastDepth", "Ẑ*"], accent=AMBER, size=13))
P.append(box(540, 950, 200, 62, ["交互矩阵 J*", "J* = ¼ ∂φ/∂I · L_I"], accent=AMBER, size=13))
P.append(box(770, 875, 210, 90, ["控制 u", "u = sat(−λH⁻¹J*ᵀMe)"], accent=TEAL, size=13))
P.append(arrow([(235, 800), (360, 800)], "φ"))
P.append(arrow([(160, 900), (300, 900), (300, 981), (360, 981)], "Ẑ*", True))
P.append(arrow([(540, 900), (540, 950)], ""))
P.append(arrow([(540, 870), (770, 905)], "e, J*, M"))
P.append(arrow([(980, 920), (1010, 920)], "action", False, TEAL, "arrow-teal"))


# ============================================================ panel 5: Push / SO101
P.append(panel(1020, 660, 956, 370, 5, "Push / SO101：从标定响应到关节接触", "#fff7e3", "#ecd9a8", "#f8edc9"))
P.append(box(1050, 735, 160, 80, ["形状 / 响应", "标定库"], accent=AMBER, size=13))
P.append(box(1240, 735, 170, 80, ["Full-M PPO", "联合成本"], accent=AMBER, size=13))
P.append(box(1440, 735, 170, 80, ["验证选模", "冻结 M"], accent=TEAL, size=13))
P.append(box(1640, 735, 300, 80, ["SO101 MuJoCo", "关节接触测试"], accent=TEAL, size=13))
P.append(arrow([(1210, 775), (1240, 775)], "train"))
P.append(arrow([(1410, 775), (1440, 775)], "select"))
P.append(arrow([(1610, 775), (1640, 775)], "deploy"))

P.append(rect(1050, 850, 500, 105, "#ffffff", "#e2cf9e", 10, 1.2))
P.append(txt(1070, 880, "联合成本", 14, INK, "start", "700"))
P.append(txt(1070, 906, "J = w_t T/T_ref + w_e ∫E dt + w_s N_switch", 13, MUTED, "start"))
P.append(txt(1070, 930, "    + w_u ∫u² dt + w_f 1_fail − w_g 1_success", 13, MUTED, "start"))

for i, name in enumerate(["push-prepare", "push-train", "push-freeze", "push-test", "push-arm"]):
    P.append(chip(1050 + i * 185, 975, 170, 34, name, size=11))
P.append(txt(1600, 828, "训练 / 标定 / 评价分离", 12, MUTED))

# ============================================================ cross-panel arrows
P.append(arrow([(614, 300), (630, 300)], "观测 / 成本", False, BLUE))
P.append(arrow([(630, 340), (614, 340)], "动作", False, BLUE))
P.append(arrow([(500, 660), (500, 634)], "action", True, TEAL, "arrow-teal"))
P.append(arrow([(1600, 634), (1600, 660)], "train / report", True, TEAL, "arrow-teal"))
P.append(arrow([(1500, 660), (1000, 634)], "M / policy", True, PURPLE, "arrow"))

P.append('</svg>')
(OUT / "architecture.svg").write_text("\n".join(P), encoding="utf-8")
print("wrote", OUT / "architecture.svg")
