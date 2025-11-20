from PIL import Image, ImageDraw, ImageFont, ImageFilter
import requests
from io import BytesIO


def create_status_image(username, status, game_name, additional_info, avatar_url="", game_icon_url="", is_banned=""):
    status_color = (0, 255, 140) if status == "Online" else (255, 80, 80)

    # Buat gambar dengan mode RGBA agar transparansi tetap ada
    img = Image.new('RGBA', (520, 300), (0, 0, 0, 0))  # transparan total dulu
    draw = ImageDraw.Draw(img)

    # Background gelap (bisa diganti gradient atau gambar blur)
    # semi-transparan dark
    # If game_icon_url is provided, use it as blurred background
    if game_icon_url:
        try:
            response = requests.get(game_icon_url)
            bg_img = Image.open(BytesIO(response.content)).convert("RGBA")
            bg_img = bg_img.resize((520, 300), Image.LANCZOS)
            bg_img = bg_img.filter(ImageFilter.GaussianBlur(5))
            # Overlay a semi-transparent dark layer for readability
            overlay = Image.new('RGBA', (520, 300), (20, 20, 30, 180))
            bg_img = Image.alpha_composite(bg_img, overlay)
            img.paste(bg_img, (0, 0))
        except Exception as e:
            # fallback to plain dark background if error
            background = Image.new('RGBA', (600, 300), (20, 20, 30, 240))
            img.paste(background, (0, 0))
    else:
        background = Image.new('RGBA', (600, 300), (20, 20, 30, 240))
        img.paste(background, (0, 0))

    # Load & paste avatar (transparansi tetap aman)
    if avatar_url:
        response = requests.get(avatar_url)
        avatar = Image.open(BytesIO(response.content)).convert("RGBA")
        avatar = avatar.resize((140, 140), Image.LANCZOS)

        # Rounded corner
        mask = Image.new('L', (140, 140), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.rounded_rectangle([0, 0, 139, 139], radius=70, fill=255)
        avatar = avatar.crop((0, 0, 140, 140))
        avatar.putalpha(mask)

        avatar_pos = (30, 70)
        img.paste(avatar, avatar_pos, avatar)
        # add circular border around avatar
        border_size = avatar.size  # (140, 140)
        border_img = Image.new('RGBA', border_size, (0, 0, 0, 0))
        border_draw = ImageDraw.Draw(border_img)
        border_width = 6
        border_draw.rounded_rectangle(
            [0, 0, border_size[0]-1, border_size[1]-1],
            radius=border_size[0]//2,
            outline=status_color,
            width=border_width
        )
        img.paste(border_img, avatar_pos, border_img)

    title_font = ImageFont.truetype("GothamBlack.otf", 36)
    regular_font = ImageFont.truetype("GothamBlack.otf", 24)

    # Teks
    draw.text((190, 70), username, fill=(255, 255, 255), font=title_font)

    draw.text((190, 105), f"[+] {status}",
              fill=status_color, font=regular_font)

    if game_name:
        draw.text((190, 140), f"Sedang bermain", fill=(
            180, 180, 180), font=regular_font)
        draw.text((190, 165), f"[+] {game_name}",
                  fill=status_color, font=regular_font)

    if additional_info:
        draw.text((190, 200), additional_info, fill=(150, 150, 150),
                  font=ImageFont.truetype("GothamBlack.otf", 18))
    if is_banned:
        draw.text((190, 220), is_banned, fill=(150, 150, 150),
                  font=ImageFont.truetype("GothamBlack.otf", 18))

    # Simpan sebagai PNG agar transparansi tetap ada
    img.save(f"status.png", "PNG")
    return img  # kalau mau langsung upload ke Discord


if __name__ == "__main__":
    create_status_image(
        username="RobloxUser",
        status="Offline",
        game_name=None,
        additional_info="@asep | 0000000",
        avatar_url="",
        game_icon_url=""
    )
