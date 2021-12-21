#RESIZE & ADD LOGO
import os
from PIL import Image
SQUARE_FIT_SIZE = 300
LOGO_FILENAME = "logo.jpg"
logoIm = Image.open(LOGO_FILENAME)
logoIm = logoIm.convert("RGBA")
logoIm = logoIm.resize((50,50))
logoWidth, logoHeight = logoIm.size
os.makedirs("withLogo", exist_ok = True)
os.makedirs("alphacomposite", exist_ok=True)
for filename in os.listdir("."):
    if not (filename.endswith(".png") or filename.endswith(".jpg")) \
        or filename == LOGO_FILENAME:
        continue
    im = Image.open(filename).convert("RGBA")
    width,height = im.size
    #Check if image needs to be resized.
    if width > SQUARE_FIT_SIZE and height > SQUARE_FIT_SIZE:
        #Calculate the new width and height to resize to.
        if width > height:
            height = int((SQUARE_FIT_SIZE / width)*height)
            width = SQUARE_FIT_SIZE
        else:
            width = int((SQUARE_FIT_SIZE / height) * width)
            height = SQUARE_FIT_SIZE
        # Resize the image.
        print("Resizing %s..." % (filename))
        im = im.resize((width,height))
        #Convert and transparent the logo.
        datas = logoIm.getdata()

        newData = []

        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        logoImTrans = logoIm.putdata(newData)
        #Add the logo.
        print("Adding logo to %s..." % (filename))
        im.paste(logoIm, (width - logoWidth, height - logoHeight), logoIm)
        #Save the changes.
        if im.mode in ("RGBA","p"):
            im = im.convert("RGB")
        im.save(os.path.join("withLogo", filename))