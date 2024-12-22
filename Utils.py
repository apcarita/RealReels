import datetime
from pydub import AudioSegment
from dotenv import load_dotenv
import os
import pickle
from openai import OpenAI

def log(book):
    current_time = datetime.datetime.now()

    log_dir = f'Logs/{book}'
    os.makedirs(log_dir, exist_ok=True)

    # Reading
    print(f"loading logs for Logs/{book}/Chapter.pkl")
    if not os.path.exists(f'Logs/{book}/Chapter.pkl'):
        with open(f'Logs/{book}/Chapter.pkl', 'wb') as f:
            pickle.dump(1, f)
        with open(f'Logs/{book}/Part.pkl', 'wb') as f:
            pickle.dump(1, f)
        with open(f'Logs/{book}Upload_Queue.pkl', 'wb') as f:
            pickle.dump([], f)
    with open(f'Logs/{book}/Chapter.pkl', 'rb') as f:
        chapter = pickle.load(f)
    
    with open(f'Logs/{book}/Part.pkl', 'rb') as f:
        line = pickle.load(f) 

    with open(f"Logs/{book}/log", "a") as log_file:
        print(f"Running at {current_time}... working on chapter: {chapter}:{line}")
        log_file.write(f"Script ran at: {current_time} | Generating Genesis {chapter}:{line}\n")


    return chapter, line

def findHowManyLines(book, chapter, line, max_words):
    if(book == "Genesis"):
        lines, _ = getChapter(book, chapter)
    else:
        lines, _ = getChapterBook(book, chapter)
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
        if lines[i].strip().startswith("Chapter") or lines[i].strip() == "":
            continue
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

def logComplete(book, chapter, text, startline, lastline, output_path):
     # Writing
    current_time = datetime.datetime.now()
    title = f"{book} {chapter}:[{startline}-{lastline}]"

    with open(f'Logs/{book}/Chapter.pkl', 'wb') as f:
      pickle.dump(chapter, f)
    with open(f'Logs/{book}/Part.pkl', 'wb') as f:
      pickle.dump(lastline, f)
    with open(f"Logs/{book}/log", "a") as log_file:
        print(f"Completing at {current_time}... {chapter}.{startline}-{lastline} saved to {output_path}")
        log_file.write(f"Completing at {current_time}... {chapter}.{startline}-{lastline} saved to {output_path}\n")

    complete = []
    with open(f'Logs/{book}/Upload_Queue.pkl', 'rb') as f:
        complete = pickle.load(f) 
    print(complete)

    if(complete != []):
        print("appending")
        complete.append([title, text, output_path])
    else:
        complete = [title, text, output_path]
        print(f"complete: {complete}")
    with open(f'Logs/{book}/Upload_Queue.pkl', 'wb') as f:
      pickle.dump(complete, f)
def setLine(book, chapter, line):
    with open(f'Logs/{book}/Chapter.pkl', 'wb') as f:
      pickle.dump(chapter, f)
    with open(f'Logs/{book}/Part.pkl', 'wb') as f:
      pickle.dump(line, f)
    print(f"setting line to {chapter}:{line}")


def uploadQueue(book):
    log_dir = f'Logs/{book}'
    os.makedirs(log_dir, exist_ok=True)
    file_path = os.path.join(log_dir, 'Upload_Queue.pkl')
    
    print(f"loading logs for {file_path}")
    if not os.path.exists(file_path):
        complete = []
        with open(file_path, 'wb') as f:
            pickle.dump(complete, f)
    else:
        try:
            with open(file_path, 'rb') as f:
                complete = pickle.load(f)
        except EOFError:
            complete = []
    return complete

def RemoveUploadQueue(book):
    complete = []
    with open(f'Logs/{book}/Upload_Queue.pkl', 'wb') as f:
        pickle.dump(complete, f)
    print(complete)


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

def describe(text, safty):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {   "role": "user",
                "content": f"{safty} \n {text}"}
        ]
    )
    description = ' '.join(completion.choices[0].message.content.split()[:50])
    print(description)


    return description
if __name__ == "__main__":
    #RemoveUploadQueue("Genesis")
    #print(getChapterBook("Frosty", 1))

    RemoveUploadQueue("Genesis")
    book = "Frosty"
    #setLine(book, 1, 1)
    #logComplete(book, 7,"sdad", 0, 25, "output_path")
    #RemoveUploadQueue("Genesis")
    with open(f'Logs/{book}Upload_Queue.pkl', 'wb') as f:
            pickle.dump([], f)

    text = findHowManyLines("Genesis", 3, 22, 95)
    print(text[0])
    #describe(text[0])
    #print(describe(" Once upon a snowy morning in the cozy town of Evergreen Hills, a group of children rushed outside, eager to build their annual snowman. The air was crisp, and the ground was blanketed with fresh, powdery snow—the perfect day for snowman building. The children worked together, rolling the snow into three large, round balls, stacking them one on top of the other. Soon, they had built a snowman that was the envy of the neighborhood. They named him Frosty, and he had a carrot nose, coal eyes, and a big, friendly smile. "))
   # describe(text)

    #test()
    #describe(findHowManyLines("Genisis", 1, 1, 100)[0])

    
    #log()
    #print(getLines("Genisis", 1, [1, 2, 3, 4, 5]))
