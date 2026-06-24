import requests
import base64
from PIL import Image, ImageDraw, ImageFont
import io
import os

PRINTIFY_TOKEN ="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzN2Q0YmQzMDM1ZmUxMWU5YTgwM2FiN2VlYjNjY2M5NyIsImp0aSI6ImQzNjc5ZWIxYTVhZTBlZTk1ZDhhYmIwY2NhNWEwYWVjZTg1ZWZhODkwYWZmZDk2NTEzYjc5ZGRlYjYxM2U0MzNiMzY5NjYyY2NmZDc1Y2MwIiwiaWF0IjoxNzgyMzExMDI2LjgzMDU5MiwibmJmIjoxNzgyMzExMDI2LjgzMDU5NCwiZXhwIjoxODEzODQ3MDI2LjgyNTA2Miwic3ViIjoiMjcwMTUwMjciLCJzY29wZXMiOlsic2hvcHMubWFuYWdlIiwic2hvcHMucmVhZCIsImNhdGFsb2cucmVhZCIsIm9yZGVycy5yZWFkIiwib3JkZXJzLndyaXRlIiwicHJvZHVjdHMucmVhZCIsInByb2R1Y3RzLndyaXRlIiwid2ViaG9va3MucmVhZCIsIndlYmhvb2tzLndyaXRlIiwidXBsb2Fkcy5yZWFkIiwidXBsb2Fkcy53cml0ZSIsInByaW50X3Byb3ZpZGVycy5yZWFkIiwidXNlci5pbmZvIl19.Ggt8seJafRGOv4cBW8jkNlTgHDl1rei3C8PttwFHCOKDTYXW5lT93H9xMrIdFrmz7IV0FFnpz6cvsoPaGKbHrXgRRy5t47NJYGQj_tv_g7MkBJY92ValsV7Q8tfNqEJwKX49FsCRTjqYxjS6uXYlEBM9Nr-JdYj4-Kp5uE_maqGCp3TrBTqeZ5sUJZhRKjnIM7UOn5rWVXvDTF9yg53lvoBWqHCGTIJeSjbunk0EKcZ69lrKthDG9g7nH8JTKHTZgq1EHQM81QDE21A0MnA_iMNz7IDYRpWdzV5_ykBvR9CUDbGv8ysbo-7l3uqJJszNkLGodeSXu62NBcRTkotGtXKiaxho-yyNmV1kMKY4THUS46l7Vo4ZuTzm8yU3qLUaie2DUH08jWBE74aXS0-PT3M52UY2sfqD8Mk0n0XgXBRMwnE9312sK9XzNgM_pZyIeq38yX0WqdgSq3p9UCSA1tv4uYhuEptVttC7ESo4smnA1TxNFsaPSEG_j1HI5V17uCHemsr-qQJZFzRP-LilNp_GhM8T4z1y9acYhLFhk4IPQQkECRAt1K6MqKWDtkbYdLcAnBRBuJAcL6D41mO5MNnqQFlQRuftYXvHxFOWqa_bv8YZTNsQU61QY3jNVBsfUxOOhW61WlmUOyQZTftPrJRfJOvjgPEa2CucUT00NsA"
SHOP_ID = 27230064
HEADERS = {
    "Authorization": f"Bearer {PRINTIFY_TOKEN}",
    "Content-Type": "application/json"
}

def download_arabic_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/arefruqaa/ArefRuqaa-Regular.ttf"
    font_path = "/tmp/arabic_font.ttf"
    if not os.path.exists(font_path):
        print("📥 Downloading Arabic font...")
        r = requests.get(font_url)
        with open(font_path, "wb") as f:
            f.write(r.content)
    return font_path

def generate_design(font_path):
    img = Image.new('RGBA', (4500, 5400), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_path, 1200)
    text = "يا حسين"
    bbox = draw.textbbox((0, 0), text, font=font, direction='rtl', language='ar')
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (4500 - w) / 2
    y = (5400 - h) / 2
    # Red glow effect
    for offset in range(8, 0, -1):
        draw.text((x+offset, y+offset), text,
                  fill=(180, 0, 0, 80),
                  font=font, direction='rtl', language='ar')
    # Main red text
    draw.text((x, y), text,
              fill=(220, 20, 20, 255),
              font=font, direction='rtl', language='ar')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode()

def upload_design(img_base64):
    payload = {
        "file_name": "ya_hussien.png",
        "contents": img_base64
    }
    r = requests.post(
        "https://api.printify.com/v1/uploads/images.json",
        headers=HEADERS,
        json=payload
    )
    result = r.json()
    print("✅ Upload:", result.get("id"))
    return result["id"]

def create_product(image_id):
    black_variants = [17426, 17427, 17428, 17429, 17430, 17431, 17432, 17433]
    payload = {
        "title": "يا حسين | Ya Hussein Tee",
        "description": "Voidwear. Wear the silence.\n\nBold Arabic calligraphy on premium black tee.\n\n✦ Red calligraphy print\n✦ Solid black unisex tee\n✦ True to size",
        "blueprint_id": 5,
        "print_provider_id": 99,
        "variants": [
            {"id": vid, "price": 3499, "is_enabled": True}
            for vid in black_variants
        ],
        "print_areas": [{
            "variant_ids": black_variants,
            "placeholders": [{
                "position": "front",
                "images": [{
                    "id": image_id,
                    "x": 0.5,
                    "y": 0.5,
                    "scale": 1.0,
                    "angle": 0
                }]
            }]
        }]
    }
    r = requests.post(
        f"https://api.printify.com/v1/shops/{SHOP_ID}/products.json",
        headers=HEADERS,
        json=payload
    )
    result = r.json()
    print("✅ Product:", result.get("id"))
    return result["id"]

# RUN
print("📥 Getting Arabic font...")
font_path = download_arabic_font()
print("🎨 Generating يا حسين design...")
design = generate_design(font_path)
print("📤 Uploading to Printify...")
image_id = upload_design(design)
print("👕 Creating black tee...")
product_id = create_product(image_id)
print(f"✅ DONE! Product ID: {product_id}")
print("👀 Check Printify dashboard!")
