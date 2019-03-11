import pyqrcode
import cv2
import zbar
from PIL import Image
#import qrcode

#cv2.namedWindow("QRcode")
cap = cv2.VideoCapture(0)
cap.set(3,600)
cap.set(4,600)

scanner = zbar.ImageScanner()
scanner.parse_config('enable')

# Capture frames from the camera
while True:
    ret, output = cap.read()
    if not ret:
         continue
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY, dstCn=0)
    pil = Image.fromarray(gray)
    width, height = pil.size
    raw = pil.tobytes()
    image = zbar.Image(width, height, 'Y800', raw)
    scanner.scan(image)

    for symbol in image:
        print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
        a = pyqrcode.create(content=unicode(symbol.data,'utf-8'))
        a.png(file='test.jpeg',scale=10)
        break

    cv2.imshow("#iothack15", output)

    # clear stream for next frame
    #rawCapture.truncate(0)

    # Wait for the magic key
    keypress = cv2.waitKey(1) & 0xFF
    if keypress == ord('q'):
    	break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
