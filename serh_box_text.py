import cv2

from flat_rotate_photo import ShowImagePlt

TEST_PATH_FROM_BOX = "output_file/flat_rotate_photo/image0-0.png"
TEST_PATH_OUTPUT = "output_file/serh_box_text/"

if __name__ == '__main__':
	image_origin = cv2.imread(TEST_PATH_FROM_BOX)
	ShowImagePlt(image_origin, "Изначально")
