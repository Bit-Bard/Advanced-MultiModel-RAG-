# Temporarily mocked/disabled due to Gemini free-tier quota limits during development testing.
# import google.generativeai as genai
# from PIL import Image
#
# from llm.model_config import configure_genai
#
# configure_genai()
# model = genai.GenerativeModel("models/gemini-2.0-flash")
#
# def analyze_image(image_path):
#
#     image = Image.open(image_path)
#
#     response = model.generate_content([
#         "Describe this image in detail",
#         image
#     ])
#
#     return response.text

def analyze_image(image_path):
    return "Image understanding temporarily disabled."