"""
BTH Triage Tool - filehash.py - File hashing and keyword search with filenames and content
"""
import os
import re
import hashlib
import fnmatch
import logging

# Configure logging
case_ref = input("Case Reference: ")
exhibit_ref = input("Exhibit Reference: ")
examiner = input("Examiner: ")
hash_matches = 0
keyword_matches = 0

logging.basicConfig(filename=exhibit_ref + ".log", level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
logging.info(f"\n**************************************************\nCase Reference: {case_ref} \nExhibit Reference: {exhibit_ref} \nExaminer: {examiner}\n **************************************************\n")

# Read the known hashes into a set for fast lookup
with open("hashset/catA.txt", "r") as a:
    catA = set(a.read().splitlines())
with open("hashset/catB.txt", "r") as b:
    catB = set(b.read().splitlines())
with open("hashset/catC.txt", "r") as c:
    catC = set(c.read().splitlines())
with open("hashset/cat4.txt", "r") as d:
    cat4 = set(d.read().splitlines())
with open("hashset/cat5.txt", "r") as e:
    cat5 = set(e.read().splitlines())

# Ask the user for the starting directory
path = input("Starting directory: ")
logging.info(f"Script started - File Path: {path}")

# Define the block size for reading files
BLOCKSIZE = 65536

# Keywords to search for
# Repeat lines below to add new keywords list - Change file names as needed
with open("keywords/keywords.txt", "r") as f:
    keywords = set(f.read().splitlines())

# Walk through the directory tree
for dirpath, dirnames, filenames in os.walk(path):
    # Process each file
    for file in filenames:
        file_path = os.path.join(dirpath, file)

        # Search for keywords in file names
        for keyword in keywords:
            if keyword.lower() in file.lower():
                logging.info(f"Found '{keyword}' in file name: {file_path}")
                print(f"Found '{keyword}' in file name: {file_path}")
                keyword_matches += 1

        # Search for keywords in document content
        if os.path.isfile(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as doc_file:
                    content = doc_file.read()
                    for keyword in keywords:
                        if re.search(rf"\b{re.escape(keyword)}\b", content, re.IGNORECASE):
                            logging.info(f"Found '{keyword}' in file name: {file_path}")
                            print(f"Found '{keyword}' in document: {file_path}")
                            keyword_matches += 1
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")

        # Compute hash value for media files
        if os.path.splitext(file)[1].lower() in [".jpeg", ".jpg", ".png", ".gif", ".mp3", ".mp4", ".avi", ".mkv", ".info"]:
            hasher = hashlib.sha256()
            try:
                with open(file_path, 'rb') as media_file:
                    block = media_file.read(BLOCKSIZE)
                    while block:
                        hasher.update(block)
                        block = media_file.read(BLOCKSIZE)
                hash_value = hasher.hexdigest()

                # Check if the hash value is in the known hashes
                if hash_value in catA | catB | catC | cat4 | cat5:
                    logging.info(f"Match found: {file_path}: {hash_value}")
                    print(f"{file_path}: {hash_value} (match)")
                    hash_matches += 1
                else:
                    logging.info(f"No match: {file_path}: {hash_value}")
                    # print(f"{file_path}: {hash_value} (no match)")
            except FileNotFoundError:
                logging.info(f"File not found: {file}")
                # print(f"File {file} not found.")
                continue

logging.info(f"Hash Values matched: {hash_matches}")
logging.info(f"Keywords matched: {keyword_matches}")

