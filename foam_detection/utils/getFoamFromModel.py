import sys
sys.path.append("./foam_detection/detectron2-main/")
sys.path.append("./detectron2-main/")

import os
import pickle
from detectron2.engine import DefaultPredictor
from detectron2.utils.visualizer import Visualizer
from detectron2.utils.visualizer import ColorMode
import cv2

def getFoamFromModel(image):
    cfg_save_path = "foam_mask_rcnn/IS_cfg.pickle"
    with open(cfg_save_path, 'rb') as f:
        cfg = pickle.load(f)

    cfg.MODEL.WEIGHTS = os.path.join("foam_mask_rcnn/" + cfg.OUTPUT_DIR, "model_final.pth")
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.4
    predictor = DefaultPredictor(cfg)

    outputs = predictor(image)
    output_instance = outputs["instances"].to("cpu")

    v = Visualizer(image[:,:,::-1], metadata={}, scale =1, instance_mode=ColorMode.SEGMENTATION)
    v = v.draw_instance_predictions(output_instance)

    detected_classes = output_instance.pred_classes.numpy().tolist()
    # print(detected_classes)
    bbox = None
    if detected_classes != []:
        try:
            foam_idx = detected_classes.index(1)
        except ValueError: # if there is no foam
            return None, cv2.cvtColor(v.get_image(), cv2.COLOR_RGB2BGR)
        else:
            detected_bboxs = output_instance.pred_boxes.tensor.numpy().tolist()
            bbox = detected_bboxs[foam_idx]

    # mask = output_instance.pred_masks.numpy()
    # print( mask.shape)
    return bbox, cv2.cvtColor(v.get_image(), cv2.COLOR_RGB2BGR)