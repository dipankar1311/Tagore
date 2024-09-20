pattern_string= None
media_file = ""

def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    import re
    import os
    import glob
    client = vision.ImageAnnotatorClient()

    global media_file
    touch_file=""

    while True:
      ff = glob.glob(path)
      for f in ff:
        if f.endswith(".mp3"):
          media_file = f
        elif "filefortouch.txt" in f:
          touch_file = f

      if media_file and touch_file:
        break

    print("media file name = " + media_file)
    print("touch file name = " + touch_file)

    with open(touch_file) as file_in:
        for line in file_in:
            line = line.strip('\n')
            image_file = "%s" % line
            print("Processing image file: " + image_file)

    with io.open(image_file, 'rb') as image_file_line:
        content = image_file_line.read()


    print("Calling OCR API")
    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    op_file_name = "../../resources/ocroutput/ocr_output.txt"
    #op_file_name = os.path.basename(path)
    #op_file_name = "../../resources/ocroutput/" + op_file_name + ".txt"
    print("Got response from OCR server")

    f = open(op_file_name, "w")
    f.write("Texts:")
    f.close()

    f = open(op_file_name, "a")

    str = ""
#   str = "["

    for text in texts[1:]:
        string = text.description
        new_str1 = re.sub('[^a-zA-Z0-9\n\.]', ' ', string)
        new_str2 = new_str1.strip()
        if new_str2:
          f.write(new_str2 + '\n')
          str = str + new_str2 + ','
          #print(str)

#    str = str + "]"
    print(str)
    global pattern_string
    pattern_string = str
    f.close()

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    print("OCR result parsing completed and stored in file " + op_file_name)

def get_media_file_name():
    global media_file
    print(media_file)
    return media_file
 
def get_pattern_string():
    global pattern_string
    print(pattern_string)
    return pattern_string.split(',')
