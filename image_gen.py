import text_gen
import requests
from PIL import Image
import os
# from dotenv import load_dotenv
import openai
from openai import OpenAI

# load_dotenv(FILE_PATH_TO_ENV)
openai.api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI()

def image_url_gen(prompt: str) -> str:
    response = client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        size="512x512",
        n=1
    )
    image_url = response.data[0].url

    return image_url


def image_download(url: str, page_no: int):
    image = requests.get(url).content
    
    file_name = "static/images/" + str(page_no) + ".jpg"
    f = open(file_name,'wb')
    f.write(image) 
    f.close() 


def image(prompt: str, page_no: int):
    image_url = image_url_gen(prompt)
    image_download(image_url, page_no)