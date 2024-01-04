import textwrap
from PIL import Image, ImageDraw, ImageFont


def create_ad_template(
        product_img: Image.Image,
        logo_image: Image.Image,
        color_hex: str,
        punchline: str,
        button_text: str
) -> Image.Image:
    """
    Creates a simple ad image with given inputs

    Args:
        - product_img (PIL.Image.Image): Base image to be used on the ad.
        - logo_image (PIL.Image.Image): Logo image to be used on the ad.
        - color_hex (str): Main color (in HEX code) of the ad created.
        - punchline (str): Punchline to be used on the ad.
        - button_text (str): Button text to be used on the ad.

    Returns:
        - ad_image (PIL.Image.Image): New ad image created with given inputs
    """
    color_hex = '#' + color_hex if '#' not in color_hex else color_hex
    # Load the logo
    MIN_HEIGHT = 100
    logo_w, logo_h = logo_image.size  # original size
    logo_w, logo_h = (
        max(logo_h, logo_w)*MIN_HEIGHT // min(logo_h, logo_w),
        MIN_HEIGHT
    )  # resized dimensions
    logo = logo_image.resize((logo_w, logo_h))

    # Forms a new template
    T_WIDTH, T_HEIGHT = (768, 1024)
    ad_image = Image.new(mode="RGB", size=(T_WIDTH, T_HEIGHT), color="white")
    # Paste the product image onto it
    product_img = product_img.resize((512, 512))
    ad_image.paste(
        im=product_img,
        box=((T_WIDTH//2-product_img.size[0]//2, 196))
    )
    # Add the logo now
    logo_mask = logo.convert("RGBA")
    ad_image.paste(
        im=logo,
        box=(T_WIDTH//2-logo.size[0]//2, 32),
        mask=logo_mask
    )
    # Text & the drawing box
    draw = ImageDraw.Draw(ad_image)
    fnt = ImageFont.load_default(size=40)

    # Add the punchline text
    # Longer text should be wrapped
    lines = textwrap.wrap(punchline, width=30)
    line_y_coordinate, line_pad = (724, 20)
    for line in lines:
        w, h = (draw.textlength(text=line, font=fnt), 20)
        draw.text(
            xy=((T_WIDTH-w)//2, line_y_coordinate),
            text=line,
            fill=color_hex,
            font=fnt
        )
        line_y_coordinate += h + line_pad

    # Button to be added
    but_size = draw.textlength(text=button_text, font=fnt)
    but_position = ((T_WIDTH-but_size)//2, T_HEIGHT-150)
    draw.rectangle(
        xy=[
            but_position,
            (but_position[0] + but_size, but_position[1] + 50)
            ],
        fill=color_hex
    )
    draw.text(
        xy=but_position,
        text=button_text,
        fill="white",
        font=fnt,
        spacing=3
    )
    return ad_image
