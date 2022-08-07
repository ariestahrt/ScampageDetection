from PIL import Image
import numpy as np
import math

def calculate_cosine(arr1, arr2):
    numerator = sum([arr1[i] * arr2[i] for i in range(0, len(arr1))])
    len_vec1 = math.sqrt(sum([x ** 2 for x in arr1]))
    len_vec2 = math.sqrt(sum([x ** 2 for x in arr2]))

    denominator = len_vec1 * len_vec2
    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

# open images

img1 = Image.open('amazon_real.png')
img2 = Image.open('myits_login.png')

# make sure images have same dimensions, use .resize to scale image 2 to match image 1 dimensions
# i am also reducing the shape by half just to save some processing power

img1_reshape = img1.resize((round(img1.size[0]*0.5), round(img1.size[1]*0.5)))
img2_reshape = img2.resize((round(img1.size[0]*0.5), round(img1.size[1]*0.5)))

# convert the images to (R,G,B) arrays

img_array1 = np.array(img1_reshape)
img_array2 = np.array(img2_reshape)

# flatten the arrays so they are 1 dimensional vectors

img_array1 = img_array1.flatten()
img_array2 = img_array2.flatten()

# divide the arrays by 255, the maximum RGB value to make sure every value is on a 0-1 scale

img_array1 = img_array1/255
img_array2 = img_array2/255

# for rgb in img_array1:
#     print(rgb)

from scipy import spatial

res = calculate_cosine(img_array1, img_array2)
print("Cosine new",  res)
similarity = -1 * (spatial.distance.cosine(img_array1, img_array2) - 1)

print(similarity)