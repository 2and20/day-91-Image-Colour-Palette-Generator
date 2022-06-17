from flask import Flask, render_template, request
import numpy as np
from PIL import Image, ImageDraw
# from scipy import misc
from collections import Counter
from math import floor


app = Flask(__name__)


def process(im_array, im, bucketing):
    x = im_array.shape[0]
    print(f"x is: {x}, x type is: {type(x)}")
    y = im_array.shape[1]
    color_list = []
    addon = floor((255 - floor(255 / bucketing) * bucketing) / 2)
    for x_elem in range(x):
        for y_elem in range(y):
            # print(f"im_array[x_elem][y_elem] is: {im_array[x_elem][y_elem]} and"
            #       f"of type: {type(im_array[x_elem][y_elem])}")
            r=(floor(im_array[x_elem][y_elem][1] / bucketing) * bucketing) + addon
            g=(floor(im_array[x_elem][y_elem][1] / bucketing) * bucketing) + addon
            b=(floor(im_array[x_elem][y_elem][2] / bucketing) * bucketing) + addon

            # g=floor(im_array[x_elem][y_elem][1]/20)+10
            # g=round(im_array[x_elem][y_elem][1], -1)
            # b=round(im_array[x_elem][y_elem][2], -1)
            color_element = (r,g,b)
            # print(f"first in color_element is {color_element[0]} and of type {type(color_element[0])}")
            color_list.append(color_element)
            # print(color_element)
    count_list = Counter(color_list)
    res=count_list.most_common(10)
    common_colors = []
    for rgb in res:
        common_colors.append(rgb) # makes rgb list
    print(f"The most common color codes are: {res}"
          f"\n in simple list form common_colors: {common_colors}")
    common_colors=[]
    for rgb in res: # turns rgb common list to hex
        hexy = [f'{i:02x}' for i in rgb[0]]
        hex = "#" + hexy[0] + hexy[1] + hexy[2]
        common_colors.append(hex)
    return common_colors




@app.route("/", methods=["GET","POST"])
def homepage():
    if request.method == "POST":
        img = "simple-colors-small.png"
        bucketing = 10
        # print(img)
        print(f"image type: {type(img)}")
        im = Image.open(img)
        print(f"img size in PIL: {im.size[1]}")
        print(im)
        ImageDraw.Draw(im)
        im.show()
        im_array = np.asarray(im)
        print(im_array)
        print(im_array.shape)
        print(f"array type is: {type(im_array.shape)}")
        print(f"first element in im_array.shape is: {im_array.shape[0]} and "
              f"the type is: {type(im_array.shape[0])}")
        common_colors = process(im_array, im, bucketing)
        return render_template("index.html", common_colors=common_colors)
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)


