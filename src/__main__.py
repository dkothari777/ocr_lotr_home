import argparse
from src.services import directory
from src.model.model import LotrScore, LotrPlayerScore
from src.services import ocr
from src.services.csv_writer import LotrCSVWriter


def main(path):
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
                score = LotrScore(line, image, line_number)
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


def parse_arguments():
    parser = argparse.ArgumentParser(description="A script with command-line arguments")
    parser.add_argument("images", type=str, help="Zip or directory of images")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    main(args.images)
