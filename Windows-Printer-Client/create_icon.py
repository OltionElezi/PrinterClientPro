"""
Create printer icon for the application
"""
from PIL import Image, ImageDraw

# Create icon sizes
sizes = [256, 128, 64, 48, 32, 16]
images = []

for size in sizes:
    # Create image
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Scale factors
    s = size / 64.0

    # Draw printer icon
    # Top part (paper tray)
    top_y = int(15 * s)
    top_height = int(10 * s)
    top_x = int(20 * s)
    top_width = int(24 * s)
    draw.rectangle([top_x, top_y, top_x + top_width, top_y + top_height],
                   fill=(99, 102, 241, 255))  # Indigo

    # Middle part (main body)
    mid_y = top_y + top_height
    mid_height = int(20 * s)
    mid_x = int(15 * s)
    mid_width = int(34 * s)
    draw.rectangle([mid_x, mid_y, mid_x + mid_width, mid_y + mid_height],
                   fill=(241, 245, 249, 255))  # Light gray

    # Paper slot
    slot_y = mid_y + int(5 * s)
    slot_height = int(10 * s)
    slot_x = int(22 * s)
    slot_width = int(20 * s)
    draw.rectangle([slot_x, slot_y, slot_x + slot_width, slot_y + slot_height],
                   fill=(15, 23, 42, 255))  # Dark

    # Bottom part (output tray)
    bot_y = mid_y + mid_height
    bot_height = int(5 * s)
    draw.rectangle([top_x, bot_y, top_x + top_width, bot_y + bot_height],
                   fill=(16, 185, 129, 255))  # Green

    # Add indicator light (small green dot)
    light_size = max(2, int(3 * s))
    light_x = int(52 * s)
    light_y = mid_y + int(7 * s)
    draw.ellipse([light_x, light_y, light_x + light_size, light_y + light_size],
                 fill=(16, 185, 129, 255))

    images.append(img)

# Save as ICO
images[0].save('printer_icon.ico', format='ICO', sizes=[(s, s) for s in sizes], append_images=images[1:])
print("Icon created: printer_icon.ico")
