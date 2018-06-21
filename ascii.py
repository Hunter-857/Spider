from PIL import Image
import argparse

ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")


def get_char(r, g, b, alpha = 256):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    unit = (256.0 + 1) / length
    return ascii_char[int(gray / unit)]


# 命令行输入参数处理
parser = argparse.ArgumentParser()
# 输入文件
# parser.add_argument('file')
# 输出文件
parser.add_argument('-o', '--output')
# 输出字符画宽
parser.add_argument('--width')
# 输出字符画高
parser.add_argument('--height')
# 获取参数
args = parser.parse_args()

IMG = 'ascii_dora.png'
WIDTH = args.width
HEIGHT = args.height
OUTPUT = args.output

if __name__ == '__main__':

    im = Image.open(IMG)
    if HEIGHT and WIDTH:
        im = im.resize((WIDTH, HEIGHT), Image.NEAREST)
    else:
        HEIGHT, WIDTH = 80, 80
        im = im.resize((WIDTH, HEIGHT), Image.NEAREST)

    txt = ""

    for i in range(HEIGHT):
        for j in range(WIDTH):
            txt += get_char(*im.getpixel((j, i)))
        txt += '\n'

    print(txt)

    # 字符画输出到文件
    if OUTPUT:
        with open(OUTPUT, 'w') as f:
            f.write(txt)
    else:
        with open("output.txt", 'w') as f:
            f.write(txt)
