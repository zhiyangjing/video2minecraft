from cv2 import VideoCapture, imwrite, waitKey
from numpy import array
from os import path, makedirs
from PIL import Image
from sys import argv, exit
from shutil import rmtree
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, \
    QLineEdit, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout, QMessageBox, QProgressBar
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThread, pyqtSignal


class Getconf(QWidget):
    def __init__(self):
        super(Getconf, self).__init__()
        self.resize(800, 500)
        self.setFixedSize(800, 500)
        font = QFont('Arial')
        font.setPointSize(18)

        self.video_path_label = QLabel("Video path:", self)
        self.name_space_label = QLabel("Name space:", self)
        self.video_size_label = QLabel("Video size:", self)
        self.single_frame_interval_label = QLabel("Frame interval:", self)
        self.display_delay_label = QLabel("Display delay", self)
        self.video_path_label.setFont(font)
        self.name_space_label.setFont(font)
        self.video_size_label.setFont(font)
        self.single_frame_interval_label.setFont(font)
        self.display_delay_label.setFont(font)

        self.video_path_line = QLineEdit(self)
        self.name_space_line = QLineEdit(self)
        self.video_size_line = QLineEdit(self)
        self.single_frame_interval_line = QLineEdit(self)
        self.display_delay_line = QLineEdit(self)
        self.video_path_line.setFont(font)
        self.name_space_line.setFont(font)
        self.video_size_line.setFont(font)
        self.single_frame_interval_line.setFont(font)
        self.display_delay_line.setFont(font)

        self.commit_button = QPushButton("Start generating", self)
        self.commit_button.setFont(font)
        self.commit_button.setFixedWidth(300)
        self.commit_button.clicked.connect(self.start_generate_func)

        self.grid_layout = QGridLayout()
        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.video_path = ""
        self.name_space = ""
        self.video_size = ""
        self.single_frame_interval = ""
        self.display_delay = ""
        self.output_path = ""
        self.func_path = ""
        self.json_path = ""
        self.num = 0

        self.layout_init()

    def layout_init(self):
        self.grid_layout.addWidget(self.video_path_label, 0, 0, 4, 1)
        self.grid_layout.addWidget(self.video_path_line, 0, 1, 4, 1)
        self.grid_layout.addWidget(self.name_space_label, 1, 0, 4, 1)
        self.grid_layout.addWidget(self.name_space_line, 1, 1, 4, 1)
        self.grid_layout.addWidget(self.video_size_label, 2, 0, 4, 1)
        self.grid_layout.addWidget(self.video_size_line, 2, 1, 4, 2)
        self.grid_layout.addWidget(self.single_frame_interval_label, 3, 0, 4, 1)
        self.grid_layout.addWidget(self.single_frame_interval_line, 3, 1, 4, 1)
        self.grid_layout.addWidget(self.display_delay_label, 4, 0, 4, 1)
        self.grid_layout.addWidget(self.display_delay_line, 4, 1, 4, 1)

        self.v_layout.addLayout(self.grid_layout)
        self.v_layout.addWidget(self.commit_button)

        self.setLayout(self.v_layout)

    def start_generate_func(self):
        self.video_path = self.video_path_line.text()
        self.name_space = self.name_space_line.text()
        try:
            self.video_size = eval(self.video_size_line.text())
        except:
            print("Invalid height width")
        try:
            self.single_frame_interval = int(self.single_frame_interval_line.text())
        except:
            pass
        self.display_delay = float(self.display_delay_line.text())
        name = self.video_path.split("/")[-1].split(".")[0]
        self.output_path, self.func_path, self.json_path = make_dirs(name, self.name_space)
        self.num = video_process(self.output_path, self.video_path, self.single_frame_interval)
        doc = open("./datapacks/output/pack.mcmeta", 'w')
        doc.write(meta)
        doc.close()
        multiple = 5
        res = {(8, 8, 8): 101, (0, 0, 0): 92, (0, 0, 1): 27, (0, 0, 2): 65, (0, 0, 3): 17, (0, 0, 4): 46, (0, 0, 5): 46,
               (0, 0, 6): 46, (0, 0, 7): 46, (0, 1, 0): 43, (0, 1, 1): 65, (0, 1, 2): 65, (0, 1, 3): 17, (0, 1, 4): 46,
               (0, 1, 5): 46, (0, 1, 6): 46, (0, 1, 7): 46, (0, 2, 0): 79, (0, 2, 1): 85, (0, 2, 2): 85, (0, 2, 3): 0,
               (0, 2, 4): 17, (0, 2, 5): 46, (0, 2, 6): 46, (0, 2, 7): 64, (0, 3, 0): 99, (0, 3, 1): 85, (0, 3, 2): 85,
               (0, 3, 3): 67, (0, 3, 4): 67, (0, 3, 5): 67, (0, 3, 6): 64, (0, 3, 7): 64, (0, 4, 0): 99, (0, 4, 1): 85,
               (0, 4, 2): 0, (0, 4, 3): 67, (0, 4, 4): 67, (0, 4, 5): 64, (0, 4, 6): 64, (0, 4, 7): 64, (0, 5, 0): 30,
               (0, 5, 1): 30, (0, 5, 2): 72, (0, 5, 3): 72, (0, 5, 4): 72, (0, 5, 5): 64, (0, 5, 6): 64, (0, 5, 7): 64,
               (0, 6, 0): 30, (0, 6, 1): 30, (0, 6, 2): 72, (0, 6, 3): 72, (0, 6, 4): 72, (0, 6, 5): 64, (0, 6, 6): 64,
               (0, 6, 7): 64, (0, 7, 0): 30, (0, 7, 1): 30, (0, 7, 2): 72, (0, 7, 3): 72, (0, 7, 4): 64, (0, 7, 5): 64,
               (0, 7, 6): 64, (0, 7, 7): 64, (1, 0, 0): 3, (1, 0, 1): 27, (1, 0, 2): 1, (1, 0, 3): 17, (1, 0, 4): 46,
               (1, 0, 5): 46, (1, 0, 6): 46, (1, 0, 7): 41, (1, 1, 0): 56, (1, 1, 1): 19, (1, 1, 2): 1, (1, 1, 3): 17,
               (1, 1, 4): 46, (1, 1, 5): 46, (1, 1, 6): 46, (1, 1, 7): 46, (1, 2, 0): 79, (1, 2, 1): 88, (1, 2, 2): 37,
               (1, 2, 3): 81, (1, 2, 4): 46, (1, 2, 5): 46, (1, 2, 6): 68, (1, 2, 7): 64, (1, 3, 0): 99, (1, 3, 1): 37,
               (1, 3, 2): 37, (1, 3, 3): 0, (1, 3, 4): 72, (1, 3, 5): 68, (1, 3, 6): 64, (1, 3, 7): 64, (1, 4, 0): 30,
               (1, 4, 1): 51, (1, 4, 2): 0, (1, 4, 3): 72, (1, 4, 4): 72, (1, 4, 5): 64, (1, 4, 6): 64, (1, 4, 7): 64,
               (1, 5, 0): 30, (1, 5, 1): 30, (1, 5, 2): 72, (1, 5, 3): 72, (1, 5, 4): 35, (1, 5, 5): 64, (1, 5, 6): 64,
               (1, 5, 7): 64, (1, 6, 0): 30, (1, 6, 1): 30, (1, 6, 2): 35, (1, 6, 3): 35, (1, 6, 4): 35, (1, 6, 5): 64,
               (1, 6, 6): 64, (1, 6, 7): 64, (1, 7, 0): 30, (1, 7, 1): 30, (1, 7, 2): 35, (1, 7, 3): 35, (1, 7, 4): 35,
               (1, 7, 5): 64, (1, 7, 6): 64, (1, 7, 7): 64, (2, 0, 0): 22, (2, 0, 1): 29, (2, 0, 2): 29, (2, 0, 3): 60,
               (2, 0, 4): 60, (2, 0, 5): 41, (2, 0, 6): 41, (2, 0, 7): 41, (2, 1, 0): 75, (2, 1, 1): 18, (2, 1, 2): 1,
               (2, 1, 3): 60, (2, 1, 4): 60, (2, 1, 5): 41, (2, 1, 6): 41, (2, 1, 7): 41, (2, 2, 0): 99, (2, 2, 1): 78,
               (2, 2, 2): 20, (2, 2, 3): 81, (2, 2, 4): 52, (2, 2, 5): 52, (2, 2, 6): 68, (2, 2, 7): 68, (2, 3, 0): 99,
               (2, 3, 1): 49, (2, 3, 2): 98, (2, 3, 3): 96, (2, 3, 4): 52, (2, 3, 5): 68, (2, 3, 6): 68, (2, 3, 7): 68,
               (2, 4, 0): 30, (2, 4, 1): 51, (2, 4, 2): 96, (2, 4, 3): 96, (2, 4, 4): 35, (2, 4, 5): 68, (2, 4, 6): 68,
               (2, 4, 7): 68, (2, 5, 0): 30, (2, 5, 1): 30, (2, 5, 2): 96, (2, 5, 3): 35, (2, 5, 4): 35, (2, 5, 5): 68,
               (2, 5, 6): 68, (2, 5, 7): 68, (2, 6, 0): 30, (2, 6, 1): 30, (2, 6, 2): 35, (2, 6, 3): 35, (2, 6, 4): 35,
               (2, 6, 5): 68, (2, 6, 6): 68, (2, 6, 7): 64, (2, 7, 0): 30, (2, 7, 1): 30, (2, 7, 2): 77, (2, 7, 3): 35,
               (2, 7, 4): 35, (2, 7, 5): 35, (2, 7, 6): 64, (2, 7, 7): 64, (3, 0, 0): 86, (3, 0, 1): 39, (3, 0, 2): 54,
               (3, 0, 3): 60, (3, 0, 4): 41, (3, 0, 5): 41, (3, 0, 6): 41, (3, 0, 7): 41, (3, 1, 0): 75, (3, 1, 1): 21,
               (3, 1, 2): 54, (3, 1, 3): 60, (3, 1, 4): 41, (3, 1, 5): 41, (3, 1, 6): 41, (3, 1, 7): 41, (3, 2, 0): 71,
               (3, 2, 1): 78, (3, 2, 2): 69, (3, 2, 3): 23, (3, 2, 4): 23, (3, 2, 5): 41, (3, 2, 6): 41, (3, 2, 7): 68,
               (3, 3, 0): 49, (3, 3, 1): 51, (3, 3, 2): 98, (3, 3, 3): 10, (3, 3, 4): 6, (3, 3, 5): 59, (3, 3, 6): 68,
               (3, 3, 7): 68, (3, 4, 0): 30, (3, 4, 1): 51, (3, 4, 2): 12, (3, 4, 3): 6, (3, 4, 4): 59, (3, 4, 5): 59,
               (3, 4, 6): 68, (3, 4, 7): 68, (3, 5, 0): 30, (3, 5, 1): 77, (3, 5, 2): 12, (3, 5, 3): 35, (3, 5, 4): 59,
               (3, 5, 5): 59, (3, 5, 6): 68, (3, 5, 7): 68, (3, 6, 0): 30, (3, 6, 1): 77, (3, 6, 2): 77, (3, 6, 3): 35,
               (3, 6, 4): 35, (3, 6, 5): 50, (3, 6, 6): 50, (3, 6, 7): 50, (3, 7, 0): 77, (3, 7, 1): 77, (3, 7, 2): 77,
               (3, 7, 3): 35, (3, 7, 4): 50, (3, 7, 5): 50, (3, 7, 6): 50, (3, 7, 7): 50, (4, 0, 0): 73, (4, 0, 1): 73,
               (4, 0, 2): 54, (4, 0, 3): 54, (4, 0, 4): 41, (4, 0, 5): 41, (4, 0, 6): 45, (4, 0, 7): 45, (4, 1, 0): 36,
               (4, 1, 1): 33, (4, 1, 2): 33, (4, 1, 3): 100, (4, 1, 4): 45, (4, 1, 5): 45, (4, 1, 6): 45, (4, 1, 7): 45,
               (4, 2, 0): 36, (4, 2, 1): 83, (4, 2, 2): 100, (4, 2, 3): 100, (4, 2, 4): 45, (4, 2, 5): 45,
               (4, 2, 6): 76, (4, 2, 7): 76, (4, 3, 0): 84, (4, 3, 1): 14, (4, 3, 2): 91, (4, 3, 3): 4, (4, 3, 4): 95,
               (4, 3, 5): 95, (4, 3, 6): 76, (4, 3, 7): 76, (4, 4, 0): 84, (4, 4, 1): 12, (4, 4, 2): 12, (4, 4, 3): 4,
               (4, 4, 4): 95, (4, 4, 5): 59, (4, 4, 6): 59, (4, 4, 7): 50, (4, 5, 0): 77, (4, 5, 1): 77, (4, 5, 2): 77,
               (4, 5, 3): 44, (4, 5, 4): 59, (4, 5, 5): 50, (4, 5, 6): 50, (4, 5, 7): 50, (4, 6, 0): 77, (4, 6, 1): 77,
               (4, 6, 2): 77, (4, 6, 3): 44, (4, 6, 4): 50, (4, 6, 5): 50, (4, 6, 6): 50, (4, 6, 7): 50, (4, 7, 0): 77,
               (4, 7, 1): 77, (4, 7, 2): 77, (4, 7, 3): 74, (4, 7, 4): 63, (4, 7, 5): 50, (4, 7, 6): 50, (4, 7, 7): 50,
               (5, 0, 0): 73, (5, 0, 1): 53, (5, 0, 2): 53, (5, 0, 3): 45, (5, 0, 4): 45, (5, 0, 5): 45, (5, 0, 6): 45,
               (5, 0, 7): 45, (5, 1, 0): 53, (5, 1, 1): 53, (5, 1, 2): 33, (5, 1, 3): 45, (5, 1, 4): 45, (5, 1, 5): 45,
               (5, 1, 6): 45, (5, 1, 7): 76, (5, 2, 0): 83, (5, 2, 1): 83, (5, 2, 2): 33, (5, 2, 3): 100, (5, 2, 4): 45,
               (5, 2, 5): 76, (5, 2, 6): 76, (5, 2, 7): 76, (5, 3, 0): 84, (5, 3, 1): 91, (5, 3, 2): 91, (5, 3, 3): 44,
               (5, 3, 4): 76, (5, 3, 5): 76, (5, 3, 6): 76, (5, 3, 7): 76, (5, 4, 0): 84, (5, 4, 1): 84, (5, 4, 2): 44,
               (5, 4, 3): 44, (5, 4, 4): 87, (5, 4, 5): 16, (5, 4, 6): 16, (5, 4, 7): 50, (5, 5, 0): 77, (5, 5, 1): 77,
               (5, 5, 2): 44, (5, 5, 3): 44, (5, 5, 4): 87, (5, 5, 5): 16, (5, 5, 6): 50, (5, 5, 7): 50, (5, 6, 0): 77,
               (5, 6, 1): 77, (5, 6, 2): 24, (5, 6, 3): 74, (5, 6, 4): 63, (5, 6, 5): 50, (5, 6, 6): 50, (5, 6, 7): 80,
               (5, 7, 0): 77, (5, 7, 1): 77, (5, 7, 2): 74, (5, 7, 3): 74, (5, 7, 4): 63, (5, 7, 5): 50, (5, 7, 6): 80,
               (5, 7, 7): 80, (6, 0, 0): 53, (6, 0, 1): 53, (6, 0, 2): 53, (6, 0, 3): 45, (6, 0, 4): 45, (6, 0, 5): 45,
               (6, 0, 6): 45, (6, 0, 7): 45, (6, 1, 0): 53, (6, 1, 1): 53, (6, 1, 2): 53, (6, 1, 3): 45, (6, 1, 4): 45,
               (6, 1, 5): 45, (6, 1, 6): 76, (6, 1, 7): 76, (6, 2, 0): 34, (6, 2, 1): 34, (6, 2, 2): 91, (6, 2, 3): 11,
               (6, 2, 4): 76, (6, 2, 5): 76, (6, 2, 6): 76, (6, 2, 7): 76, (6, 3, 0): 34, (6, 3, 1): 84, (6, 3, 2): 91,
               (6, 3, 3): 11, (6, 3, 4): 11, (6, 3, 5): 11, (6, 3, 6): 76, (6, 3, 7): 76, (6, 4, 0): 38, (6, 4, 1): 24,
               (6, 4, 2): 24, (6, 4, 3): 44, (6, 4, 4): 87, (6, 4, 5): 48, (6, 4, 6): 48, (6, 4, 7): 48, (6, 5, 0): 38,
               (6, 5, 1): 24, (6, 5, 2): 24, (6, 5, 3): 93, (6, 5, 4): 93, (6, 5, 5): 16, (6, 5, 6): 31, (6, 5, 7): 80,
               (6, 6, 0): 38, (6, 6, 1): 24, (6, 6, 2): 24, (6, 6, 3): 74, (6, 6, 4): 74, (6, 6, 5): 63, (6, 6, 6): 31,
               (6, 6, 7): 80, (6, 7, 0): 38, (6, 7, 1): 38, (6, 7, 2): 24, (6, 7, 3): 74, (6, 7, 4): 63, (6, 7, 5): 31,
               (6, 7, 6): 80, (6, 7, 7): 80, (7, 0, 0): 53, (7, 0, 1): 53, (7, 0, 2): 53, (7, 0, 3): 45, (7, 0, 4): 45,
               (7, 0, 5): 45, (7, 0, 6): 45, (7, 0, 7): 76, (7, 1, 0): 34, (7, 1, 1): 34, (7, 1, 2): 53, (7, 1, 3): 45,
               (7, 1, 4): 76, (7, 1, 5): 76, (7, 1, 6): 76, (7, 1, 7): 76, (7, 2, 0): 34, (7, 2, 1): 34, (7, 2, 2): 34,
               (7, 2, 3): 11, (7, 2, 4): 11, (7, 2, 5): 76, (7, 2, 6): 76, (7, 2, 7): 76, (7, 3, 0): 34, (7, 3, 1): 34,
               (7, 3, 2): 24, (7, 3, 3): 11, (7, 3, 4): 11, (7, 3, 5): 11, (7, 3, 6): 48, (7, 3, 7): 48, (7, 4, 0): 38,
               (7, 4, 1): 38, (7, 4, 2): 24, (7, 4, 3): 11, (7, 4, 4): 11, (7, 4, 5): 48, (7, 4, 6): 48, (7, 4, 7): 48,
               (7, 5, 0): 38, (7, 5, 1): 38, (7, 5, 2): 24, (7, 5, 3): 24, (7, 5, 4): 93, (7, 5, 5): 48, (7, 5, 6): 31,
               (7, 5, 7): 80, (7, 6, 0): 38, (7, 6, 1): 38, (7, 6, 2): 24, (7, 6, 3): 74, (7, 6, 4): 74, (7, 6, 5): 31,
               (7, 6, 6): 31, (7, 6, 7): 80, (7, 7, 0): 38, (7, 7, 1): 38, (7, 7, 2): 24, (7, 7, 3): 74, (7, 7, 4): 63,
               (7, 7, 5): 31, (7, 7, 6): 80, (7, 7, 7): 80}
        blocks = ["cyan_glazed_terracotta", "blue_terracotta", "gray_wool", "black_glazed_terracotta",
                  "light_gray_wool", "chiseled_nether_bricks", "diamond_ore", "black_terracotta", "gray_terracotta",
                  "cyan_terracotta", "cobblestone", "pink_wool", "orange_glazed_terracotta", "stone_bricks",
                  "oak_planks", "deepslate_diamond_ore", "mushroom_stem", "blue_glazed_terracotta",
                  "deepslate_redstone_ore", "cracked_deepslate_bricks", "deepslate_copper_ore", "nether_quartz_ore",
                  "crimson_stem", "light_blue_terracotta", "yellow_glazed_terracotta", "cracked_nether_bricks",
                  "jungle_planks", "polished_blackstone_bricks", "brown_glazed_terracotta", "crimson_planks",
                  "lime_wool", "quartz_bricks", "coal_ore", "pink_terracotta", "orange_wool", "prismarine_bricks",
                  "orange_terracotta", "deepslate_emerald_ore", "yellow_wool", "mangrove_planks", "red_terracotta",
                  "purple_wool", "chiseled_stone_bricks", "cracked_polished_blackstone_bricks", "birch_planks",
                  "magenta_wool", "blue_wool", "dark_oak_planks", "pink_glazed_terracotta", "lime_terracotta",
                  "white_glazed_terracotta", "green_glazed_terracotta", "lapis_ore", "red_glazed_terracotta",
                  "stripped_crimson_stem", "black_wool", "brown_terracotta", "copper_ore", "deepslate_bricks",
                  "light_gray_glazed_terracotta", "purple_glazed_terracotta", "gray_glazed_terracotta",
                  "deepslate_iron_ore", "end_stone_bricks", "light_blue_wool", "warped_stem[axis=x]",
                  "purple_terracotta", "cyan_wool", "light_blue_glazed_terracotta", "light_gray_terracotta",
                  "redstone_ore", "spruce_planks", "stripped_warped_stem", "red_wool", "end_stone", "brown_wool",
                  "magenta_glazed_terracotta", "lime_glazed_terracotta", "deepslate_gold_ore", "green_terracotta",
                  "white_wool", "deepslate_lapis_ore", "iron_ore", "acacia_planks", "yellow_terracotta",
                  "warped_planks", "nether_gold_ore", "white_terracotta", "deepslate_coal_ore", "melon_stem",
                  "cracked_stone_bricks", "glowstone", "blackstone", "sandstone", "gold_ore", "smooth_stone",
                  "emerald_ore", "red_nether_bricks", "mossy_stone_bricks", "green_wool", "magenta_terracotta", "none"]
        progress_bar = Progress(self.num - 1)
        progress_bar.show()
        progress_bar.start_func(multiple, self.num, self.output_path, self.func_path,
                self.json_path, self.video_size, self.name_space, self.display_delay, blocks, res)


class Progress(QWidget):
    def __init__(self, maxum):
        super(Progress, self).__init__()
        self.resize(600, 200)
        self.progressbar = QProgressBar(self)
        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(maxum)

        self.step = 0

        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.v_layout.addWidget(self.progressbar)
        self.v_layout.addLayout(self.h_layout)

        self.setLayout(self.v_layout)

        self.process_thread = ProcessThread()
        self.process_thread.process_signal.connect(self.update_func)

    def start_func(self, mul, num, out, func, json, size, space, delay, blocks, res):
        self.process_thread.function_generation(mul,
            num, out, func, json, size, space, delay, blocks, res)

    def update_func(self, k):
        self.progressbar.setValue(k)
        app.processEvents()


class ProcessThread(QThread):
    process_signal = pyqtSignal(int)

    def __init__(self):
        super(ProcessThread, self).__init__()
        self.progress = 0

    def function_generation(self, multiple, num, output_path,
            func_path, json_path, video_size, name_space, delay, blocks, res):
        last_image = [[[256, 256, 256]] * video_size[0] for _ in range(video_size[1])]
        for k in range(1, num):
            self.process_signal.emit(k)
            print(k)
            im = Image.open(output_path + "%08d.jpg" % k)
            im_resized = im.resize(video_size)
            func = open(func_path + "%08d.mcfunction" % k, 'w')
            json_file = open(json_path + "%08d.json" % k, 'w')
            image = array(im_resized)
            rows = video_size[1]
            cols = video_size[0]
            for i in range(rows):
                for j in range(cols):
                    temp = image[i][j]
                    last_temp = last_image[i][j]
                    block = (temp[0] >> multiple, temp[1] >> multiple, temp[2] >> multiple)
                    last_block = (last_temp[0] >> multiple, last_temp[1] >> multiple, last_temp[2] >> multiple)
                    if blocks[res[block]] != blocks[res[last_block]]:
                        func.write("setblock %d 10 %d %s\n" % (-i - 1, j, blocks[res[block]]))
            json_file.write(content % (name_space, k))
            func.close()
            json_file.close()
            last_image = image

            func = open(func_path + "start.mcfunction", 'w')
            json_file = open(json_path + "start.json", 'w')
            start = 3
        for i in range(num):
            func.write("schedule function {2:s}:{0:08d} {1:f}s\n".format(i, start + i * delay, name_space))

        json_file.write(content2 % name_space)
        func.close()
        json_file.close()


def make_dirs(name, name_space):
    output_path = "./temp/%s/" % name
    func_path = "./datapacks/output/data/%s/functions/" % name_space
    json_path = "./datapacks/output/data/minecraft/tags/functions/"
    try:
        for eachPath in [output_path, func_path, json_path]:
            if path.exists(eachPath):
                rmtree(eachPath)
            makedirs(eachPath)
    except:
        print("Invalid file name")
    return output_path, func_path, json_path


def video_process(output_path, video_path, interval):
    times = num = 1
    vid = VideoCapture(video_path)
    while vid.isOpened():
        is_read, frame = vid.read()
        if times % interval == 0:
            if is_read:
                file_name = '%08d' % num
                imwrite(output_path + file_name + '.jpg', frame)
                waitKey(1)
                num += 1
            else:
                break
        times += 1
    return num


meta = \
    """{
    "pack": {
        "pack_format": 11,
        "description": "Just for building."
    }
}
"""

content = \
    """{
    "values":[
        "%s:%08d"
    ]
}
"""

content2 = \
    """{
        "values":[
            "%s:start"
        ]
    }
    """

if __name__ == "__main__":
    app = QApplication(argv)
    main = Getconf()
    main.show()
    exit(app.exec())
