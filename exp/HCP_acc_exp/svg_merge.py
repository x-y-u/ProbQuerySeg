"""
    coding: utf-8
    Project: Fiber_Query
    File: svg_merge.py
    Author: xieyu
    Date: 2025/10/30 17:48
    IDE: PyCharm
"""

import svgutils.transform as sg
import cairosvg
import re

def merge_svgs_to_png(svg_paths, out_png_path="merged.png", direction="vertical", dpi=300):
    svgs = [sg.fromfile(p) for p in svg_paths]
    roots = [s.getroot() for s in svgs]

    sizes = []
    for s in svgs:
        w = s.root.get("width")
        h = s.root.get("height")
        print(w, h)

        # 🧩 如果缺失 width/height，则从 viewBox 提取
        if not w or not h:
            viewbox = s.root.get("viewBox")
            if viewbox:
                _, _, w, h = map(float, viewbox.split())
            else:
                # 默认值（单位像素）
                print(1)
                w, h = 1000.0, 800.0
        else:
            w = float(re.sub(r"[a-zA-Z]", "", w))
            h = float(re.sub(r"[a-zA-Z]", "", h))

        sizes.append((w, h))

    if direction == "vertical":
        width = max(w for w, _ in sizes)
        height = sum(h for _, h in sizes)
        print(width, height)
        fig = sg.SVGFigure(f"{width}pt", f"{height}pt")

        y_offset = 0
        for root, (_, h) in zip(roots, sizes):
            root.moveto(0, y_offset)
            y_offset += h
        fig.append(roots)
    else:
        pass

    fig.root.set("viewBox", f"0 0 {width} {height}")

    # 临时文件保存
    temp_svg = "/media/UG3/xieyu/fiber_query/HCP/temp_merged.eps"
    fig.save(temp_svg)

    # ✅ 输出为 PNG
    # cairosvg.svg2png(url=temp_svg, write_to=out_png_path, dpi=dpi)
    # print(f"✅ 拼接完成并导出为：{out_png_path}")


def main():


    # 示例使用
    merge_svgs_to_png(["/media/UG3/xieyu/fiber_query/HCP/per_class_Volume_Precision_line.svg", "/media/UG3/xieyu/fiber_query/HCP/per_class_Volume_OR_line.svg"], "/media/UG3/xieyu/fiber_query/HCP/merged_Precision_OR.png", direction="vertical", dpi=600)

    pass


if __name__ == '__main__':
    main()
