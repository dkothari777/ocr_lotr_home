import csv

from src.model.model import LotrPlayerScore, LotrScore


class LotrCSVReader:

    def __init__(self):
        pass

    @staticmethod
    def read_csv(path):
        table_dict = {}
        with open(path) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                player_id = row["player_id"]
                score = LotrScore()
                if "line_number" in row:
                    score.ranking_init(row["line_number"],
                                       row["player_id"],
                                       row["difficulty"],
                                       row["score"],
                                       row["possible_duplicate"],
                                       row["image_file"])
                else:
                    score.ranking_init(-1,
                                       row["player_id"],
                                       row["difficulty"],
                                       row["score"],
                                       row["possible_duplicate"],
                                       row["image_file"])
                if player_id in table_dict.keys():
                    player_scores: LotrPlayerScore = table_dict[player_id]
                    player_scores.add(score)
                    table_dict[player_id] = player_scores
                else:
                    new_player_score = LotrPlayerScore(player_id)
                    new_player_score.add(score)
                    table_dict[player_id] = new_player_score
        return table_dict
