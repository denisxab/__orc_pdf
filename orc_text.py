import cv2

try:
	from PIL import Image
except ImportError:
	import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'

TEST_PATH_FROM_BOX = "output_file/serh_box_text/cap0.png"

if __name__ == '__main__':
	image_file = TEST_PATH_FROM_BOX
	img = cv2.imread(image_file)

	print(pytesseract.image_to_string(img))
