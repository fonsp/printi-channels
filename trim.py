from PIL import Image, ImageOps

def trim_file(path):
    im = Image.open(path).convert("L")
    # We invert the image, and ask PIL for the bounding box around all non-black pixel in the image.
    bbox = ImageOps.invert(im).getbbox()

    if bbox is None:
        return "all white"

    im_cropped = im.crop((0, 0, im.width, bbox[3]))
    im_cropped.save(path)
