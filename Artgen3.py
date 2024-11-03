from together import Together
import os
import moviepy.video.io.ImageSequenceClip
from dotenv import load_dotenv
import random
import requests
import json



def createVid(line, duration, output_path):
    load_dotenv()

    words = line.split()
    seed = random.randint(1, 1000)
    images = []
    for i, word in enumerate(words):
        images.append(createFrame(word, seed, f"Generated/temp/generate_{i}.png"))
    stitchFrames(images, duration, output_path)

    return output_path

def stitchFrames(images, duration, output_path):
    print(images)
    movie_clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(images, 1/(duration/len(images)))
    movie_clip.write_videofile(output_path)
    return output_path

def createFrame(description, seed, output_path):
    url = "https://api.together.xyz/v1/images/generations"
    payload = {
      "steps": 8,
      "n": 1,
      "model": "black-forest-labs/FLUX.1-schnell",
      "height": 1024,
      "width": 768,
      "seed": seed,
      "prompt": f"religiously, {description}",
      "negative_prompt": "buildings, people"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer " + os.environ.get("TOGETHER_API_KEY")
    }

    response = requests.post(url, json=payload, headers=headers)

    data = json.loads(response.content)
    image_url = data['data'][0]['url']
    response = requests.get(image_url)

    if response.status_code == 200:
        with open(output_path, "wb") as file:
            file.write(response.content)
        #print(f"Image saved as {output_path}'")
    return output_path

if __name__ == "__main__":
    load_dotenv()

    createVid("In the beginning of God's creation of the heavens and the earth.", 3.5, "Generated/Intermediate/test.png")
    #createFrame("In the beginning of God's creation of the heavens and the earth", 799, "example.png")
    
