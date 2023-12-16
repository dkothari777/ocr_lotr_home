from array import array
import re


class LotrScore(object):

    def __init__(self):
        self.hashcode = None
        self.image = None
        self.possible_duplicate = None
        self.score = None
        self.difficulty = None
        self.player_id = None
        self.line_number = None

    def __int__(self):
        pass

    def ranking_init(self, line_number, player_id, difficulty, score, possible_duplicate, image):
        self.line_number = int(line_number)
        self.player_id = player_id
        self.difficulty = int(difficulty.strip("_"))
        self.score = int(score)
        self.possible_duplicate = bool(possible_duplicate)
        self.image = image
        self.hashcode = hash(str(line_number) + player_id + str(difficulty) + str(score) + str(possible_duplicate) + image)

    def image_init(self, line, image, line_number):
        line_splits = line.split("|")
        self.player_id, index = self.parse_player_id(line_splits)
        self.difficulty, index = self.parse_difficulty(line_splits, index)
        self.score, index = self.parse_score(line_splits, index)
        self.hashcode = hash(line)
        self.possible_duplicate = False
        self.image = image
        self.line_number = line_number

    @staticmethod
    def parse_player_id(arr_text, starting_index=0):
        for index in range(starting_index, len(arr_text)):
            text = arr_text[index]
            all_of_them = re.findall(r'[A-Za-z0-9]{4,}', text)
            if len(all_of_them) != 0:
                return all_of_them[0].strip(), index + 1
        return arr_text[0] + arr_text[1], starting_index

    @staticmethod
    def parse_difficulty(arr_text, starting_index):
        pattern = r'(Difficulty\s*(\d+))'
        for index in range(starting_index, len(arr_text)):
            text = arr_text[index]
            if "Difficulty" in text:
                match = re.search(pattern, text)
                if match:
                    return int(match.group(2)), index + 1
        return -1, starting_index

    @staticmethod
    def parse_score(arr_text, starting_index):
        arr_text = arr_text[::-1]
        pattern = r'\d{2,3}(?:,\d{3})*'
        for index in range(0, len(arr_text)):
            text = arr_text[index].strip()
            matches = re.findall(pattern, text)
            if len(matches) != 0:
                return int(matches[0].replace(',', '')), index + 1
        return -1, starting_index

    def __str__(self):
        return f"player_id: {self.player_id}, difficulty: {self.difficulty}, score: {self.score}, " \
               f"possible_duplicate: {self.possible_duplicate}"

    def to_dict(self):
        return {"line_number": self.line_number, "player_id": self.player_id, "difficulty": self.difficulty,
                "score": self.score,
                "possible_duplicate": self.possible_duplicate, "image_file": self.image}


class LotrPlayerScore(object):

    def __init__(self, player_id):
        self.player_id = player_id
        self.player_score = []
        self.score = 0
        self.battles = 0

    def add(self, score: LotrScore):
        for s in self.player_score:
            if s.hashcode == score.hashcode:
                score.possible_duplicate = True
        self.player_score.append(score)
        self.score += score.score
        self.battles += 1

    def total_score(self):
        return self.score

    def total_battles(self):
        return self.battles

    def get_player_score(self):
        return self.player_score

    def __str__(self):
        return f"{self.player_score}, total_score: {self.score}, total_battles: {self.battles}"

    def to_dict(self):
        return {'player_id': self.player_id, 'total_battles': self.total_battles(), 'total_score': self.total_score()}

    def to_attempts(self):
        player_dict = {}
        player_dict["player_id"] = self.player_id
        for x in range(len(self.player_score)):
            attempt_number = x + 1
            player_dict[f"attempt_{attempt_number}"] = self.player_score[x].score
        player_dict["total_score"] = self.score
        return player_dict
