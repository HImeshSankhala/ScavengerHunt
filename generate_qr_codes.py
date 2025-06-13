import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

def create_qr_code(data, filename, title):
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Create a larger image with title
    img_width = 400
    img_height = 500
    final_img = Image.new('RGB', (img_width, img_height), 'white')
    
    # Resize QR code to fit
    qr_size = 300
    qr_img = qr_img.resize((qr_size, qr_size))
    
    # Paste QR code in center
    qr_x = (img_width - qr_size) // 2
    qr_y = 50
    final_img.paste(qr_img, (qr_x, qr_y))
    
    # Add title and data text
    draw = ImageDraw.Draw(final_img)
    
    try:
        # Try to use a nice font
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        data_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        data_font = ImageFont.load_default()
    
    # Draw title
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (img_width - title_width) // 2
    draw.text((title_x, 15), title, fill="black", font=title_font)
    
    # Draw QR data
    data_bbox = draw.textbbox((0, 0), data, font=data_font)
    data_width = data_bbox[2] - data_bbox[0]
    data_x = (img_width - data_width) // 2
    draw.text((data_x, 370), data, fill="black", font=data_font)
    
    # Add instructions
    instruction = "Scan this QR code with the app"
    inst_bbox = draw.textbbox((0, 0), instruction, font=data_font)
    inst_width = inst_bbox[2] - inst_bbox[0]
    inst_x = (img_width - inst_width) // 2
    draw.text((inst_x, 400), instruction, fill="gray", font=data_font)
    
    # Save the image
    final_img.save(filename)
    print(f"Created QR code: {filename}")

# Create QR codes for first two challenges
if __name__ == "__main__":
    # Challenge 1: Black Cat Alley
    create_qr_code(
        "BLACKCAT_ALLEY_001",
        "test-qr-codes/challenge-1-black-cat-alley.png",
        "Challenge 1: Black Cat Alley"
    )
    
    # Challenge 2: Art Museum
    create_qr_code(
        "ART_MUSEUM_002", 
        "test-qr-codes/challenge-2-art-museum.png",
        "Challenge 2: Milwaukee Art Museum"
    )
    
    # Challenge 3: Discovery World
    create_qr_code(
        "DISCOVERY_WORLD_003",
        "test-qr-codes/challenge-3-discovery-world.png", 
        "Challenge 3: Discovery World"
    )
    
    print("All QR codes created successfully!")

