import easyocr
import cv2


class OCR:

    def __init__(self):
        self.reader = easyocr.Reader(['en'], gpu=False)

    def detect(self, image_path=None):
        detected_number = None
        valid_panel_number = []
        try:
            if image_path:
                img = cv2.imread(image_path)
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                binary_img = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 131, 15)
                _, _, boxes, _ = cv2.connectedComponentsWithStats(binary_img)
                boxes = boxes[1:]
                filtered_boxes = []
                for x, y, w, h, pixels in boxes:
                    if h < 80 and w < 80 and h > 10 and w > 10:
                        if h < w:
                            filtered_boxes.append((x, y, w, h))
                for x, y, w, h in filtered_boxes:
                    x_centriod = int((x + x + w) / 2)
                    y_centriod = int((y + y + h) / 2)
                    if x_centriod > int(img.shape[1] / 2) and int(img.shape[0] / 3) < y_centriod < int(img.shape[0] / 3) * 2:
                        new_img = img.copy()
                        new_img = cv2.rectangle(new_img, (x, y), (x + w, y +h), (0, 255, 0), 3)
                        crop_img = img[y:y + h, x:x + w]
                        crop_img = cv2.resize(crop_img, (400, 400))
                        result = self.reader.readtext(crop_img)
                        for _, detected_number, _ in result:
                            if detected_number.isdigit():
                                if len(detected_number) < 3:
                                    valid_panel_number.append(detected_number)
                        #cv2.destroyAllWindows()
            else:
                valid_panel_number = None
        except Exception as e:
            print('ERR:', e)
            valid_panel_number = None
        if valid_panel_number:
            valid_panel_number = valid_panel_number[0]
        else:
            valid_panel_number = None
        return valid_panel_number
