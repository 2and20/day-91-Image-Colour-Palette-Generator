from flask import Flask, render_template, request
import numpy as np
from PIL import Image, ImageDraw
# from scipy import misc
from collections import Counter
from math import floor
import shutil
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = ""

def process(im_array, im, bucketing):
    x = im_array.shape[0]
    print(f"x is: {x}, x type is: {type(x)}")
    y = im_array.shape[1]
    color_list = []
    addon = floor((255 - floor(255 / bucketing) * bucketing) / 2) # just evens out bucketing
    for x_elem in range(x):
        for y_elem in range(y):
            # print(f"im_array[x_elem][y_elem] is: {im_array[x_elem][y_elem]} and"
            #       f"of type: {type(im_array[x_elem][y_elem])}")
            r=(floor(im_array[x_elem][y_elem][0] / bucketing) * bucketing) + addon
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
        common_colors.append(rgb[0]) # makes rgb list, drops frequency
    print(f"The most common color codes are: {res}"
          f"\n in simple list form common_colors: {common_colors}")
    common_colors=[]
    common_colors_rgb=[]
    for rgb in res: # turns rgb common list to hex
        common_colors_rgb.append(rgb[0])
        hexy = [f'{i:02x}' for i in rgb[0]]
        hex = "#" + hexy[0] + hexy[1] + hexy[2]
        common_colors.append(hex)
    print(f"common_colors_rgb is: {common_colors_rgb}")
    return common_colors





@app.route("/", methods=["GET","POST"])
def homepage():
    if request.method == "POST":
        # img1 = request.files.get("colorfile")
        img1 = request.files["colorfile"]
        # print(f"img1.read() is: {img1.read()}")
        bucketing = int(request.form.get("bucketing"))
        # print(img1)
        print(f"image type: {type(img1)}")
        im = Image.open(img1)
        filename = secure_filename(img1.filename)
        print(f"filename is: {filename}")
        print(f"img1.read() is: {img1.read()}")
        img1.save("img_save2.png")
        # with open("img_save.png", "wb") as write_im:
        #     write_im.write(img1.read())
        print(f"img1 size in PIL: {im.size[1]}")
        print(f"im is: {im}")
        ImageDraw.Draw(im)
        im.show()
        im_array = np.asarray(im)
        # print(im_array)
        print(im_array.shape)
        print(f"array type is: {type(im_array.shape)}")
        print(f"first element in im_array.shape is: {im_array.shape[0]} and "
              f"the type is: {type(im_array.shape[0])}")
        common_colors = process(im_array, im, bucketing)
        return render_template("index.html", common_colors=common_colors, bucketing=bucketing)
    return render_template("index.html", bucketing=10) # default for web display set here


if __name__ == '__main__':
    app.run(debug=True)


