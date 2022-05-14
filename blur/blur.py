"""
File: blur.py
Name:
-------------------------------
This file shows the original image first,
smiley-face.png, and then compare to its
blurred image. The blur algorithm uses the
average RGB values of a pixel's nearest neighbors.
"""

from simpleimage import SimpleImage


def blur(img):
    """
    建立一新照片，與舊照片有相同長與寬
    先以for loop將照片長寬為range
    模糊化表示新pixel為將原pixel與周圍8個pixel平均
    而一張照片會有9個加總情況，8種皆不是9個pixel加總，因此建立第二個for loop
    range皆由-1~2，再透過if判斷，當pixel的位置(x,y)加上(i,j)小於照片(寬,長)，並大於等於0
    即可進行pixel的rgb加總，並以變數c來計算pixel的數量
    最後回傳新照片
    """
    new = SimpleImage.blank(img.width, img.height)
    for x in range(img.width):
        for y in range(img.height):
            r = 0
            g = 0
            b = 0
            c = 0
            # 九宮格的大小
            for i in range(-1,2,1):
                for j in range(-1,2,1):
                    if img.width > i+x >= 0:
                        if img.height > j+y >= 0:
                            p = img.get_pixel(x+i, y+j)
                            r += p.red
                            g += p.green
                            b += p.blue
                            c += 1
            new_p = new.get_pixel(x, y)
            new_p.red = r/c
            new_p.green = g/c
            new_p.blue = b/c
    return new


def main():
    """
    將舊照片藉由blur()模糊化
    再透過for loop調整模糊的程度
    """
    old_img = SimpleImage("images/smiley-face.png")
    old_img.show()

    blurred_img = blur(old_img)
    for i in range(5):
        blurred_img = blur(blurred_img)
    blurred_img.show()


# ---- DO NOT EDIT CODE BELOW THIS LINE ---- #

if __name__ == '__main__':
    main()
