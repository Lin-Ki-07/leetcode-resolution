"""Generate an animated walkthrough of the visited-set solution."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
OUT = HERE / "visited-cycle.gif"
NODES = ["A", "B", "C", "D"]
X = [105, 285, 465, 645]
Y = 105
STEPS = [0, 1, 2, 3, 1]


def font(size):
    candidates = [
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def frame(step):
    im = Image.new("RGB", (760, 360), "#ffffff")
    d = ImageDraw.Draw(im)
    title = font(25)
    body = font(19)
    # The arrows model next references. D.next returns to B.
    for i in range(3):
        d.line((X[i] + 48, Y, X[i + 1] - 50, Y), fill="#64748b", width=3)
        d.polygon([(X[i + 1] - 50, Y), (X[i + 1] - 62, Y - 7), (X[i + 1] - 62, Y + 7)], fill="#64748b")
    d.line([(X[3], Y + 48), (X[3], 210), (X[1], 210), (X[1], Y + 52)], fill="#64748b", width=3, joint="curve")
    d.polygon([(X[1], Y + 49), (X[1] - 7, Y + 62), (X[1] + 7, Y + 62)], fill="#64748b")

    seen = set(STEPS[:step])
    current = STEPS[step]
    for i, (name, x) in enumerate(zip(NODES, X)):
        color = "#f5d0b5" if i == current else "#dbeafe" if i in seen else "#f1f5f9"
        d.ellipse((x - 46, Y - 46, x + 46, Y + 46), fill=color, outline="#475569", width=2)
        d.text((x, Y - 12), name, fill="#0f172a", font=title, anchor="mt")
        if i == current:
            d.text((x, Y - 78), "now", fill="#9a3412", font=body, anchor="mt")
            d.line((x, Y - 54, x, Y - 47), fill="#9a3412", width=2)

    visited = "、".join(NODES[i] for i in STEPS[:step]) or "空"
    d.rounded_rectangle((32, 235, 728, 340), radius=8, fill="#f8fafc", outline="#cbd5e1", width=2)
    d.text((52, 247), f"第 {step + 1} 轮  ·  当前节点 {NODES[current]}", fill="#0f172a", font=body)
    d.text((52, 276), f"检查前 visited：{visited}", fill="#334155", font=body)
    action = f"{NODES[current]} 已访问 → 返回入口 B" if current in seen else f"{NODES[current]} 未访问 → 加入集合，沿 next 移动"
    d.text((52, 307), action, fill="#9a3412" if current in seen else "#334155", font=body)
    return im


def main():
    frames = [frame(i) for i in range(len(STEPS))]
    frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=[1100] * 4 + [2200], loop=0, optimize=True)
    print(OUT)


if __name__ == "__main__":
    main()
