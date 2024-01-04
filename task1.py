import torch
import cv2 as cv
import numpy as np
from PIL import Image
from warnings import filterwarnings
from diffusers import StableDiffusionImg2ImgPipeline


filterwarnings("ignore")

# configure the device and load the model
DEVICE = "cpu"
if torch.backends.mps.is_available():
    DEVICE = torch.device("mps")
elif torch.cuda.is_available():
    DEVICE = torch.device("cuda")

MODEL_PATH = "runwayml/stable-diffusion-v1-5"
pipeline = StableDiffusionImg2ImgPipeline.from_pretrained(MODEL_PATH)
pipeline.to(DEVICE)


def create_new_image(
        pil_img: Image.Image,
        text_prompt: str,
        color_hex: str,
        steps: int,
        seed: int
) -> Image.Image:
    """
    Creates an image by using Stable Diffusion Img2Img model

    Args:
        - pil_img (PIL.Image.Image): Uploaded PIL image
        - text_prompt (str): Prompt to create the image
        - color_hex (str): The prominent color to be used in the created image
        - steps (int): Number of inference steps

    Returns:
        - new_image (PIL.Image.Image): New image created by the model
    """
    # HEX code should have in RGB format.
    assert len(color_hex.strip('#')) == 6, (
        "HEX code should be in RGB format with a string length 6. "
        "Alpha channel is not accepted."
    )
    # Remove # in front of the HEX code if exists
    color_hex = color_hex.strip('#') if '#' in color_hex else color_hex
    # Fix the generation process by providing manual seed
    generator = torch.Generator(device=DEVICE).manual_seed(seed)
    # Get original image
    orj_im = np.array(pil_img)
    # Create solid color
    hex_im = np.concatenate(
        (
            np.full(
                shape=(orj_im.shape[0], orj_im.shape[1], 1),
                fill_value=int(color_hex[0: 2], base=16),
                dtype=np.uint8
            ),
            np.full(
                shape=(orj_im.shape[0], orj_im.shape[1], 1),
                fill_value=int(color_hex[2: 4], base=16),
                dtype=np.uint8
            ),
            np.full(
                shape=(orj_im.shape[0], orj_im.shape[1], 1),
                fill_value=int(color_hex[4: 6], base=16),
                dtype=np.uint8
            )
        ),
        dtype=np.uint8,
        axis=2
    )
    # Blend these two together with equal weights
    blended_PIL_img = Image.fromarray(
        cv.addWeighted(
            src1=orj_im,
            alpha=0.5,
            src2=hex_im,
            beta=0.5,
            gamma=0.0
        )
    )
    # Run the StableDiffusion inference and return the output image
    with torch.no_grad():
        new_image = pipeline(
            prompt=text_prompt,
            image=blended_PIL_img,
            num_inference_steps=steps,
            generator=generator
        ).images[0]

    return new_image
