from Data_recieving_and_Dashboard.mrcnn_demo.m_rcnn import *
from Data_recieving_and_Dashboard.mrcnn_demo.visualize import *
from Data_recieving_and_Dashboard.packages import *
from Data_recieving_and_Dashboard.ocr import OCR

class DetectPanel:
    def __init__(self):
        handle_uploaded_file(str(os.getcwd()) + '/cropped_images_for_panel')
        MODEL_PATH = str(os.getcwd() ) + '/panel_detection_models/' + 'mask_rcnn_object.h5'
        self.CROPPED_IMAGES_FOLDER = str(os.getcwd()) + '/cropped_images_for_panel/'
        self.test_model, self.inference_config = load_inference_model(1, MODEL_PATH)
        self.panel_ocr = OCR()
        
    def detect(self, image_path):
        image = cv2.imread(image_path)
        height, width, _ = image.shape
        print(image.shape)
        number_of_partition = 5
        detected_panels = []
        if not os.path.exists(self.CROPPED_IMAGES_FOLDER):
            os.makedirs(self.CROPPED_IMAGES_FOLDER)
        else:
            for file in os.listdir(self.CROPPED_IMAGES_FOLDER):
                os.remove(os.path.join(self.CROPPED_IMAGES_FOLDER, file))
        if 1 :
        # try:
            results = self.test_model.detect([image])[0]
            object_count = len(results['class_ids'])
            for i in range(object_count):
                temp_dict = {}
                mask = results['masks'][:, :, (i)]
                detected_contours = get_mask_contours(mask)
                valid_contours = self.remove_false_contours(detected_contours)
                for cnt in valid_contours:
                    if self.check_contour_placement(cnt, width, number_of_partition):
                        rack_window_co_ord = self.crop_panel(image, cnt,'{}.jpg'.format(str(i)))
                        detected_panel_number = self.panel_ocr.detect(os.path.join(self.CROPPED_IMAGES_FOLDER, '{}.jpg'. format(str(i))))
                        RESIZE_HEIGHT = 544
                        RESIZE_WIDTH = 960
                        ratio_height = RESIZE_HEIGHT / height
                        ratio_width = RESIZE_WIDTH / width
                        panel_co_cordinates = []
                        rack_window_co_ordinates = []
                        for elem in self.fine_contour(cnt):
                            temp_list = []
                            temp_list.append(int(elem[0] * ratio_width))
                            temp_list.append(int(elem[1] * ratio_height))
                            panel_co_cordinates.append(temp_list)
                        if rack_window_co_ord:
                            rack_window_co_ordinates.append(int(rack_window_co_ord[0] * ratio_width))
                            rack_window_co_ordinates.append(int(rack_window_co_ord[1] * ratio_height))
                            rack_window_co_ordinates.append(int(rack_window_co_ord[2] * ratio_width))
                            rack_window_co_ordinates.append(int(rack_window_co_ord[3] * ratio_height))
                        panel_co_cordinates_str = ''
                        rack_window_co_ordinates_str = ''
                        for co_ords in panel_co_cordinates:
                            for co_ord in co_ords:
                                panel_co_cordinates_str += str(co_ord) + ';'
                        for co_ord in rack_window_co_ordinates:
                            rack_window_co_ordinates_str += str(co_ord) + ';'
                        temp_dict['co_ordinates'] = panel_co_cordinates_str
                        temp_dict['panel_number'] = detected_panel_number
                        temp_dict['rack_window_co_ordinates'] = rack_window_co_ordinates_str
                        if rack_window_co_ord:
                            image = cv2.rectangle(image, (rack_window_co_ord[0], rack_window_co_ord[1]), (rack_window_co_ord[2],rack_window_co_ord[3]), (0, 255, 0), 2)
                        detected_panels.append(temp_dict)
                        resized_image = cv2.resize(image, (960, 544))
                        panel_co_cordinates = np.array(panel_co_cordinates, np.int32)
                        panel_co_cordinates = panel_co_cordinates.reshape((-1, 1, 2))
                        panel_co_cordinates = cv2.polylines(resized_image, [panel_co_cordinates], True, (0, 255, 0), 2)
            #cv2.destroyAllWindows()
            return detected_panels
        # except Exception as e:
        #     print(e)
        #     return detected_panels

    def remove_false_contours(self, contours):
        if 1 :
        # try:
            average_contour_area = None
            average_contour_height = None
            average_contour_width = None
            average_contour_area_list = []
            average_contour_height_list = []
            average_contour_widht_list = []
            valid_contours = []
            for contour in contours:
                average_contour_area_list.append(cv2.contourArea(contour))
                average_contour_height_list.append(cv2.boundingRect(contour)[-1])
                average_contour_widht_list.append(cv2.boundingRect(contour)[-2])
            average_contour_area = int(sum(average_contour_area_list) / len(average_contour_area_list))
            average_contour_height = int(sum(average_contour_height_list) /len(average_contour_height_list))
            average_contour_width = int(sum(average_contour_widht_list) /len(average_contour_widht_list))
            for contour in contours:
                if (average_contour_area - 100 < cv2.contourArea(contour) <average_contour_area + 100 and average_contour_height -100 < cv2.boundingRect(contour)[-1] <  average_contour_height + 100 and average_contour_width - 100 < cv2.boundingRect(contour)[-2] < average_contour_width + 100):
                    valid_contours.append(contour)
            contours = valid_contours
            #cv2.destroyAllWindows()
        # except Exception as e:
        #     print('ERROR WHILE REMOVING FALSE CONTOUR: {}'.format(str(e)))
        return contours

    def check_contour_placement(self, contour, width, num_of_partition):
        if 1:
        # try:
            partition_width = int(width / num_of_partition)
            min_partition_width = partition_width
            max_partition_width = partition_width * (num_of_partition - 1)
            moment = cv2.moments(contour)
            x_co_ords = int(moment['m10'] / moment['m00'])
            if (x_co_ords > min_partition_width and x_co_ords < max_partition_width):
                return True
            else:
                return False
            #cv2.destroyAllWindows()
        # except Exception as e:
        #     print(e)
        #     return False

    def extend_contour(self, contour, image_height, image_array):
        if 1:
        # try:
            pass
        # except Exception as e:
        #     print(e)
        return contour

    def crop_panel(self, image_array, contour, filename):
        rack_window_co_ord = []
        if 1 :
        # try:
            co_ordinates = np.array(contour, np.int32)
            x, y, w, h = cv2.boundingRect(co_ordinates)
            crop_img = image_array[y:y + h, x:x + w]
            height, _, _ = crop_img.shape
            edge = cv2.Canny(crop_img, 50, 150, L2gradient=True)
            keypoints = cv2.findContours(edge.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = imutils.grab_contours(keypoints)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            for contour in contours:
                approx = cv2.approxPolyDP(contour, 10, True)
                if len(approx) == 4:
                    rack_x, rack_y, rack_w, rack_h = cv2.boundingRect(contour)
                    rack_window_y = int((rack_y + rack_y + rack_h) / 2)
                    half_height = height / 2
                    two_third_height_max = height * 2 / 3
                    if (half_height < rack_window_y < two_third_height_max and  2 < rack_w / rack_h < 4 and rack_w / w < 0.3):
                        rack_window_co_ord.append(x + rack_x)
                        rack_window_co_ord.append(y + rack_y)
                        rack_window_co_ord.append(x + rack_x + rack_w)
                        rack_window_co_ord.append(y + rack_y + rack_h)
                        break
            cv2.imwrite(os.path.join(self.CROPPED_IMAGES_FOLDER, filename), crop_img)
            #cv2.destroyAllWindows()
        # except Exception as e:
        #     print('ERROR WHILE CROPPING IMAGE: {}'.format(str(e)))
        return rack_window_co_ord

    def fine_contour(self, contour):
        if 1 : 
        # try:
            number_of_skip_contour = 100
            count = 0
            fine_contour = []
            for co_ordinate in contour:
                if count % number_of_skip_contour == 0:
                    fine_contour.append([int(co_ordinate[0]), int(
                        co_ordinate[1])])
                count += 1
            contour = fine_contour
        # except Exception as e:
        #     print('ERROR WHILE FINING THE CONTOURS: {}'.format(str(e)))
        return contour

    def draw_contour(self, image_array, contour):
        if 1 : 
        # try:
            co_ordinates = np.array(contour, np.int32)
            co_ordinates = co_ordinates.reshape((-1, 1, 2))
            image_array = cv2.polylines(image_array, [co_ordinates], True,(0, 255, 0), 2)
            #cv2.destroyAllWindows()
        # except Exception as e:
        #     print('ERROR WHILE DRAWING CONTOUR: {}'.format(str(e)))
        return image_array

    def display_image(self, image_array):
        if 1: 
        # try:
            image_array = cv2.resize(image_array, (720, 480))
            cv2.imshow('Panel Detection', image_array)
            cv2.waitKey(0)
            #cv2.destroyAllWindows()
        # except Exception as e:
        #     print('ERROR WhILE DISPLAYING IMAGE: {}'.format(str(e)))
