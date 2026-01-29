import cv2
import pytesseract 
import matplotlib.pyplot as plt

# tesseract path:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def detect_plate (img_path):

    img= cv2.imread(img_path)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred=cv2.GaussianBlur(gray, (5,5),0)
   

   # applying canny edge detection and finding contours

    edges= cv2.Canny(blurred, 100, 200)
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    
    contours= sorted(contours, key=cv2.contourArea, reverse=True)
    plate_contour= None

    for contour in contours:
        e= 0.02* cv2.arcLength(contour, True)
        approx= cv2.approxPolyDP(contour, e, True)

        if len(approx)==4:
            plate_contour= approx
            break
    
    if plate_contour is not None:
        x,y,w,h= cv2.boundingRect(plate_contour)
        plate_img=gray[y:y+h,x:x+w]

        _,thresh=cv2.threshold(plate_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    ocr_result= pytesseract.image_to_string(thresh, config='--psm 8')
    plt.imshow(cv2.cvtColor(plate_img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.title(f"OCR Result: {ocr_result.strip()}")
    plt.show()
    return ocr_result

detect_plate(r"C:\Testing\OCR\1_qre-gAVNTuazaUPvNw2w-Q.jpg")