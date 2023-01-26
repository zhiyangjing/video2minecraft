import cv2
import numpy
import os
from PIL import Image
import pickle
import sys
import shutil
"""
输出:在当前目录生成1.19版本中/saves/world/datapacks文件夹下的所有项目
    生成位置在当前目录的packages文件夹中
    
文件配置:
1.配置下方的video_path和video_name,其余会自动生成
2.配置interval,interval=2时大致一秒十帧
3.配置命名空间,(随便起)

命名规则:mcfunction从1开始按顺序命名.格式eg: 00000001.mcfunction
"""

video_path = "./videos/"    # 默认地址 (Default video directory)
video_name = "testmc203.mp4"  # 默认文件名 (Default video name)
name_space = "mine"        # 默认的命名空间 (Default name space)
video_size = [352,198]      # 默认的输出尺寸,可以保持不变 (Default image size)
interval = 1                # 读取mp4文件时帧数间隔，默认为2 (When reading MP4 files, the frame interval is 2 by default)
delay = 1                 # 连续运行mcfunction的间隔(秒) (The interval at which mcfunction runs continuously(seconds))


# 创建文件夹
print("Creating the directory.")

name = video_name.split(".")[0]
if os.path.exists("./temp/%s" %name):
    shutil.rmtree("./temp/%s" %name)
os.makedirs("./temp/%s" %name)
output_path = "./temp/%s/" %name  # 图片暂存文件夹


# video --> png
print("Parsing the video...")

times = num = 1
vid = cv2.VideoCapture(video_path+video_name)
while vid.isOpened():
    is_read, frame = vid.read()
    if times % interval == 0:
        if is_read:
            file_name = '%08d' % num
            cv2.imwrite(output_path + file_name + '.jpg', frame)
            cv2.waitKey(1)
            num += 1
        else:
            break
    times += 1

print("Parsing complete.")
print("Generating the function files.")
print("\r",end="")

# 生成mcfunction
with open("./data","rb") as data:
    res,blocks = pickle.load(data)

if os.path.exists("./datapacks/output/data/%s/functions/" %name_space):
    shutil.rmtree("./datapacks/output/data/%s/functions/" %name_space)
os.makedirs("./datapacks/output/data/%s/functions/" %name_space)
func_path = "./datapacks/output/data/%s/functions/" %name_space

meta = \
"""{
    "pack": {
        "pack_format": 11,
        "description": "Just for building."
    }
}
"""

doc = open("./datapacks/output/pack.mcmeta",'w')
doc.write(meta)
doc.close

if os.path.exists("./datapacks/output/data/minecraft/tags/functions/"):
    shutil.rmtree("./datapacks/output/data/minecraft/tags/functions/")
os.makedirs("./datapacks/output/data/minecraft/tags/functions/")
json_path = "./datapacks/output/data/minecraft/tags/functions/"


# shrink the size
last_image = [[[256,256,256]] * video_size[0] for _ in range(video_size[1])]
for k in range(1,num):
    print("\r", end="")
    print("Processing:{: 3d}%:[".format((k*100)//num),"#" * (k*50//num) \
          +"_" * (50-(k*50//num)),"]", end="")
    sys.stdout.flush()
    im = Image.open(output_path+"%08d.jpg" %k)
    im_resized = im.resize(video_size)
    func = open(func_path+"%08d.mcfunction" %k,'w')
    funcjson = open(json_path+"%08d.json" %k,'w')
    image = numpy.array(im_resized)
    rows = video_size[1]
    cols = video_size[0]
    for i in range(rows):
        for j in range(cols):
            temp = image[i][j]
            last_temp = last_image[i][j]
            block = (temp[0]>>5,temp[1]>>5,temp[2]>>5)
            last_block = (last_temp[0]>>5,last_temp[1]>>5,last_temp[2]>>5)
            if blocks[res[block]] != blocks[res[last_block]]:
                func.write("setblock %d 10 %d %s\n" %(-i-1,j,blocks[res[block]]))
    content = \
"""{
    "values":[
        "%s:%08d"
    ]
}
"""
    funcjson.write(content %(name_space,k))
    func.close()
    funcjson.close()
    last_image = image

func = open(func_path + "start.mcfunction", 'w')
funcjson = open(json_path + "start.json", 'w')
start = 3
for i in range(num):
    func.write("schedule function {2:s}:{0:08d} {1:f}s\n".format(i,start+i*delay,name_space))
content2 = \
"""{
    "values":[
        "%s:start"
    ]
}
"""
funcjson.write(content2 %name_space)
func.close()
funcjson.close()

print("\r", end="")
print("Processing:{}%:[".format(100), "#" * 50,"]")
print("{} function files have been created.".format(num))
