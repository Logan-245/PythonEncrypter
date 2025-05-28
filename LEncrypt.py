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



def encrypt(filename, message):

    # Open image and convert
    img = Image.open(filename)
    img = img.convert('RGBA')
    pixels = np.array(img)
    height, width = img.size
    total_pixels = width * height

    offset = 30
    pixel_num = 0

    # normalize the message, and get its length
    message = message.upper()
    messageLength = len(message)

    if messageLength >= 255:
        print("Message too long (max 254 characters)")
        return

    if messageLength * offset >= total_pixels:
        print("Message too long")
        exit()

    # Loop through each letter in the message
    index = 0  # index into the message

    #store message length in first pixel add to all so the pixel look reativly unchanged/corupted
    pixels[0,0][3] = messageLength
    print(messageLength)
    while index < messageLength:
        letter = message[index]
        pixelChannel, pixelMod = char_offsets_Dictionary[letter]

        pixel_num += offset


        x = pixel_num % width
        y = pixel_num // width

        prev_pixel_num = pixel_num - 1
        prev_x = prev_pixel_num % width
        prev_y = prev_pixel_num // width

        r, g, b, _ = pixels[prev_y, prev_x]

        if r < 5 or r > 250 or g < 5 or g > 250 or b < 5 or b > 250:
            continue  # skip bad pixel, don't increment index

        new_pixel = pixels[prev_y, prev_x].astype(int)

        if pixelChannel == 'R':
            new_pixel[0] += pixelMod
        elif pixelChannel == 'G':
            new_pixel[1] += pixelMod
        elif pixelChannel == 'B':
            new_pixel[2] += pixelMod



        pixels[y, x] = new_pixel.astype(np.uint8)

        index += 1  # Only move to the next letter if this one was successfully encoded

    # save the new image
    new_img = Image.fromarray(pixels)
    #JPG doesnt work correctly so save all files as png
    new_filename = "Encrypted_" + filename.partition('.')[0] + ".png"
    new_img.save(new_filename, format="PNG")
    print("Message encrypted into image and saved as", new_filename)


# Ask user for inputs
filename = input("Enter image filename: ")
message = input("Enter message to hide: ")
encrypt(filename, message)
