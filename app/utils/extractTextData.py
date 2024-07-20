import pytesseract
import cv2
import tempfile
import re
from PIL import Image
from pytesseract import Output

def extractImageTextData(uploaded_image_file, ret):
    print("extractImageTextData")

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        for chunk in uploaded_image_file.chunks():
            temp_file.write(chunk)
        temp_image_file_path = temp_file.name

    #process image
    processed_two_imgs = processImage(temp_image_file_path)  #CONVERTED TO NP ARRAY
    temp_file.close()

    #extract text and draw 
    image_data = extractTextAndDraw(processed_two_imgs, uploaded_image_file)

    return image_data

def extractTextAndDraw(processed_two_imgs, uploaded_image_file):
    processed_np_img = processed_two_imgs[0]
    np_img_color = processed_two_imgs[1]

    data = pytesseract.image_to_data(processed_np_img, output_type=Output.DICT)

    # Create a dictionary to store blocks
    blocks = {}

    # Iterate over each text element
    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 0:  # Only consider text with confidence > 0
            block_num = data['block_num'][i]
            text = data['text'][i]
            text = clean_text(text)
            if text == "":
                continue
            left, top, width, height = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

            # Add the text to the corresponding block
            if block_num not in blocks:
                blocks[block_num] = {'text': text, 'left': left, 'top': top, 'width': width, 'height': height}
            else:
                # Extend the boundaries of the block
                blocks[block_num]['left'] = min(blocks[block_num]['left'], left)
                blocks[block_num]['top'] = min(blocks[block_num]['top'], top)
                blocks[block_num]['width'] = max(blocks[block_num]['width'], left + width - blocks[block_num]['left'])
                blocks[block_num]['height'] = max(blocks[block_num]['height'], top + height - blocks[block_num]['top'])
                blocks[block_num]['text'] += ' ' + text  # Concatenate additional text

    # Create a copy of the image to draw the rectangles, no need to make copy
    np_img_with_blocks = np_img_color

    # Draw a rectangle around each block and print text
    new_block_num = 1
    json_image_data = {}
    text_data = ""
    for block_num, block_data in blocks.items():
        left, top, width, height = block_data['left'], block_data['top'], block_data['width'], block_data['height']
        
        #draw rectangle 
        cv2.rectangle(np_img_with_blocks, (left, top), (left + width, top + height), (255, 0, 0), 4) #BGR

        #draw circle 
        if(new_block_num<10):
            circLeft = left+20
            radius = 40
        else:
            circLeft = left+40
            radius = 50
        cv2.circle(np_img_with_blocks, (circLeft, top - 35), radius, (255, 255, 255), -1)  # -1 fills the circle

        #text 
        cv2.putText(np_img_with_blocks, str(new_block_num), (left, top - 12), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 215), 4)
        # print(f"Block {new_block_num} Text: {block_data['text']}")
        json_image_data[str(new_block_num)]= block_data['text']
        text_data += " "+block_data['text']
        new_block_num+=1

    #save image 
    max_width, max_height = 1920, 1080
    height, width = np_img_with_blocks.shape[:2]

    if width > max_width or height > max_height:
        # Calculate the scaling factor
        scaling_factor = min(max_width / width, max_height / height)
        new_width = int(width * scaling_factor)
        new_height = int(height * scaling_factor)
        
        # Resize the image
        resized_image = cv2.resize(np_img_with_blocks, (new_width, new_height), interpolation=cv2.INTER_AREA)
    else:
        # If the image does not need resizing, keep it as it is
        resized_image = np_img_with_blocks

    # Convert BGR to RGB 
    final_np_img = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

    #cv2.imwrite('output_image.png', img, [cv2.IMWRITE_PNG_COMPRESSION, 0])  #high quality pngs
    #cv2.imwrite('output_image.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 100])
    # cv2.imwrite('output_image_quality_100_resized.jpg', final_np_img, [cv2.IMWRITE_JPEG_QUALITY, 100]) #compressed jpegs
 
    # for key, value in json_image_data.items():
    #     print(f"Key: {key}, Value: {value}")

    ret_data = {
        "new_np_image": final_np_img,   #np array
        "json_image_data": json_image_data,  #json extracted data
        "str_image_text": text_data  #string of all text 
    }
    return ret_data

def clean_text(text):
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    return text.strip()  # Remove leading and trailing spaces


def processImage(image_path):
    # print("reading from:"+image_path)
    np_img = cv2.imread(image_path, flags=cv2.IMREAD_GRAYSCALE)
    np_img_color = cv2.imread(image_path)
    processed_np_img = cv2.adaptiveThreshold(
        np_img, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        61,
        11
    )
    return [processed_np_img, np_img_color]

def extractPdfTextData(file, ret):
    ret["status"] = 401
    ret["mssg"] = "pdf files not supported yet"
    return 
