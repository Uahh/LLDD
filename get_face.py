import os
import cv2
import time


def getAllPath(dirpath, *args):
    PathArray = []
    for r, ds, fs in os.walk(dirpath):
        for fn in fs:
            if os.path.splitext(fn)[1] in args:
                fname = os.path.join(r, fn)
                PathArray.append(fname)
    return PathArray


def cut_face(sourcePath, targetPath, *args):
    ImagePaths = getAllPath(sourcePath, *args)

    count = 1
    # haarcascade_frontalface_alt.xml为库训练好的分类器文件，下载opencv，安装目录中可找到
    face_cascade = cv2.CascadeClassifier('C:\\Python310\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_alt.xml')
    for imagePath in ImagePaths:
        img = cv2.imread(imagePath)

        if type(img) != str:
            faces = face_cascade.detectMultiScale(img, 1.1, 3)
            if len(faces):
                for (x, y, w, h) in faces:
                    # 设置人脸宽度大于16像素，去除较小的人脸
                    if w >= 16 and h >= 16:
                        # 以时间戳和读取的排序作为文件名称
                        listStr = [str(count)]
                        fileName = ''.join(listStr)
                        # 扩大图片，可根据坐标调整
                        X = int(x)
                        W = min(int(x + w), img.shape[1])
                        Y = int(y)
                        H = min(int(y + h), img.shape[0])

                        f = cv2.resize(img[Y:H, X:W], (W - X, H - Y))
                        cv2.imwrite(targetPath + os.sep + '%s.jpg' % fileName, f)
                        count += 1

if __name__ == '__main__':
    sourcePath = r'D:\\Project\\LLDD\\picture\\nanjolno'
    targetPath1 = r'D:\\Project\\LLDD\\picture\\nanjolno_cut'
    cut_face(sourcePath, targetPath1, '.jpg', '.JPG', 'png', 'PNG')
