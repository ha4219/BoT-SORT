import cv2


data = []
with open('test1.txt', 'r') as f:
    while True:
        line = f.readline()
        if not line: break
        data.append(line)

res = []
for dat in data:
    frame = []
    for xy in dat.strip().split(','):
        try:
            x, y = map(float, xy.split())
            frame.append((x, y))
        except:
            continue
    res.append(frame)

import numpy as np

h_matrix = np.load('h_r_1217.npy')
cap = cv2.VideoCapture('IMG_0414~2.mp4')
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)

vid_writer = cv2.VideoWriter(
    'test111.mp4',
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (int(width), int(height))
)

# 영상 sync를 맞추기 위해 -10부터 시작합니다.
idx = -10
while True:
    ret_val, frame = cap.read()
    if ret_val:
        if idx < 0: continue
        try:
            for (x, y) in res[idx]:
                if x < 0.0 or y < 0.0 or x > 1.0 or y > 1.0: continue
                bbox = cv2.perspectiveTransform(np.array([[[x, y]]]), h_matrix).reshape(2)
                
                cv2.circle(frame, (int(bbox[0]), int(bbox[1])), radius=15, color=(255,0,0), thickness=-1)
        except:
            print('except', idx)
    else:
        break
    idx += 1
    vid_writer.write(frame)