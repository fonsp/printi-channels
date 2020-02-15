from PIL import Image, ImageOps, ImageFont, ImageDraw


def trim_image(im):
    # We invert the image, and ask PIL for the bounding box around all non-black pixel in the image.
    bbox = ImageOps.invert(im).getbbox()

    if bbox is None:
        return "all white"

    im_cropped = im.crop((0, 0, im.width, bbox[3]))
    return im_cropped


def trim_file(path):
    im = Image.open(path).convert("L")
    trim_image(im).save(path)


def trim_and_name_file(path, channel_name, width):
    im = Image.open(path).convert("L")
    im_cropped = trim_image(im)

    c_title = "/" + channel_name
    w = width // 10 # 10 is the character width for our font at size 16
    chopped = [c_title[start:start + w] for start in range(0, len(c_title), w)]

    new_im = Image.new("L", (width, 10 + 16 + 10 + 16 * len(chopped) + 20 + im_cropped.height), color="white")
    draw = ImageDraw.Draw(new_im)

    font = ImageFont.truetype("RobotoMono-MediumItalic.ttf", 16)
    verycoolurl = "channels.printi.me"
    draw.text(((width - 9*len(verycoolurl)) // 2, 10), verycoolurl, fill="black", font=font)


    font = ImageFont.truetype("RobotoMono-Medium.ttf", 16)
    for h, line in enumerate(chopped):
        draw.text(((width - 10*len(line)) // 2, 10 + 16 + 10 + 16*h), line, fill="black", font=font)

    new_im.paste(im_cropped, (0, 10 + 16 + 10 + 16 * len(chopped) + 20))
    new_im.save("as"+path)
