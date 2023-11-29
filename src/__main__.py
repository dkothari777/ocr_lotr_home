import argparse
from src.services import directory
from src.model.model import LotrScore, LotrPlayerScore
from src.services import ocr
from src.services.crew_list import CrewListService
from src.services.csv_reader import LotrCSVReader
from src.services.csv_writer import LotrCSVWriter
from fuzzywuzzy import fuzz

def parse_images(path):
    dir_service = directory.DirectoryImageService(path)
    csv_service = LotrCSVWriter()
    list_of_images = dir_service.list_images()
    table_dict = {}
    line_number = 1
    for image in list_of_images:
        print(f"Parsing Image: {image}")
        lines = ocr.read_image(image)
        split_lines = lines.split("\n")
        count = 0
        for line in split_lines:
            if "Difficulty" in line:
                score = LotrScore()
                score.image_init(line, image, line_number)
                player_id = score.player_id
                # print(f"player_id: {player_id}, score: {score}")
                count += 1
                line_number += 1
                if player_id in table_dict.keys():
                    player_scores: LotrPlayerScore = table_dict[player_id]
                    player_scores.add(score)
                    table_dict[player_id] = player_scores
                else:
                    new_player_score = LotrPlayerScore(player_id)
                    new_player_score.add(score)
                    table_dict[player_id] = new_player_score
        print(f"Only Found {count} in {image}")
    dir_service.cleanup()
    csv_service.write_ranking_csv(table_dict)
    csv_service.write_total_csv(table_dict)


import re


def is_formatted_number(s):
    pattern = r'^-?\d{1,3}(,\d{3})*(\.\d+)?$'
    return bool(re.match(pattern, s))


def check_if_name_exist(line, crew_list):
    lower_line = line.strip().lower()
    for name in crew_list:
        if fuzz.ratio(lower_line, name.strip().lower()) > 85:
            return True
    return False


def get_name(line, crew_list):
    lower_line = line.strip().lower()
    for name in crew_list:
        if fuzz.ratio(lower_line, name.strip().lower()) > 85:
            return name
    return None


def parse_easyocr(images, crew_list_path):
    crew_list = CrewListService(crew_list_path).crew_list
    dir_service = directory.DirectoryImageService(images)
    csv_service = LotrCSVWriter()
    list_of_images = dir_service.list_images()
    table_dict = {}
    line_number = 1
    for image in list_of_images:
        print(f"Parsing Image: {image}")
        lines = ocr.read_easyocr_image(image)
        count = 0
        print(lines)
        for i in range(len(lines)):
            if check_if_name_exist(lines[i], crew_list):
                lotr_score = LotrScore()
                rank = line_number
                player_name = get_name(lines[i], crew_list)
                while "Difficulty" not in lines[i]:
                    i = i + 1
                difficulty = lines[i].lstrip("Difficulty").strip()
                while not is_formatted_number(lines[i]):
                    i = i + 1
                score = lines[i]
                lotr_score.ranking_init(rank, player_name, difficulty, score.replace(",", ""), False, image)
                count += 1
                if player_name in table_dict.keys():
                    player_scores: LotrPlayerScore = table_dict[player_name]
                    player_scores.add(lotr_score)
                    table_dict[player_name] = player_scores
                else:
                    new_player_score = LotrPlayerScore(player_name)
                    new_player_score.add(lotr_score)
                    table_dict[player_name] = new_player_score
                line_number = line_number + 1
        print(f"Only Found {count} in {image}")
    dir_service.cleanup()
    csv_service.write_ranking_csv(table_dict)
    csv_service.write_total_csv(table_dict)
    csv_service.write_attempt_csv(table_dict)


def parse_arguments():
    parser = argparse.ArgumentParser(description="A script with command-line arguments")
    parser.add_argument("--images", type=str, help="Zip or directory of images")
    parser.add_argument("--csv", type=str, help="ranking csv file")
    parser.add_argument("--easy-ocr", type=bool, default=False, help="use easy-ocr instead of pytesseract")
    parser.add_argument("--crew-list", type=str, help="crew list required by easy-ocr")
    return parser.parse_args()


def parse_csv(path):
    print(f"Parsing csv {path}")
    csv_reader = LotrCSVReader()
    csv_writer = LotrCSVWriter()
    table_dict = csv_reader.read_csv(path)
    csv_writer.write_attempt_csv(table_dict)


if __name__ == '__main__':
    args = parse_arguments()
    if args.easy_ocr is not None and args.crew_list is not None and args.images is not None:
        parse_easyocr(args.images, args.crew_list)
    elif args.images is not None:
        parse_images(args.images)
    elif args.csv is not None:
        parse_csv(args.csv)
    else:
        print("Error proper arguments not found!")
