"""Create compact animated linked-list diagrams for LeetCode 19."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FONT = Path("C:/Windows/Fonts/msyh.ttc")
YELLOW, BLUE = "#fff0bf", "#cce8ff"
TEAL, ORANGE, DARK, GRAY = "#26a69a", "#e7795f", "#344054", "#b9c0c8"


def font(size):
    return ImageFont.truetype(str(FONT), size) if FONT.exists() else ImageFont.load_default()


def arrow(draw, start, end, color=TEAL, width=3):
    x1, y1 = start
    x2, y2 = end
    draw.line((x1, y1, x2 - 9, y2), fill=color, width=width)
    draw.polygon(((x2, y2), (x2 - 10, y2 - 6), (x2 - 10, y2 + 6)), fill=color)


def node(draw, x, y, label, fill=YELLOW, faded=False):
    outline = GRAY if faded else DARK
    draw.ellipse((x - 31, y - 31, x + 31, y + 31), fill=fill, outline=outline, width=2)
    draw.text((x, y), label, anchor="mm", font=font(25), fill=outline)


def save_gif(frames, name, durations):
    frames[0].save(HERE / name, save_all=True, append_images=frames[1:], duration=durations,
                   loop=0, optimize=False, disposal=2)


def deletion_frame(step):
    image = Image.new("RGB", (680, 250), "white")
    draw = ImageDraw.Draw(image)
    xs, y = (125, 340, 555), 120
    draw.text((32, 20), ("原链表", "找到前驱节点 1", "修改 1.next", "删除后")[step], font=font(22), fill=DARK)
    node(draw, xs[0], y, "1", BLUE if step >= 1 else YELLOW)
    node(draw, xs[1], y, "2", "#f5f5f5" if step == 3 else YELLOW, faded=step == 3)
    node(draw, xs[2], y, "3")
    if step < 2:
        arrow(draw, (xs[0] + 32, y), (xs[1] - 32, y))
    else:
        draw.line(((xs[0] + 20, y - 26), (xs[0] + 60, 69), (xs[2] - 60, 69),
                   (xs[2] - 22, y - 25)), fill=ORANGE, width=4, joint="curve")
        draw.polygon(((xs[2] - 22, y - 25), (xs[2] - 35, y - 30), (xs[2] - 28, y - 42)), fill=ORANGE)
    arrow(draw, (xs[1] + 32, y), (xs[2] - 32, y), GRAY if step == 3 else TEAL)
    if step in (2, 3):
        draw.text((340, 207), "1.next = 2.next", anchor="mm", font=font(20), fill=ORANGE)
    return image


def gap_frame(slow, fast, phase):
    image = Image.new("RGB", (940, 285), "white")
    draw = ImageDraw.Draw(image)
    labels = ("D", "1", "2", "3", "4", "5", "None")
    xs, y = (65, 195, 325, 455, 585, 715, 845), 137
    title = "fast 先走 3 步" if phase == "lead" else "两指针一起走" if phase == "sync" else "slow 在待删节点前"
    draw.text((28, 17), title, font=font(21), fill=DARK)
    for i, (x, label) in enumerate(zip(xs, labels)):
        if i:
            arrow(draw, (xs[i - 1] + 31, y), (x - (31 if i < 6 else 35), y))
        if i == 6:
            draw.text((x, y), label, anchor="mm", font=font(21), fill=DARK)
        else:
            node(draw, x, y, label, BLUE if i == slow else YELLOW)
    for index, name, color, text_y in ((slow, "slow", "#287cb5", 62), (fast, "fast", ORANGE, 222)):
        x = xs[index]
        draw.text((x, text_y), name, anchor="mm", font=font(20), fill=color)
        if text_y < y:
            draw.line((x, text_y + 15, x, y - 35), fill=color, width=3)
        else:
            draw.line((x, y + 35, x, text_y - 16), fill=color, width=3)
    if phase == "done":
        draw.text((585, 266), "删 4：3.next = 4.next", anchor="mm", font=font(19), fill=ORANGE)
    return image


def main():
    save_gif([deletion_frame(i) for i in range(4)], "delete-node.gif", [1100, 1100, 1500, 2000])
    positions = [(0, 0, "lead"), (0, 1, "lead"), (0, 2, "lead"), (0, 3, "lead"),
                 (1, 4, "sync"), (2, 5, "sync"), (3, 6, "done")]
    save_gif([gap_frame(*position) for position in positions], "pointer-gap.gif", [900] * 6 + [2400])


if __name__ == "__main__":
    main()
