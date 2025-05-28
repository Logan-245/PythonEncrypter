from PIL import Image

# test values abcdefghijklmnopqrstuvwxyz
# Alpha channel values and what they mean:
RFLAG = 254
GFLAG = 253
BFLAG = 252
SKIPFLAG = 251
LASTFLAG = 250

# Mapping of encode values and their respective chars
DITCTUPLES = {
    'A': ('R', -4), 'B': ('R', -3), 'C': ('R', -2),
    'D': ('R', -1), 'E': ('R', 0),  'F': ('R', 1),
    'G': ('R', 2),  'H': ('R', 3),  'I': ('R', 4),
    'J': ('G', -4), 'K': ('G', -3), 'L': ('G', -2),
    'M': ('G', -1), 'N': ('G', 0),  'O': ('G', 1),
    'P': ('G', 2),  'Q': ('G', 3),  'R': ('G', 4),
    'S': ('B', -4), 'T': ('B', -3), 'U': ('B', -2),
    'V': ('B', -1), 'W': ('B', 0),  'X': ('B', 1),
    'Y': ('B', 2),  'Z': ('B', 3),  ' ': ('B', 4)
}

# Takes in the array of pixels, x and y co-ordinates, width and the char to be stored
#   Will calculate the delta with the previous pixel, change the current pixels color channel by delta
#   then change the alpha channel with the respective flag
#   skips any pixel with an extreme value that could bring value outside the [0,255] range
def encodePix(pixels, x, y, width, char):
    # get the previous index and calculate prev x and y coordinates
    prevI = x + y * width - 1
    prevX = prevI % width
    prevY = prevI // width

    prevPix = pixels[prevX, prevY]
    # unpack RGB
    r, g, b, _ = prevPix

    # skip a pixel if less than 5 or over 250
    if r < 5 or r > 250 or g < 5 or g > 250 or b < 5 or b > 250:
        pixels[x, y] = (r, g, b, SKIPFLAG)
        return False
    # ensure that the char exists in char map, default to a space char otherwise
    ch = char if char in DITCTUPLES else ' '
    # extract the color channel and the delta from the char map
    channel, change = DITCTUPLES[ch]
    # get the rgb values of the pixel, change the appropriate color channel, clamp to [0,255] if needed
    newPix  = [r, g, b]
    channelIndex = {'R':0, 'G':1, 'B':2}[channel]
    newVal = newPix[channelIndex] + change
    newVal = min(255, max(0, newVal))
    newPix[channelIndex] = newVal
    # append the flag as alpha
    pixels[x, y] = tuple(newPix) + ({'R': RFLAG, 'G': GFLAG, 'B': BFLAG}[channel],)
    return True


def Encrypt(inputPath, message, offset=30, outputPath="encrypted.png"):
    # open the image and prep it by ensuring RGB and finding the size
    img = Image.open(inputPath)
    img = img.convert('RGBA')
    pixels = img.load()
    width, height = img.size
    totalPix = width * height

    # ensure all chars are uppercase
    message = message.upper()
    msgLen = len(message)

    # check if the message is too long to be placed in the image
    if msgLen * offset >= totalPix:
        print("Message too long for this image")
        return

    #split the message into an array of chars
    msgChars = list(message)

    #track the index of the offset and how many chars are encoded
    offsetIndex = 1
    encoded = 0
    # loop through the array, only advancing when a pixel is successfully written
    while encoded < msgLen:
        i = offsetIndex * offset
        x, y = i % width, i // width

        offsetIndex += 1
        if encodePix(pixels, x, y, width, msgChars[encoded]):
            encoded += 1



            # check if it's the last char
            if encoded == msgLen:
                # grab its current RGB
                r, g, b, _ = pixels[x, y]
            # overwrite alpha with lastFlag and exit the loop
                pixels[x, y] = (r, g, b, LASTFLAG)
                break

    img.save(outputPath)
    print(f"Message encrypted, output written to {outputPath}")


message = input("Enter the message to encrypt : ").upper()
fileName = input("Enter the image filename: ")
Encrypt(fileName, message)