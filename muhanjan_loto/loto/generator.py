import os
import random
from collections import Counter
from re import T
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import json


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
FONT_PATH = os.path.join(DIR_PATH, "Font/HussarBd.otf")
COLUMNS = [[1, 9],
           [10, 19],
           [20, 29],
           [30, 39],
           [40, 49],
           [50, 59],
           [60, 69],
           [70, 79],
           [80, 90]]


class LotoGenerator():

    @staticmethod
    def generate_loto(loto):
        loto_items = sorted(json.loads(loto))
        loto_items_copy = sorted(json.loads(loto))

        items_per_row = []

        for _ in range(1, 4):
            cols = []
            for _ in range(5):
                decade_list = []
                for idx, col in enumerate(COLUMNS):
                    for item in loto_items_copy:
                        if item >= col[0] and item <= col[1]:
                            decade_list.append(idx+1)

                while max(Counter(decade_list), key=Counter(decade_list).get) in cols:
                    decade_list.remove(
                        max(Counter(decade_list), key=Counter(decade_list).get))
                new_num = max(Counter(decade_list),
                                key=Counter(decade_list).get)

                loto_items_copy.remove([el for el in loto_items_copy if el >=
                                        COLUMNS[new_num-1][0] and el <= COLUMNS[new_num-1][1]][0])
                cols.append(new_num)

            cols = sorted(cols)

            row_items = []
            for col in cols:
                item = [el for el in loto_items if el >=
                        COLUMNS[col-1][0] and el <= COLUMNS[col-1][1]][0]
                row_items.append(item)
                loto_items.remove(item)

            items_per_row.append(row_items)

        loto = []
        for row in items_per_row:
            row_data = []
            for d in range(9):
                i_data = 0
                for i in row:
                    if i // 10 == d or (i == 90 and d == 8):
                        i_data = i
                        break
                row_data.append(i_data)
            loto.append(row_data)

        return loto

    @staticmethod
    def generate_lotteries(count=10):
        lotteries = {}
        index = 1
        while len(lotteries) != count:
            dec_count = {0: 0, 1: 0, 2: 0, 3: 0,
                         4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
            loto = []
            for _ in range(15):
                new_item = 0
                while new_item == 0 or new_item in loto or dec_count[new_item//10] == 3:
                    new_item = random.randint(1, 90)
                    if dec_count[8] == 3 and new_item == 90:
                        new_item = 0
                    if dec_count[8] != 3 and new_item == 90:
                        dec_count[8] += 1
                if new_item != 90:
                    dec_count[new_item//10] = dec_count[new_item//10] + 1
                loto.append(new_item)
            loto = sorted(loto)
            if loto not in list(lotteries.values()):
                lotteries[index] = sorted(loto)
                index += 1

        return lotteries


if __name__ == "__main__":
    # generator.generate_images("lotteries.txt")
    print(LotoGenerator.generate_loto("[6, 11, 19, 29, 32, 36, 37, 40, 44, 59, 62, 63, 64, 70, 76]"))
