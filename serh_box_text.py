import cv2

from flat_rotate_photo import ShowImagePlt, gray_image, write_image

TEST_PATH_FROM_BOX = "output_file/flat_rotate_photo/image0-0.png"
TEST_PATH_OUTPUT = "output_file/serh_box_text/"


def show_rectangle(img, x, w, y, y2):
	image = img.copy()
	cv2.rectangle(image, (x, w), (y, y2), (255, 0, 0), 4)
	ShowImagePlt(image, "Квадрат")


if __name__ == '__main__':
	image_origin = cv2.imread(TEST_PATH_FROM_BOX)
	# ShowImagePlt(image_origin, "Изначально")

	x, y, end_x, pad_y = 1250, 2150, 1380, 700
	# show_rectangle(image_origin, x, y, end_x, pad_y)

	cap_imag = image_origin[pad_y:y, x:x + (end_x - x)]
	# ShowImagePlt(cap_imag, "Обрезанный кусок")

	cap_num_imag = image_origin[pad_y:790, x:x + (end_x - x)]
	# ShowImagePlt(cap_num_imag, "Обрезанный кусок числа")

	cap_num_imag = gray_image(cap_num_imag)
	# ShowImagePlt(cap_num_imag, "Обрезанный  чб кусок числа")

	write_image("output_file/serh_box_text/cap0.png", cap_num_imag)


