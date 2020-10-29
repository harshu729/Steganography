import cv2
import numpy as np





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





def hideData(image, secretMsg):

    nBytes = image.shape[0] * image.shape[1] * 3 // 8
    print("Maximum bytes to encode:", nBytes)
    print(image)

    if len(secretMsg) > nBytes:
        print("Error Encountered Insufficient Bytes, Need Bigger Image or Less Data !!")
        print('Please Try Again')
        input("Press Enter to continue...")
        encode()

    secretMsg += "#####"
    dataIndex = 0
    binarySecretMsg = msgToBinary(secretMsg)
    print(binarySecretMsg)
    dataLen = len(binarySecretMsg)

    for values in image:
        for pixel in values:
            r, g, b = msgToBinary(pixel)
            if dataIndex < dataLen:
                pixel[0] = int(r[:-1] + binarySecretMsg[dataIndex], 2)
                dataIndex += 1
            if dataIndex < dataLen:
                pixel[1] = int(g[:-1] + binarySecretMsg[dataIndex], 2)
                dataIndex += 1
            if dataIndex < dataLen:
                pixel[2] = int(b[:-1] + binarySecretMsg[dataIndex], 2)
                dataIndex += 1
            if dataIndex >= dataLen:
                break


    # print(image[10,0,1])
    # print(image)
    return image






def showData(image):
    binaryData = ""

    for values in image:
        for pixel in values:
            r, g, b = msgToBinary(pixel)
            binaryData += r[-1]
            binaryData += g[-1]
            binaryData += b[-1]

    allBytes = [ binaryData[ i : i+8 ] for i in range(0, len(binaryData), 8) ]

    decodedData = ""

    for byte in allBytes:
        decodedData += chr(int(byte, 2))
        if decodedData[-5:] == "#####":
            break

    return decodedData[:-5]






def encode():
    imageName = input("Enter image name(with extension): ")
    img = cv2.imread(imageName)

    print("The Shape of the Input Image is: ", img.shape)
    print("The Original Image is now Opened in a New Window")
    resizedImage = cv2.resize(img, (500, 500))
    cv2.imshow("Resized Image", resizedImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    secretData = input("Enter the Secret Data to be Encoded : ")
    if (len(secretData) == 0):
        print('Secret Data is empty')
        print('Please Try Again')
        input("Press Enter to continue...")
        encode()

    else:
        filename = input("Enter the Name of New Encoded Image(With Extension): ")
        encodedImage = hideData(img,secretData)
        cv2.imwrite(filename, encodedImage)



def decode():
    image_name = input("Enter the Name of the Steganographed Image that you want to Decode (With Extension) :")
    image = cv2.imread(image_name)

    print("The Steganographed image is as shown below: ")
    resizedImage = cv2.resize(image, (500, 500))
    cv2.imshow("Resized Image", resizedImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    text = showData(image)
    return text







def Steganography():
    userInput = int(input("Image Steganography \n 1. Encode the data \n 2. Decode the data \n Your input is: "))
    if (userInput == 1):
        print("\nEncoding....")
        encode()

    elif (userInput == 2):
        print("\nDecoding....")
        print("Decoded message is " + decode())
    else:
        print("Enter correct input")
        print('Please Try Again')
        input("Press Enter to continue...")
        Steganography()





if __name__ == "__main__":
    Steganography()