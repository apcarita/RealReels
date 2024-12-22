from ReelCreator import *

def main():
    christmasHashTags = ['#Christmas', '#MerryChristmas', '#ChristmasEve', '#ChristmasTree', '#HolidaySeason', '#SantaClaus', '#Xmas']
    finalVideo, title, text = CreateReel("christmas: ", "Frosty", 95,"Frosty The Snowman (Instrumental).mp3", "1wg2wOjdEWKA7yQD8Kca")
    upload(finalVideo, title, text, christmasHashTags)


if __name__ == "__main__":
    main()
