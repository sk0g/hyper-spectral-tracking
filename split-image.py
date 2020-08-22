from hs_utils import X2Cube
from PIL import Image
from matplotlib import pyplot
import numpy as np


def display_example_image_channels():
    image_dir = '../extracted/test/rubik/HSI/0005.png'

    img = Image.open(image_dir)

    img_array = np.asarray(img)

    channel_data = X2Cube(img_array)
    num_channels = channel_data.shape[2]

    fig = pyplot.figure(
        figsize=(36, 18))
    for channel in range(num_channels):
        fig.add_subplot(4, 4, channel+1)
        pyplot.imshow(
            channel_data[:,:,[channel]],
            cmap='inferno')

    fig.show()


if __name__ == '__main__':
    display_example_image_channels()
