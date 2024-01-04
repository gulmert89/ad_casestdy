import io
# import base64
import uvicorn
from PIL import Image
from datetime import datetime
from task1 import create_new_image
from task2 import create_ad_template
from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException, UploadFile, File


case_app = FastAPI()


@case_app.get("/")
async def home_page():
    return {
        "message": (
            "You are in! ...but maybe you should visit the page "
            "'...:8000/docs' to play with a GUI. There is nothing "
            "to do here really :|")
        }


@case_app.post("/create_image")
async def create_image(
    text_prompt: str,
    color_hex: str,
    inference_steps: int = 10,
    inference_seed: int = 42,
    reference_img: UploadFile = File(...)
) -> FileResponse:
    # Read the uploaded image
    image_data = await reference_img.read()
    reference_img = Image.open(io.BytesIO(image_data)).resize((512, 512))

    try:
        # import the function from task1
        generated_img = create_new_image(
            pil_img=reference_img,
            text_prompt=text_prompt,
            color_hex=color_hex,
            steps=inference_steps,
            seed=inference_seed
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Save the template
    now = datetime.today().strftime("%d%m%Y-%H%M%S")
    img_path = f"generated_imgs/your_img_{now}.png"
    generated_img.save(img_path)
    return FileResponse(path=img_path)


@case_app.post("/create_ad")
async def create_ad(
    punchline: str,
    button_text: str,
    color_hex: str,
    uploaded_base_img: UploadFile = File(...),
    uploaded_logo: UploadFile = File(...)
 ) -> FileResponse:
    # Read the uploaded image
    base_img = await uploaded_base_img.read()
    logo = await uploaded_logo.read()
    base_img = Image.open(io.BytesIO(base_img))
    logo = Image.open(io.BytesIO(logo))

    try:
        # Import the function from task2
        generated_ad = create_ad_template(
            product_img=base_img,
            logo_image=logo,
            color_hex=color_hex,
            punchline=punchline,
            button_text=button_text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Convert image to byte and return
    # img_byte_arr = io.BytesIO()
    # generated_ad.save(img_byte_arr, format='PNG')
    # img_byte_arr = img_byte_arr.getvalue()
    # encoded_img = base64.b64encode(img_byte_arr)

    # Save the template
    now = datetime.today().strftime("%d%m%Y-%H%M%S")
    img_path = f"generated_imgs/your_ad_{now}.png"
    generated_ad.save(img_path)
    return FileResponse(path=img_path)

if __name__ == "__main__":
    uvicorn.run(
        app=case_app,
        host="0.0.0.0",
        port=8000
    )
