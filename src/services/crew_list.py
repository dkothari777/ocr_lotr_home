import os


class CrewListService:

    def __init__(self, path):
        self.crew_list = sorted(self.__read_file(path))

    @staticmethod
    def __read_file(path):
        if os.path.exists(path):
            with open(path, 'r') as fs:
                player_names = [line.strip() for line in fs if line.strip()]
            return player_names
        raise Exception(f"File {path} not found!")
