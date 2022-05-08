from google_images_download import google_images_download
import json

from PIL import Image, ImageFont, ImageDraw
import os


def draw_caption(save_name, text):
    files = os.listdir(os.path.join(os.getcwd(), "downloads", "images"))
    font = ImageFont.truetype("font.ttf", 10)

    base = Image.new("RGB", (100, 20), (0, 0, 0))
    draw = ImageDraw.Draw(base)

    size = draw.textsize(text=text, font=font)
    base = base.resize((int(size[0] + size[0] / 6), int(size[1] + size[1] / 6)))

    draw = ImageDraw.Draw(base)
    draw.text((base.width / 2, base.height / 2), text, fill=(255, 255, 255), anchor="ms", font=font)

    idx = 0
    for i in files:
        im = Image.open(os.path.join(os.path.join(os.getcwd(), "downloads", "images"), i), "r")
        base_width = int(im.width / 3)

        wpercent = (base_width / float(base.size[0]))
        hsize = int((float(base.size[1]) * float(wpercent)))
        pasted_base = base.resize((base_width, hsize))
        im.paste(pasted_base,
                 (int((im.width / 2) - (pasted_base.width / 2)), int(im.height / 10 - pasted_base.height / 2)))

        im.save(os.path.join("downloads", "captioned_images", str(idx) + save_name))

        idx += 1


def main():
    configs = json.loads(open("config.json", "r").read())
    records = configs["records"]

    downloader = google_images_download.googleimagesdownload()

    for i in records:
        limit = i.get("limit")
        if not limit:
            limit = 2
        downloader.download({
            "keywords": i["keyword"],
            "limit": limit,
            "size": ">640*480",
            "image_directory": "images",
            "format": "jpg"
        })
        draw_caption(i["keyword"]+".jpg", i["caption"])

main()
