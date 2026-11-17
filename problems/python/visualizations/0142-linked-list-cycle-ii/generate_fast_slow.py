"""Render the two phases of Floyd's cycle detection as a GIF."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


OUT = Path(__file__).resolve().parent / "fast-slow-cycle.gif"
X = [105, 285, 465, 645]
Y = 105
NODES = "ABCD"
FRAMES = [
    (0, 0, "开始：两个指针都在 A"),
    (1, 2, "第 1 轮：slow 到 B，fast 到 C"),
    (2, 1, "第 2 轮：slow 到 C，fast 到 B"),
    (3, 3, "第 3 轮：在 D 相遇"),
    (0, 3, "重置：slow 回到 A，fast 留在 D"),
    (1, 1, "同速走 1 步：在入口 B 相遇"),
]


def font(size):
    path = Path("C:/Windows/Fonts/msyh.ttc")
    return ImageFont.truetype(str(path), size) if path.exists() else ImageFont.load_default()


def draw_frame(slow, fast, caption):
    image = Image.new("RGB", (760, 320), "white")
    d = ImageDraw.Draw(image)
    label, node = font(19), font(25)
    for i in range(3):
        d.line((X[i] + 48, Y, X[i + 1] - 50, Y), fill="#64748b", width=3)
        d.polygon([(X[i + 1] - 50, Y), (X[i + 1] - 62, Y - 7), (X[i + 1] - 62, Y + 7)], fill="#64748b")
    d.line([(X[3], Y + 48), (X[3], 205), (X[1], 205), (X[1], Y + 52)], fill="#64748b", width=3)
    d.polygon([(X[1], Y + 49), (X[1] - 7, Y + 62), (X[1] + 7, Y + 62)], fill="#64748b")
    for i, x in enumerate(X):
        d.ellipse((x - 46, Y - 46, x + 46, Y + 46), fill="#f1f5f9", outline="#475569", width=2)
        d.text((x, Y - 12), NODES[i], fill="#0f172a", font=node, anchor="mt")
    # Place the labels side by side when the pointers coincide.
    if slow == fast:
        d.text((X[slow] - 24, Y - 82), "slow", fill="#1d4ed8", font=label, anchor="mt")
        d.text((X[fast] + 25, Y - 82), "fast", fill="#b45309", font=label, anchor="mt")
    else:
        d.text((X[slow], Y - 82), "slow", fill="#1d4ed8", font=label, anchor="mt")
        d.text((X[fast], Y + 53), "fast", fill="#b45309", font=label, anchor="mt")
    d.rounded_rectangle((32, 230, 728, 300), radius=8, fill="#f8fafc", outline="#cbd5e1", width=2)
    d.text((52, 248), caption, fill="#334155", font=label)
    return image


def main():
    frames = [draw_frame(*item) for item in FRAMES]
    frames[0].save(OUT, save_all=True, append_images=frames[1:], duration=[1100, 1100, 1100, 1600, 1500, 2300], loop=0, optimize=True)
    print(OUT)


if __name__ == "__main__":
    main()
