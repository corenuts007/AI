

import argparse
import time
from pathlib import Path
import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random

from spyproj.yolov7.models.experimental import attempt_load
from spyproj.yolov7.utils.datasets import LoadStreams, LoadImages
from spyproj.yolov7.utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from spyproj.yolov7.utils.plots import plot_one_box
from spyproj.yolov7.utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Detective:
    def detect(self):
        source, weights, view_img, save_txt, imgsz, trace = self.opt.source, self.opt.weights, self.opt.view_img, self.opt.save_txt, self.opt.img_size, not self.opt.no_trace
        save_img = not self.opt.nosave and not source.endswith(
            '.txt')  # save inference images
        webcam = source.isnumeric() or source.endswith('.txt') or source.lower().startswith(
            ('rtsp://', 'rtmp://', 'http://', 'https://'))
        previousTime=currentTime = datetime.now()
        # Directories
        save_dir = Path(increment_path(Path(self.opt.project) / self.opt.name,
                        exist_ok=self.opt.exist_ok))  # increment run
        (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True,
                                                            exist_ok=True)  # make dir
        # Initialize
        set_logging()
        device = select_device(self.opt.device)
        half = device.type != 'cpu'  # half precision only supported on CUDA

        # Load model
        model = attempt_load(weights, map_location=device)  # load FP32 model
        stride = int(model.stride.max())  # model stride
        imgsz = check_img_size(imgsz, s=stride)  # check img_size

        if trace:
            model = TracedModel(model, device, self.opt.img_size)

        if half:
            model.half()  # to FP16

        # Second-stage classifier
        classify = False
        if classify:
            modelc = load_classifier(name='resnet101', n=2)  # initialize
            modelc.load_state_dict(torch.load(
                'weights/resnet101.pt', map_location=device)['model']).to(device).eval()

        # Set Dataloader
        vid_path, vid_writer = None, None
        if webcam:
            view_img = check_imshow()
            cudnn.benchmark = True  # set True to speed up constant image size inference
            dataset = LoadStreams(source, img_size=imgsz, stride=stride)
        else:
            dataset = LoadImages(source, img_size=imgsz, stride=stride)

        #print("11111111111111111111111")

        # Get names and colors
        names = model.module.names if hasattr(model, 'module') else model.names
        colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

        # Run inference
        if device.type != 'cpu':
            model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(
                next(model.parameters())))  # run once
        old_img_w = old_img_h = imgsz
        old_img_b = 1

        t0 = time.time()
        for path, img, im0s, vid_cap in dataset:
            img = torch.from_numpy(img).to(device)
            img = img.half() if half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Warmup
            if device.type != 'cpu' and (old_img_b != img.shape[0] or old_img_h != img.shape[2] or old_img_w != img.shape[3]):
                old_img_b = img.shape[0]
                old_img_h = img.shape[2]
                old_img_w = img.shape[3]
                for i in range(3):
                    model(img, augment=self.opt.augment)[0]

            # Inference
            t1 = time_synchronized()
            pred = model(img, augment=self.opt.augment)[0]
            t2 = time_synchronized()

            # Apply NMS
            pred = non_max_suppression(
                pred, self.opt.conf_thres, self.opt.iou_thres, classes=self.opt.classes, agnostic=self.opt.agnostic_nms)
            t3 = time_synchronized()

            # Apply Classifier
            if classify:
                pred = apply_classifier(pred, modelc, img, im0s)

            #print("222222222222222222222")
            ##print(f"Results saved to {len(pred)}{s}")

            # Process detections
            for i, det in enumerate(pred):  # detections per image
                if webcam:  # batch_size >= 1
                    p, s, im0, frame = path[i], '%g: ' % i, im0s[i].copy(
                    ), dataset.count
                else:
                    p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

                #print(f"333333333333333333")
                #print(f"Results saved to {len(det)}")
                #print(f"44444444")
                p = Path(p)  # to Path
                #previousTime=currentTime = now
                currentTime = datetime.now()
                
                diff = relativedelta(currentTime, previousTime)
                #first time
                print("current_time===============================>",currentTime)
                print("previousTime===============================>",previousTime)
                print("diff===============================>",diff.minutes)
                #print("timeeeeeeeeeeeeeeeeeeeeeeeeeeee", diff.minutes)
                if(diff.minutes>1):
                    imgName1=currentTime.strftime("%H_%M")+p.name
                    previousTime= currentTime
                else:
                    imgName1=previousTime.strftime("%H_%M")+p.name
                
                print("imgName1===============================>",imgName1)
                save_path = str(save_dir /imgName1)  # img.jpg
                txt_path = str(save_dir / 'labels' / p.stem) + \
                    ('' if dataset.mode == 'image' else f'_{frame}')  # img.txt
                # normalization gain whwhpreviousTime
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]
                personDetected =False
                if len(det):
                    for c in det[:, -1].unique():
                        if(names[int(c)]=='person'):
                            personDetected=True
                            #print("person detected")
                if (personDetected):
                        # Rescale boxes from img_size to im0 size
                        det[:, :4] = scale_coords(
                            img.shape[2:], det[:, :4], im0.shape).round()
                        #print("save====>",save_path)
                        # #print results
                        for c in det[:, -1].unique():
                            #print("person detected")
                            n = (det[:, -1] == c).sum()  # detections per class
                            # add to string
                            s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "

                        # Write results
                        for *xyxy, conf, cls in reversed(det):
                            if save_txt:  # Write to file
                                xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)
                                                ) / gn).view(-1).tolist()  # normalized xywh
                                # label format
                                line = (
                                    cls, *xywh, conf) if self.opt.save_conf else (cls, *xywh)
                                with open(txt_path + '.txt', 'a') as f:
                                    f.write(('%g ' * len(line)).rstrip() % line + '\n')

                            if save_img or view_img:  # Add bbox to image
                                now = datetime.now()
                                current_time = now.strftime("%H:%M:%S")    
                                label = f'{names[int(cls)]} {current_time}'
                                plot_one_box(xyxy, im0, label=label,
                                            color=colors[int(cls)], line_thickness=4)

                    # #print time (inference + NMS)
                        #print(f'{s}Done. ({(1E3 * (t2 - t1)):.1f}ms) Inference, ({(1E3 * (t3 - t2)):.1f}ms) NMS')

                    # Stream results
                        if view_img:
                            cv2.imshow(str(p), im0)
                            cv2.waitKey(1)  # 1 millisecond

                    # Save results (image with detections)
                        if save_img:
                            if dataset.mode == 'image':
                                cv2.imwrite(save_path, im0)
                                #print(f" The image with the result is saved in: {save_path}")
                            else:  # 'video' or 'stream'
                                if vid_path != save_path:  # new video
                                    vid_path = save_path
                                    if isinstance(vid_writer, cv2.VideoWriter):
                                        vid_writer.release()  # release previous video writer
                                    if vid_cap:  # video
                                        fps = vid_cap.get(cv2.CAP_PROP_FPS)
                                        w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                                        h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                                    else:  # stream
                                        fps, w, h = 30, im0.shape[1], im0.shape[0]
                                        save_path += '.avi'
                                    vid_writer = cv2.VideoWriter(
                                        save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                                vid_writer.write(im0)
                                

        if save_txt or save_img:
            s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
            ##print(f"Results saved to {save_dir}{s}")

        #print(f'Done. ({time.time() - t0:.3f}s)')


    def __init__(self):
        print('detect obj')
        parser = argparse.ArgumentParser()
        parser.add_argument('--weights', nargs='+', type=str, default='yolov7.pt', help='model.pt path(s)')
        parser.add_argument('--source', type=str, default='0', help='source')  # file/folder, 0 for webcam
        parser.add_argument('--img-size', type=int, default=640, help='inference size (pixels)')
        parser.add_argument('--conf-thres', type=float, default=0.25, help='object confidence threshold')
        parser.add_argument('--iou-thres', type=float, default=0.45, help='IOU threshold for NMS')
        parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
        parser.add_argument('--view-img', action='store_true', help='display results')
        parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
        parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
        parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
        parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
        parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
        parser.add_argument('--augment', action='store_true', help='augmented inference')
        parser.add_argument('--update', action='store_true', help='update all models')
        parser.add_argument('--project', default='runs/detect', help='save results to project/name')
        parser.add_argument('--name', default='exp', help='save results to project/name')
        parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
        parser.add_argument('--no-trace', action='store_true', help='don`t trace model')
        self.opt = parser.parse_args()
        print('self.opt', self.opt)
        #check_requirements(exclude=('pycocotools', 'thop'))

        # with torch.no_grad():
        #     if self.opt.update:  # update all models (to fix SourceChangeWarning)
        #         for self.opt.weights in ['yolov7.pt']:
        #             detect()
        #             strip_self.optimizer(self.opt.weights)
        #     else:
        #         detect()

    def detect_object_method(self):
        print('detect_object_method')
        #for self.self.opt.weights in ['yolov7.pt']:
        self.opt.weights = 'spyproj\yolov7\yolov7.pt'
        self.opt.img_size = 640
        #self.opt.source = '0'
        self.opt.conf = 0.25
        self.opt.save_img = False
        self.detect()
        strip_optimizer(self.opt.weights)
