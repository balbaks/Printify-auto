import requests
import base64
from PIL import Image, ImageDraw, ImageFont
import io

PRINTIFY_TOKEN ="eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzN2Q0YmQzMDM1ZmUxMWU5YTgwM2FiN2VlYjNjY2M5NyIsImp0aSI6ImQzNjc5ZWIxYTVhZTBlZTk1ZDhhYmIwY2NhNWEwYWVjZTg1ZWZhODkwYWZmZDk2NTEzYjc5ZGRlYjYxM2U0MzNiMzY5NjYyY2NmZDc1Y2MwIiwiaWF0IjoxNzgyMzExMDI2LjgzMDU5MiwibmJmIjoxNzgyMzExMDI2LjgzMDU5NCwiZXhwIjoxODEzODQ3MDI2LjgyNTA2Miwic3ViIjoiMjcwMTUwMjciLCJzY29wZXMiOlsic2hvcHMubWFuYWdlIiwic2hvcHMucmVhZCIsImNhdGFsb2cucmVhZCIsIm9yZGVycy5yZWFkIiwib3JkZXJzLndyaXRlIiwicHJvZHVjdHMucmVhZCIsInByb2R1Y3RzLndyaXRlIiwid2ViaG9va3MucmVhZCIsIndlYmhvb2tzLndyaXRlIiwidXBsb2Fkcy5yZWFkIiwidXBsb2Fkcy53cml0ZSIsInByaW50X3Byb3ZpZGVycy5yZWFkIiwidXNlci5pbmZvIl19.Ggt8seJafRGOv4cBW8jkNlTgHDl1rei3C8PttwFHCOKDTYXW5lT93H9xMrIdFrmz7IV0FFnpz6cvsoPaGKbHrXgRRy5t47NJYGQj_tv_g7MkBJY92ValsV7Q8tfNqEJwKX49FsCRTjqYxjS6uXYlEBM9Nr-JdYj4-Kp5uE_maqGCp3TrBTqeZ5sUJZhRKjnIM7UOn5rWVXvDTF9yg53lvoBWqHCGTIJeSjbunk0EKcZ69lrKthDG9g7nH8JTKHTZgq1EHQM81QDE21A0MnA_iMNz7IDYRpWdzV5_ykBvR9CUDbGv8ysbo-7l3uqJJszNkLGodeSXu62NBcRTkotGtXKiaxho-yyNmV1kMKY4THUS46l7Vo4ZuTzm8yU3qLUaie2DUH08jWBE74aXS0-PT3M52UY2sfqD8Mk0n0XgXBRMwnE9312sK9XzNgM_pZyIeq38yX0WqdgSq3p9UCSA1tv4uYhuEptVttC7ESo4smnA1TxNFsaPSEG_j1HI5V17uCHemsr-qQJZFzRP-LilNp_GhM8T4z1y9acYhLFhk4IPQQkECRAt1K6MqKWDtkbYdLcAnBRBuJAcL6D41mO5MNnqQFlQRuftYXvHxFOWqa_bv8YZTNsQU61QY3jNVBsfUxOOhW61WlmUOyQZTftPrJRfJOvjgPEa2CucUT00NsA"
SHOP_ID = 27230064
HEADERS = {
    "Authorization": f"Bearer {PRINTIFY_TOKEN}",
    "Content-Type": "application/json"
}

# STEP 1: Get correct variant IDs
def get_variants():
    r = requests.get(
        "https://api.printify.com/v1/catalog/blueprints/5/print_providers/99/variants.json",
        headers=HEADERS
    )
    result = r.json()
    print("✅ Variants:", result)
    return result

# STEP 2: Generate Design
def generate_design():
    img = Image.new('RGB', (4500, 5400), color='black')
    draw = ImageDraw.Draw(img)
    
    # Big bold text
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 600)
    
    lines = ["SILENCE", "IS", "POWER"]
    y = 1800
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        x = (4500 - w) / 2
        draw.text((x, y), line, fill='white', font=font)
        y += 700
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode()

# STEP 3: Upload Design
def upload_design(img_base64):
    payload = {
        "file_name": "silence_is_power.png",
        "contents": img_base64
    }
    r = requests.post(
        "https://api.printify.com/v1/uploads/images.json",
        headers=HEADERS,
        json=payload
    )
    result = r.json()
    print("✅ Upload result:", result)
    return result["id"]

# STEP 4: Create Product
def create_product(image_id, variants):
    # Get first 4 variant IDs only
    variant_ids = [v["id"] for v in variants["variants"][:4]]
    print("Using variant IDs:", variant_ids)
    
    payload = {
        "title": "SILENCE IS POWER Tee",
        "description": "Minimal streetwear. Speak less. Do more.",
        "blueprint_id": 5,
        "print_provider_id": 99,
        "variants": [
            {"id": vid, "price": 2999, "is_enabled": True}
            for vid in variant_ids
        ],
        "print_areas": [{
            "variant_ids": variant_ids,
            "placeholders": [{
                "position": "front",
                "images": [{
                    "id": image_id,
                    "x": 0.5,
                    "y": 0.5,
                    "scale": 0.8,
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
    print("✅ Product created:", result)
    return result["id"]

# RUN
print("🔍 Getting variants...")
variants = get_variants()
print("🎨 Generating design...")
design = generate_design()
print("📤 Uploading to Printify...")
image_id = upload_design(design)
print("👕 Creating product...")
product_id = create_product(image_id, variants)
print(f"✅ DONE! Product ID: {product_id}")
print("👀 Go check Printify dashboard to preview!")
