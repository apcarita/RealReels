import datetime
from pydub import AudioSegment
from dotenv import load_dotenv
import os
import pickle
from openai import OpenAI

def log():
    current_time = datetime.datetime.now()
    # Reading
    with open('Logs/Chapter.pkl', 'rb') as f:
        chapter = pickle.load(f)
    
    with open('Logs/Part.pkl', 'rb') as f:
        line = pickle.load(f) 

    with open("Logs/log", "a") as log_file:
        print(f"Running at {current_time}... working on chapter: {chapter}:{line}")
        log_file.write(f"Script ran at: {current_time} | Generating Genisis {chapter}:{line}\n")
    return chapter, line

def findHowManyLines(book, chapter, line, max_words):
    lines, _ = getChapter(book, chapter)
    #print(f"Lines from chapter {chapter}:{line}")

    selected_lines = []
    total_words = 0
    total_chars = 0
    last_line_number = line
    nchapter = chapter
    print(len(lines))
    if(line >= len(lines)):
        nchapter = chapter + 1
        lines, _ = getChapter(book, nchapter)
        line = 1
        print("line does not exist; next chapter")
    for i in range(line - 1, len(lines)):
        words_in_line = len(lines[i].split())
        chars_in_line = len(lines[i])
        if (total_words + words_in_line > max_words) or (total_chars + chars_in_line > 900):
            if not selected_lines:
                selected_lines.append(lines[i])
                last_line_number = i + 1
            break
        if(i >= len(lines)):
            selected_lines.append(lines[i])
            nchapter = chapter + 1
            lines, _ = getChapter(book, nchapter)
            i = 0
            line = 1
            break
        print(f"adding line {i+1}: {lines[i]}")
        selected_lines.append(lines[i])
        total_words += words_in_line
        total_chars += chars_in_line
        last_line_number = i + 2

        print("last Line number: ", last_line_number)

    return selected_lines, last_line_number, nchapter

def logComplete(chapter, startline, lastline, output_path):
     # Writing
    current_time = datetime.datetime.now()

    with open('Logs/Chapter.pkl', 'wb') as f:
      pickle.dump(chapter, f)

    with open('Logs/Part.pkl', 'wb') as f:
      pickle.dump(lastline, f)
    with open("Logs/log", "a") as log_file:
        print(f"Completing at {current_time}... {chapter}.{startline}-{lastline} saved to {output_path}")
        log_file.write(f"Completing at {current_time}... {chapter}.{startline}-{lastline} saved to {output_path}\n")

def getChapter(book, chapter):
    lines = []
    with open(book, "r") as file:
        for line in file:
            # Check if the line starts with '1'
            if line.strip().startswith(f"{chapter}:"):
                # Remove all digits and strip whitespace
                cleaned_line = ''.join(filter(lambda x: not x.isdigit(), line)).strip()[2:]
                lines.append(cleaned_line)
        text = ' '.join(lines)
    return lines, text

def getChapterBook(book, chapter_number):
    chapters = []
    current_chapter_lines = []
    with open(book, 'r') as file:
        for line in file:
            if line.strip().startswith('Chapter'):
                if current_chapter_lines:
                    chapters.append(current_chapter_lines)
                    current_chapter_lines = []
                # Include the chapter heading if needed
                current_chapter_lines.append(line.strip())
            else:
                current_chapter_lines.append(line.strip())
        if current_chapter_lines:
            chapters.append(current_chapter_lines)
    
    # Debugging output
    print(f"Total chapters found: {len(chapters)}")
    for i, chap in enumerate(chapters, 1):
        print(f"Chapter {i} has {len(chap)} lines")

    if 1 <= chapter_number <= len(chapters):
        chapter_lines = chapters[chapter_number - 1]
        text = ' '.join(chapter_lines)
        return chapter_lines, text
    else:
        return [], ''

def getLines(book, chapter, lines):
    chap = getChapter(book, chapter)
    selected_lines = [chap[0][i-1] for i in lines if 0 < i <= len(chap[0])]
    return selected_lines

def test():
    Book = "Genisis"
    chapter, start_line = log()
    max_words = 80
    lines, lineNumber, nc = findHowManyLines(Book, chapter, start_line, max_words)
    logComplete(nc, start_line, lineNumber, "dsafasd")

def describe(text):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {   "role": "user",
                "content": f"Describe the following bible verse in detail and order for an ai image generation model in LESS THAN 400 character or 50 words. get right into the description, avoid starting with an intro, and DO NOT INCLUDE NAKED PEOPLE, say they are covered in leaves. avoid names Adam and Eve {text}"}
        ]
    )
    description = completion.choices[0].message.content
    print(description)


    return description
if __name__ == "__main__":
    #lines, _ = getChapter("genisis", 1)
    #logComplete(2, 0, 4, "test.mp3")

    with open('Logs/Chapter.pkl', 'rb') as f:
        chapter = pickle.load(f)
    
    with open('Logs/Part.pkl', 'rb') as f:
        line = pickle.load(f) 

    print(getChapterBook("A Court Of Thorns.txt", 1))

    #print(chapter, line)

    #text = findHowManyLines("Genisis", 2, 24, 100)

    #print(text)
    #describe(text)

    #test()
    #describe(findHowManyLines("Genisis", 1, 1, 100)[0])

    
    #log()
    #print(getLines("Genisis", 1, [1, 2, 3, 4, 5]))
