# 视频转mc像素画
## 用途
本程序可以根据视频生成对应的像素画。

通过截取视频中部分单帧画面，然后对该画面进行
处理得到`.mcfunction`文件以及相关的配置文件.

## 使用方法
打开`main.py`完成相应配置(或者不配置,只进行小部分调整)
然后运行即可.
> 注意:要安装对应的第三方库
> 包括:numpy pillow cv-python

运行结束后可直接将获得的`datapacks`文件夹复制到`world`文件夹下
直接替换原有`datapacks`

# Convert video to mc pixel art
## Purpose
This program can generate corresponding pixel art according to the video.

After intercepting single frames in the video, we can then 
change them into `.mcfunction` file and related configuration files.

## Instructions
Edit `main.py` to complete the corresponding configuration. 
(or just use the default settings)

Run the program after that.
> Note: You need to install the corresponding third-party library
> Including: numpy pillow cv-python

After the program finished, you can directly copy the
obtained `datapacks` folder to the `world` folder
to replace the original `datapacks`