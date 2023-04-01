import os

import PIL.ImageDraw2
from PIL import Image, ImageOps
# 遍历文件，将所有文件的路径放入一个列表里
def file_walk(root_path):
    file_list = []
    for dirPath, dirNames, fileNames in os.walk(root_path):
        for fileName in fileNames:
            if fileName.lower().endswith('.webp'):
                filePath = os.path.join(dirPath, fileName)
                file_list.append(filePath)
    return file_list


def webp2png(file_list):
    for srcImagePath in file_list:
        image = Image.open(srcImagePath)
        image = ImageOps.exif_transpose(image)
        dstImagePath = os.path.splitext(srcImagePath)[0] + '.png'
        image.save(dstImagePath)
        print('%s ---> %s' % (srcImagePath, dstImagePath))


if __name__ == '__main__':
    imagePath = "C:\\Users\\admin\Desktop\\need"
    image_list = file_walk(imagePath)
    webp2png(image_list)

    # input('按回车键退出')  # 打包之后避免执行完程序后窗口立刻关闭的问题
