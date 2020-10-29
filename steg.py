
# Importing Required Modules
import cv2
import numpy as np






# Function to Convert Secret Data into Binary Format
def msgToBinary(message):
    if type(message) == str:
        return ''.join([format(ord(i), "08b") for i in message])
    elif type(message) == bytes or type(message) == np.ndarray:
        return [format(i, "08b") for i in message]
    elif type(message) == int or type(message) == np.uint8:
        return format(message, "08b")
    else:
        print("Input type not supported")
        input("Press Enter to try Again...")
        encode()






# Function to hide the secret message into the image
def hideData(image, secretMsg):

    # Calculate the Maximum Bytes to Encode
    nBytes = image.shape[0] * image.shape[1] * 3 // 8
    print("Maximum bytes to encode:", nBytes)
    print(image)

    # Checking if the Number of Bytes to Encode is Less than the Maximum Bytes in the Image
    if len(secretMsg) > nBytes:
        raise ValueError("Error Encountered Insufficient Bytes, Need Bigger Image or Less Data !!")

    # Delimeter
    secretMsg += "#####"
    dataIndex = 0
    binarySecretMsg = msgToBinary(secretMsg)
    print(binarySecretMsg)

    # Length of Data that needs to be Hidden
    dataLen = len(binarySecretMsg)

    for values in image:
        for pixel in values:
            # Convert RGB Values to Binary Format
            r, g, b = msgToBinary(pixel)
            # Modifying the Least Significant Bit (LSB)
            if dataIndex < dataLen:
                # Red Pixel
                pixel[0] = int(r[:-1] + binarySecretMsg[dataIndex], 2)
                dataIndex += 1
            if dataIndex < dataLen:
                # Green Pixel
                pixel[1] = int(g[:-1] + binarySecretMsg[dataIndex], 2)
                dataIndex += 1
            if dataIndex < dataLen:
                # Blue Pixel
                pixel[2] = int(b[:-1] + binarySecretMsg[dataIndex], 2)
                dataIndex += 1
            if dataIndex >= dataLen:
                break


    # print(image[10,0,1])
    # print(image)
    return image






# Function for Decoding Secret Data from Image
def showData(image):
    binaryData = ""
    for values in image:
        for pixel in values:

            # Converting the Red, Green and Blue Values into Binary Format
            r, g, b = msgToBinary(pixel)

            # Now Extracting Data from the Least Significant Bit (LSB) of
            # Red Pixel
            binaryData += r[-1]
            # Green Pixel
            binaryData += g[-1]
            # Blue Pixel
            binaryData += b[-1]

    # Split by 8-Bits
    allBytes = [ binaryData[ i : i+8 ] for i in range(0, len(binaryData), 8) ]

    # Converting from Bits to Characters
    decodedData = ""

    for byte in allBytes:
        decodedData += chr(int(byte, 2))
        # Checking if We have Reached the Delimeter
        if decodedData[-5:] == "#####":
            break

    # print(decodedData)

    # Removing the Delimeter from Secret Data
    return decodedData[:-5]






# Function for Encoding Text into Image
def encode():
    imageName = input("Enter image name(with extension): ")

    # Reading the Input Image using OpenCV-Python.
    img = cv2.imread(imageName)

    # Image Details
    # Calculate the Number of Bytes from the Output
    print("The Shape of the Input Image is: ", img.shape)
    print("The Original Image is now Opened in a New Window")
    resizedImage = cv2.resize(img, (500, 500))
    # Opens up an Image Window
    cv2.imshow("Resized Image", resizedImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Taking Input for Secret Data
    secretData = input("Enter the Secret Data to be Encoded : ")
    if (len(secretData) == 0):
        print('Secret Data is empty')
        print('Please Try Again')
        input("Press Enter to continue...")
        encode()

    else:
        filename = input("Enter the Name of New Encoded Image(With Extension): ")
        # Function Called for Encoding Secret Data into Image
        encodedImage = hideData(img,secretData)
        cv2.imwrite(filename, encodedImage)






# Function for Decoding Secret Data from Image
def decode():

    # Reading the Image that has the Secret Text
    image_name = input("Enter the Name of the Steganographed Image that you want to Decode (With Extension) :")
    # Reading Image from User
    image = cv2.imread(image_name)

    print("The Steganographed image is as shown below: ")
    # resizedImage = cv2.resize(image, (500, 500))
    # Displays Steganographed Image
    cv2.imshow("Resized Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Function called for Decoding the Secret Data from Steganographed Image
    text = showData(image)
    return text






# Steganography Main Function
def Steganography():
    # Taking Input from User
    userInput = int(input("Image Steganography \n 1. Encode the data \n 2. Decode the data \n Your input is: "))

    if (userInput == 1):
        print("\nEncoding....")
        # Function Called for Encoding Text into Image
        encode()

    elif (userInput == 2):
        print("\nDecoding....")
        # Function Called for Decoding Text from Image
        print("Decoded message is " + decode())
    else:
        raise Exception("Enter correct input")






# Driver Code
if __name__ == "__main__":
    Steganography()