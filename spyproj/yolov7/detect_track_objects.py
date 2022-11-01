import argparse
import time
from pathlib import Path
import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, \
                check_imshow, non_max_suppression, apply_classifier, \
                scale_coords, xyxy2xywh, strip_optimizer, set_logging, \
                increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel
from datetime import datetime
from dateutil.relativedelta import relativedelta
from spyproj.yolov7.sort import *
from dateutil.relativedelta import relativedelta
from spyproj.repository.alertdetails_repository import AlertDetails
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os.path
from spyproj.utils.googleDriveUpload import googleDriveUpload

class DetectiveAndTrack():
    """Function to Draw Bounding boxes"""
    def draw_boxes(self,img, bbox, identities=None, categories=None, confidences = None, names=None, colors = None):
        for i, box in enumerate(bbox):
            x1, y1, x2, y2 = [int(i) for i in box]
            tl = self.opt.thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
            cat = int(categories[i]) if categories is not None else 0
            id = int(identities[i]) if identities is not None else 0
            # conf = confidences[i] if confidences is not None else 0

            color = colors[cat]
            
            if not self.opt.nobbox:
                cv2.rectangle(img, (x1, y1), (x2, y2), color, tl)

            if not self.opt.nolabel:
                label = str(id) + ":"+ names[cat] if identities is not None else  f'{names[cat]} {confidences[i]:.2f}'
                tf = max(tl - 1, 1)  # font thickness
                t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
                c2 = x1 + t_size[0], y1 - t_size[1] - 3
                cv2.rectangle(img, (x1, y1), c2, color, -1, cv2.LINE_AA)  # filled
                cv2.putText(img, label, (x1, y1 - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)


        return img


    def detect(self):
        source, weights, view_img, save_txt, imgsz, trace = self.opt.source, self.opt.weights, self.opt.view_img, self.opt.save_txt, self.opt.img_size, not self.opt.no_trace
        save_img = not self.opt.nosave and not source.endswith('.txt')  # save inference images
        webcam = source.isnumeric() or source.endswith('.txt') or source.lower().startswith(
            ('rtsp://', 'rtmp://', 'http://', 'https://'))
            
        process_endtime = self.process_endtime
        
        print("*********************DetectiveAndTrack*********************************")
        print('process_endtime:', process_endtime)
        previousTime=currentTime = datetime.now()
        uploadVideo =False

        save_dir = Path(increment_path(Path(self.opt.project) / self.opt.name, exist_ok=self.opt.exist_ok))  # increment run
        if not self.opt.nosave:  
            (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

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
            modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model']).to(device).eval()

        # Set Dataloader
        vid_path, vid_writer = None, None
        if webcam:
            view_img = check_imshow()
            cudnn.benchmark = True  # set True to speed up constant image size inference
            dataset = LoadStreams(source, img_size=imgsz, stride=stride)
        else:
            dataset = LoadImages(source, img_size=imgsz, stride=stride)

        # Get names and colors
        names = model.module.names if hasattr(model, 'module') else model.names
        colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

        # Run inference
        if device.type != 'cpu':
            model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
        old_img_w = old_img_h = imgsz
        old_img_b = 1

        t0 = time.time()
        ###################################
        startTime = 0
        ###################################
        countValue = 0
        for path, img, im0s, vid_cap in dataset:
            countValue = countValue + 1
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
            pred = non_max_suppression(pred, self.opt.conf_thres, self.opt.iou_thres, classes=self.opt.classes, agnostic=self.opt.agnostic_nms)
            t3 = time_synchronized()

            # Apply Classifier
            if classify:
                pred = apply_classifier(pred, modelc, img, im0s)

            # Process detections
            for i, det in enumerate(pred):  # detections per image
                if webcam:  # batch_size >= 1
                    p, s, im0, frame = path[i], '%g: ' % i, im0s[i].copy(), dataset.count
                else:
                    p, s, im0, frame = path, '', im0s, getattr(dataset, 'frame', 0)

                p = Path(p)  # to Path
                #previousTime=currentTime = now
                currentTime = datetime.now()
                
                diff = relativedelta(currentTime, previousTime)
                #first time
                print("current_time===============================>",currentTime)
                print("previousTime===============================>",previousTime)
                print("diff===============================>",diff.minutes)
                #print("timeeeeeeeeeeeeeeeeeeeeeeeeeeee", diff.minutes)
                #first time
                isReadyToUpload = False
                previousVideoPath= 'abc'
                img3=''

                if(diff.minutes>10):
                    imgName1=currentTime.strftime("%H_%M")+p.name
                    isReadyToUpload=True
                    img3=previousTime.strftime("%H_%M")+p.name+'.webm'
                    #print('1',img3)
                    previousVideoPath=str(save_dir / img3)
                    #print('2',previousVideoPath)
                    previousTime= currentTime
                    #previousVideoPath+='.webm'
                    #print('3',previousVideoPath)
                else:
                    imgName1=previousTime.strftime("%H_%M")+p.name
                    isReadyToUpload = False
                
                print("imgName1===============================>",imgName1)
                save_path = str(save_dir /imgName1)  # img.jpg

                txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # img.txt
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                personDetected =False
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                    # Print results
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string
                        if(names[int(c)]=='person'):
                            personDetected=True
                            self.insertAlertDetailsIntoDB(self.group_name,self.cam_name,self.building_name,save_path,self.email_address,self.phone_numbers)

                    dets_to_sort = np.empty((0,6))
                    # NOTE: We send in detected object class too
                    for x1,y1,x2,y2,conf,detclass in det.cpu().detach().numpy():
                        dets_to_sort = np.vstack((dets_to_sort, 
                                    np.array([x1, y1, x2, y2, conf, detclass])))


                    if self.opt.track:
    
                        tracked_dets = sort_tracker.update(dets_to_sort, self.opt.unique_track_color)
                        tracks =sort_tracker.getTrackers()

                        # draw boxes for visualization
                        if len(tracked_dets)>0:
                            bbox_xyxy = tracked_dets[:,:4]
                            identities = tracked_dets[:, 8]
                            categories = tracked_dets[:, 4]
                            confidences = None

                            if self.opt.show_track:
                                #loop over tracks
                                for t, track in enumerate(tracks):
                    
                                    track_color = colors[int(track.detclass)] if not self.opt.unique_track_color else sort_tracker.color_list[t]

                                    [cv2.line(im0, (int(track.centroidarr[i][0]),
                                                    int(track.centroidarr[i][1])), 
                                                    (int(track.centroidarr[i+1][0]),
                                                    int(track.centroidarr[i+1][1])),
                                                    track_color, thickness=self.opt.thickness) 
                                                    for i,_ in  enumerate(track.centroidarr) 
                                                        if i < len(track.centroidarr)-1 ] 
                    else:
                        bbox_xyxy = dets_to_sort[:,:4]
                        identities = None
                        categories = dets_to_sort[:, 5]
                        confidences = dets_to_sort[:, 4]
                    
                    im0 = self.draw_boxes(im0, bbox_xyxy, identities, categories, confidences, names, colors)

                    
                        
                    
                    
                # Print time (inference + NMS)
                print(f'{s}Done. ({(1E3 * (t2 - t1)):.1f}ms) Inference, ({(1E3 * (t3 - t2)):.1f}ms) NMS')

                # Stream results
                ######################################################
                if dataset.mode != 'image' and self.opt.show_fps:
                    currentTime = time.time()

                    fps = 1/(currentTime - startTime)
                    startTime = currentTime
                    cv2.putText(im0, "FPS: " + str(int(fps)), (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0),2)

                #######################################################
                if view_img:
                    cv2.imshow(str(p), im0)
                    cv2.waitKey(1)  # 1 millisecond

                # Save results (image with detections)
                if save_img:
                    if dataset.mode == 'image':
                        cv2.imwrite(save_path, im0)
                        print(f" The image with the result is saved in: {save_path}")
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
                                save_path += '.webm'
                            vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'VP90'), fps, (w, h))
                        vid_writer.write(im0)
                        print("isReadyToUpload===>",isReadyToUpload)
                        print("Person Detedted===>",uploadVideo)
                        print("**************************isReadyToUpload && Person Detected =",isReadyToUpload and uploadVideo)
                        if(personDetected and not isReadyToUpload):
                            uploadVideo =True
                        
                        if(isReadyToUpload and uploadVideo):
                            uploadVideo=False
                            self.UpdateAlertDetailsIntoDB(self.group_name,self.cam_name,self.building_name,previousVideoPath)
            print('datetime.now():', datetime.now())
            print('process_endtime:', process_endtime)
            print('countValue:', countValue)
            # FIXME, have to remove the countValue condition
            if(datetime.now() >= process_endtime or countValue > 100):
                print('Path name:', p)
                print('P name:', p.name)
                cv2.destroyWindow(str(p))
                break
            else:
                print('Still condition not satisfy')

        if save_txt or save_img:
            s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
            #print(f"Results saved to {save_dir}{s}")

        print(f'Done. ({time.time() - t0:.3f}s)')

    def insertAlertDetailsIntoDB(self, group_name,cam_name,building_name,save_path,email_address,phone_numbers) :
            print("person detected -- Insert cam info into db")
            alertData = {}
            alertData['org_name'] = group_name
            alertData['camera_name'] = cam_name
            alertData['camera_location'] = building_name
            alertData['alert_time'] = datetime.now()
            #save_path=save_path.replace("\\","abcd")
            alertData['video_location'] = save_path+'.webm'
            alertName =alertData['alert_name']=alertData['org_name']+alertData['camera_name']+alertData['camera_location']+ alertData['video_location'] 
            alertData['alert_name']=alertName
            alertData['status']='inprogress'
            alertData['email_address']=email_address
            alertData['phone_numbers']=phone_numbers
            alertData['message_status']='not send'
            alertData['notification_link_status']='not send'
            alertcursor = AlertDetails.find_alert_details_by_filterCondition({'alert_name': alertName})
            alertlist = list(alertcursor)
            if len(alertlist) == 0:
                print("insert db=",alertData )
                AlertDetails.create_alert(alertData)
                print('Insert DB completedddd',alertData)
    
    def UpdateAlertDetailsIntoDB(self, group_name,cam_name,building_name,save_path) :
    	
        #to get unique id
        print("Updatting db with status==completed")
        #save_path=save_path.replace("\\","abcd")
        alertName =group_name+cam_name+building_name+ save_path
        print("filter condition*******",alertName)
        alertcursor = AlertDetails.find_alert_details_by_filterCondition({'alert_name': alertName})
        alertlist = list(alertcursor)
        print('No of records in UpdateAlertDetailsIntoDB Notification:', len(alertlist))
        for alertData in alertlist:
            alertData['status']='ready'
            alertData = {"$set": alertData}
            AlertDetails.update_alert({'alert_name': alertName}, alertData)
        print('Alert Update DB completed')                   

    def __init__(self):
        print('detect obj')
        parser = argparse.ArgumentParser()
        parser.add_argument('--weights', nargs='+', type=str, default='yolov7.pt', help='model.pt path(s)')
        parser.add_argument('--source', type=str, default='inference/images', help='source')  # file/folder, 0 for webcam
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

        parser.add_argument('--track', action='store_true', help='run tracking')
        parser.add_argument('--show-track', action='store_true', help='show tracked path')
        parser.add_argument('--show-fps', action='store_true', help='show fps')
        parser.add_argument('--thickness', type=int, default=2, help='bounding box and font size thickness')
        parser.add_argument('--seed', type=int, default=1, help='random seed to control bbox colors')
        parser.add_argument('--nobbox', action='store_true', help='don`t show bounding box')
        parser.add_argument('--nolabel', action='store_true', help='don`t show label')
        parser.add_argument('--unique-track-color', action='store_true', help='show each track in unique color')

        self.opt = parser.parse_args()
        print('self.opt', self.opt)

        np.random.seed(self.opt.seed)

        sort_tracker = Sort(max_age=5,
                        min_hits=2,
                        iou_threshold=0.2) 

        #check_requirements(exclude=('pycocotools', 'thop'))

        #with torch.no_grad():
        #    if self.opt.update:  # update all models (to fix SourceChangeWarning)
        #        for self.opt.weights in ['yolov7.pt']:
        #            detect()
        #            strip_optimizer(self.opt.weights)
        #    else:
        #        detect()

    def detect_process(self, url, process_endtime,group_name,cam_name,building_name,email_address,phone_numbers):
        print('***********detect_track_object_method')
        #for self.opt.weights in ['yolov7.pt']:
        self.opt.weights = 'spyproj\yolov7\yolov7.pt'
        self.opt.img_size = 640
        #self.opt.source = 'https://www.youtube.com/watch?v=BTFWu21-arc'
        #self.opt.source = '0'
        self.opt.source = url
        self.opt.conf = 0.25
        self.opt.save_img = False
        self.process_endtime = process_endtime
        self.group_name = group_name
        self.cam_name = cam_name
        self.building_name = building_name
        self.email_address = email_address
        self.phone_numbers = phone_numbers
        self.detect()
        strip_optimizer(self.opt.weights)
