from google.cloud.vision import ImageAnnotatorClient, Image
import os

def detect_safe_search(path):
    """Detects unsafe features in the file."""

    client = ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = Image(content=content)

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = (
        "UNKNOWN",
        "VERY_UNLIKELY",
        "UNLIKELY",
        "POSSIBLE",
        "LIKELY",
        "VERY_LIKELY",
    )
    print("Safe search:")
    adult = likelihood_name[safe.adult]
    print(f"adult: {adult}")
    if(adult == "VERY_LIKELY" or adult == "LIKELY" or adult == "POSSIBLE"):
        print("Adult content detected. Skipping...")
        return True
    return False
    #print(f"medical: {likelihood_name[safe.medical]}")
    #print(f"spoofed: {likelihood_name[safe.spoof]}")
    #print(f"violence: {likelihood_name[safe.violence]}")
    #print(f"racy: {likelihood_name[safe.racy]}")

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            file_path = os.path.join(folder_path, filename)
            print(f"Processing file: {file_path}")
            detect_safe_search(file_path)

if __name__ == "__main__":
    folder_path = "/Users/adam/Documents/COde/RelReels/Generated_Genesis/images/Genesis 3:[13-15]/generate_19.jpg"
    detect_safe_search(folder_path)