from PIL import Image
import numpy as np

char_offsets_Dictionary = {
    'A': ('R', -4), 'B': ('R', -3), 'C': ('R', -2),
    'D': ('R', -1), 'E': ('R', 1), 'F': ('R', 2),
    'G': ('R', 3), 'H': ('R', 4), 'I': ('R', 5),
    'J': ('G', -4), 'K': ('G', -3), 'L': ('G', -2),
    'M': ('G', -1), 'N': ('G', 1), 'O': ('G', 2),
    'P': ('G', 3), 'Q': ('G', 4), 'R': ('G', 5),
    'S': ('B', -4), 'T': ('B', -3), 'U': ('B', -2),
    'V': ('B', -1), 'W': ('B', 1), 'X': ('B', 2),
    'Y': ('B', 3), 'Z': ('B', 4), ' ': ('B', 5),
}

def decrypt(filename):
    # Open image and convert
    img = Image.open(filename)
    img = img.convert('RGBA')
    pixels = np.array(img)
    width, height = img.size
    total_pixels = width * height

    offset = 30
    pixel_num = 0

    decoded_message = ""

    index = 0

    # Read message length from pixel (0, 0)
    messageLength = pixels[0, 0][3]
    print(messageLength)

    # Loop through each letter in the message
    while index < messageLength:

        # Advance to the next pixel
        pixel_num += offset

        # get pixel location from offset
        # ie with an image width of 1000 and a pixel of 3000
        # this pixel will be the first pixel in the 3rd row
        x = pixel_num % width
        y = pixel_num // width

        r, g, b, _ = pixels[y, x]

        # same as above but for the previous pixel ie 2999
        prev_pixel_num = pixel_num - 1
        prev_x = prev_pixel_num % width
        prev_y = prev_pixel_num // width

        pr, pg, pb, _ = pixels[prev_y, prev_x].astype(int)

        if pr < 5 or pr > 250 or pg < 5 or pg > 250 or pb < 5 or pb > 250 or r < 5 or r > 250 or g < 5 or g > 250 or b < 5 or b > 250:
            continue

        if r != pr:
            channel = 'R'
            diff = r - pr
        elif g != pg:
            channel = 'G'
            diff = g - pg
        elif b != pb:
            channel = 'B'
            diff = b - pb
        else:
            continue  # No difference detected, skip

        found_letter = ''
        for letter in char_offsets_Dictionary:
            pixelChannel, pixelMod = char_offsets_Dictionary[letter]
            if pixelChannel == channel and pixelMod == diff:
                found_letter = letter
                break
        if found_letter == '':
            break
        decoded_message += found_letter
        index += 1

    print("Decoded message:", decoded_message)


filename = input("Enter image filename: ")

decrypt(filename)