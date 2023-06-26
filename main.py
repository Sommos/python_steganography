# using cv2 and numpy over PIL because it allows for direct pixel manipulation and thus is more efficient
import cv2
import numpy as np

def encode_image(image_path, message):
    # load the image
    image = cv2.imread(image_path)

    # convert the message into binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    # check if the image is big enough to hold the message
    if len(binary_message) > image.shape[0] * image.shape[1]:
        raise ValueError('Message is too long to be encoded in the image.')

    # encode the message into the image
    encoded_image = np.copy(image)
    binary_index = 0

    # loop through the image and replace the least significant bit of each pixel
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            pixel = list(image[i, j])
            # replace the least significant bit of each pixel with the message
            if binary_index < len(binary_message):
                pixel[0] = (pixel[0] & 0xFE) | int(binary_message[binary_index])
                binary_index += 1

            encoded_image[i, j] = pixel

    # save the encoded image
    cv2.imwrite('encoded_image.png', encoded_image)

def decode_image(encoded_image_path):
    # load the encoded image
    encoded_image = cv2.imread(encoded_image_path)

    binary_message = ''
    # loop through the image and extract the least significant bit of each pixel
    for i in range(encoded_image.shape[0]):
        for j in range(encoded_image.shape[1]):
            pixel = encoded_image[i, j]
            binary_message += str(pixel[0] & 1)

    message = ''
    # loop through the binary message and convert it back into characters
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        char = chr(int(byte, 2))
        message += char

    return message

# test the functions with a test image and message
image_path = 'test_image.png'
message_to_hide = "This is a test message!"

encode_image(image_path, message_to_hide)
decoded_message = decode_image('encoded_image.png')

print("Original Message:", message_to_hide)
print("Decoded Message:", decoded_message)