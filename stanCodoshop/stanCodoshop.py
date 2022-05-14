"""
File: stanCodoshop.py
Name: Yipin
----------------------------------------------
SC101_Assignment3 Adapted from Nick Parlante's
Ghost assignment by Jerry Liao.
"""

import os
import sys
from simpleimage import SimpleImage



def get_pixel_dist(pixel, red, green, blue):
    """
    Returns a value that refers to the "color distance" between a pixel and a mean RGB value.

    Input:
        pixel (Pixel): the pixel with RGB values to be compared
        red (int): the average red value of the pixels to be compared
        green (int): the average green value of the pixels to be compared
        blue (int): the average blue value of the pixels to be compared

    Returns:
        dist (float): the "color distance" of a pixel to the average RGB value of the pixels to be compared.
    """
    color_distance = ((red-pixel.red)**2+(green-pixel.green)**2+(blue-pixel.blue)**2)**0.5
    return color_distance


def get_average(pixels):
    """
    Given a list of pixels, finds their average red, blue, and green values.

    Input:
        pixels (List[Pixel]): a list of pixels to be averaged

    Returns:
        rgb (List[int]): a list of average red, green, and blue values of the pixels
                        (returns in order: [red, green, blue])
    """
    total_r = 0
    total_g = 0
    total_b = 0
    count = 0
    for n in pixels:
        total_r += n.red
        total_g += n.green
        total_b += n.blue
        count += 1
    avg_r = total_r//count
    avg_g = total_g//count
    avg_b = total_b//count
    c_avg = [avg_r, avg_g, avg_b]

    return c_avg  # list


def get_best_pixel(pixels):
    """
    Given a list of pixels, returns the pixel with the smallest "color distance", which has the closest color to the average.

    Input:
        pixels (List[Pixel]): a list of pixels to be compared
    Returns:
        best (Pixel): the pixel which has the closest color to the average
    """
    p_avg = get_average(pixels)  # list
    lst = []
    for n in pixels:
        color_d = get_pixel_dist(n, p_avg[0], p_avg[1], p_avg[2])
        lst.append((color_d, n))
    b_d, b_p = min(lst, key=lambda t: t[0])  # 需指定t[0],不然系統會在相同b_d時比較b_p，然而b_p是記憶體位址無法比較
    best = [b_p.red, b_p.green, b_p.blue]
    # 用list直接找最小的

    '''
    smallest = float('inf')
    best = []
    for n in pixels:
        color_d = get_pixel_dist(n, p_avg[0], p_avg[1], p_avg[2])
        if color_d < smallest:
            smallest = color_d
    best = [n.red, n.green, n.blue]
    '''

    return best  # list




def solve(images):
    """
    Given a list of image objects, compute and display a Ghost solution image
    based on these images. There will be at least 3 images and they will all
    be the same size.

    Input:
        images (List[SimpleImage]): list of images to be processed
    """
    width = images[0].width
    height = images[0].height
    result = SimpleImage.blank(width, height)
    
    # ----- YOUR CODE STARTS HERE ----- #
    # Write code to populate image and create the 'ghost' effect

    for x in range(width):
        for y in range(height):
            imgs_p = []
            for img in images:
                img_p = img.get_pixel(x, y)
                imgs_p += [img_p]

            closed_p = get_best_pixel(imgs_p)   # list

            result_p = result.get_pixel(x, y)
            result_p.red = closed_p[0]
            result_p.green = closed_p[1]
            result_p.blue = closed_p[2]

    # ----- YOUR CODE ENDS HERE ----- #

    print("Displaying image!")
    result.show()


def jpgs_in_dir(dir):
    """
    (provided, DO NOT MODIFY)
    Given the name of a directory, returns a list of the .jpg filenames
    within it.

    Input:
        dir (string): name of directory
    Returns:
        filenames(List[string]): names of jpg files in directory
    """
    filenames = []
    # 讀 dir 資料夾的檔案
    for filename in os.listdir(dir):
        if filename.endswith('.jpg'):
            filenames.append(os.path.join(dir, filename))
    return filenames


def load_images(dir):
    """
    (provided, DO NOT MODIFY)
    Given a directory name, reads all the .jpg files within it into memory and
    returns them in a list. Prints the filenames out as it goes.

    Input:
        dir (string): name of directory
    Returns:
        images (List[SimpleImages]): list of images in directory
    """
    images = []
    jpgs = jpgs_in_dir(dir)
    for filename in jpgs:
        print("Loading", filename)
        image = SimpleImage(filename)
        images.append(image)
    return images


def main():
    # (provided, DO NOT MODIFY)
    args = sys.argv[1:]
    # We just take 1 argument, the folder containing all the images.
    # The load_images() capability is provided above.
    images = load_images(args[0])
    solve(images)


if __name__ == '__main__':
    main()
