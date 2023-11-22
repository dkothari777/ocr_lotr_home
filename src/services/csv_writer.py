import csv


class LotrCSVWriter():

    def __init__(self):
        pass

    def write_ranking_csv(self, lotr_dict):
        arr = []
        for v in lotr_dict.values():
            for i in v.get_player_score():
                arr.append(i.to_dict())
        self.write_file("ranking.csv", arr)
        return arr

    def write_total_csv(self, lotr_dict: dict):
        arr = []
        for v in lotr_dict.values():
            arr.append(v.to_dict())
        self.write_file("totals.csv", arr)
        return arr

    def write_attempt_csv(self, lotr_dict: dict):
        arr = []
        for v in lotr_dict.values():
            arr.append(v.to_attempts())
        self.write_file("attempts.csv", arr)
        return arr

    @staticmethod
    def write_file(filename, data):
        fieldnames = data[0].keys()
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                if "attempt_6" in row:
                    print(row)
                else:
                    writer.writerow(row)
        print(f'CSV file "{filename}" has been created.')
