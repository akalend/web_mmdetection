# -*- coding: utf-8 -*-
import daemon
import json
import mmcv
import mmdet
import os
import sys
import time
import torch, torchvision
# import numpy as np
from mmcv.ops import get_compiling_cuda_version, get_compiler_version
from mmdet.apis import inference_detector, init_detector
from PIL import Image

# Choose to use a config and initialize the detector

def detection(num, score_thr):

    config = 'configs/mask_rcnn/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco.py'
    # Setup a checkpoint file to load
    checkpoint = 'checkpoints/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco_bbox_mAP-0.408__segm_mAP-0.37_20200504_163245-42aa3d00.pth'
    # initialize the detector
    model = init_detector(config, checkpoint, device='cpu')

    # Use the detector to do inference
    img = f'/tmp/upload/{num}.png'
    img_out = f'/tmp/upload/{num}.out.png'
    data_out = f'/tmp/upload/{num}.out.json'

    ts = time.time()
    result = inference_detector(model, img)
    # score_thr = 0.85

    classes = model.CLASSES

    out = []
    num = 0
    for it in result[0]:
      if len(it):
        for itt in it:
            if itt[4] > score_thr:
                prb = float(itt[4])
                tmp = [ int(xx) for  xx in itt.tolist() ]
                tmp[4] = prb
                out.append({classes[num] : tmp})
      num +=1

    with open(data_out, 'w') as fp:
        json.dump(out, fp)

    img = model.show_result(img, result, score_thr=score_thr, thickness=0, show=False, out_file=img_out, text_color='red', font_scale=1)

    common_time = time.time() - ts  
    print( 'processing time:' ,int(common_time) )



if len(sys.argv) < 2:
    print('fail parameters')
    exit(0)


filename = '/tmp/upload/{}.png'.format(sys.argv[1])
if not os.path.isfile(filename):
    print( 'filename {} do not exist'.format(filename) )
    exit(0)

os.chdir('/root/mmdetection')
logfile = '/var/log/detection.log'

if len(sys.argv) == 3:
    print( 'start id=' , sys.argv[1])
    detection(sys.argv[1], float(sys.argv[2]))
else:
    print( 'start id=' , sys.argv[1], 'prd=', sys.argv[2])
    detection(sys.argv[1], 0.5)

