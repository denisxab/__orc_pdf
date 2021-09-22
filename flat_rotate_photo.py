import cv2
import matplotlib.pyplot as plt
import numpy as np

# TEST_PATH_FROM_ROTATE = "/home/denis/PycharmProjects/orc_pdf/test/test_rotation_text_img/-27_.png"    #26|26      (-)
# TEST_PATH_FROM_ROTATE = "/home/denis/PycharmProjects/orc_pdf/test/test_rotation_text_img/26g.png"     #64|-25     (+)
# TEST_PATH_FROM_ROTATE = "/home/denis/PycharmProjects/orc_pdf/test/test_rotation_text_img/44g.png"  # 45|-44     (+)
# TEST_PATH_FROM_ROTATE = "/home/denis/PycharmProjects/orc_pdf/test/test_rotation_text_img/0g.png"      #90|0       (+)

TEST_PATH_FROM_ROTATE = "/home/denis/PycharmProjects/orc_pdf/output_file/get_image_from_pdf/image8-0.png"  # 1.5|1.5   (+)

TEST_PATH_OUTPUT = "output_file/flat_rotate_photo/"


def ShowImagePlt(img: np.ndarray, title: str = "No Name") -> None:
	"""
	Показать изображение в matplotlib.pyplot
	:param img:
	:param title:Оглавление изображения
	"""
	plt.suptitle(title)  # Название заголовка
	plt.xlabel('X')  # Название X
	plt.ylabel('Y')  # Название Y
	plt.grid(True)  # Установить сетку
	plt.imshow(img, cmap='gray',extent=[0,1500,0,2000])  # Загрузить в черно-белом режиме
	plt.show()  # Отобразить


def blur_image(img: np.ndarray) -> np.ndarray:
	"""
	Размыть изображения
	https://i.imgur.com/hXHe1TV.png
	"""
	return cv2.blur(img, (10, 30))  # Влияет на степень размытия


def gray_image(img: np.ndarray) -> np.ndarray:
	"""
	Преобразуйте изображение в оттенки серого

	https://i.imgur.com/APmgnkB.png
	:return: gray
	"""
	return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # В черно-белый


def brighten_image(img: np.ndarray) -> np.ndarray:
	"""
	Засветлеть участки в изображении

	https://i.imgur.com/AQfvEY3.png
	:return: thresh
	"""
	# Порог изображения, устанавливая для всех пикселей переднего плана значение
	# 255 и все пиксели фона на 0
	return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]


def highlighting_text(img: np.ndarray, thresh_filtered) -> tuple[np.ndarray, np.ndarray]:
	"""
	Выделение цветом участки с текстом

	https://i.imgur.com/IOn1XCT.png

	:param img:
	:param thresh_filtered: получить из `brighten_image()`
	"""
	nonZeroCoordinates = cv2.findNonZero(thresh_filtered)
	imageCopy = img.copy()
	for pt in nonZeroCoordinates:
		imageCopy = cv2.circle(imageCopy, (pt[0][0], pt[0][1]), 1, (255, 0, 0))

	return imageCopy, nonZeroCoordinates


def del_noise_from_image(img: np.ndarray, kernel_size: int = 4):
	"""
	Удалить шум в изображение

	https://i.imgur.com/AIJF42W.png

	:param img:
	:param kernel_size:  # Чем выше значение, тем больше шума удаляется
	"""
	ksize = (kernel_size, kernel_size)
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ksize)
	return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)


def rotation_image(img: np.ndarray, turning_angle: float):
	"""
	Поворот изображения на указанный угол
	:param img:
	:param turning_angle:
	"""
	h, w, c = image.shape
	scale = 1.0
	center = (w / 2., h / 2.)
	M = cv2.getRotationMatrix2D(center, turning_angle, scale)
	rotated = img.copy()
	cv2.warpAffine(img, M, (w, h), rotated, cv2.INTER_CUBIC, cv2.BORDER_REPLICATE)
	return rotated


def get_angel_image(turning_angle: float):
	"""
	Преобразование угла поворота

	`turning_angle = box[2]`

	:param turning_angle: Угол поворота
	"""
	if turning_angle < 45:
		turning_angle = turning_angle  # 90 + angle
	else:
		turning_angle = turning_angle - 90  # -(90 % angle)
	return turning_angle


###
def draw_angel_in_image(img: np.ndarray, turning_angle: float) -> None:
	"""
	Нарисовать угол поворота в изображении

	:param img:
	:param turning_angle:
	"""
	cv2.putText(img, "Angle: {:.2f} degrees".format(turning_angle),
	            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


def draw_rectangle_in_image_and_get_angel(img: np.ndarray, nonZeroCoordinates: np.ndarray) -> float:
	"""
	Нарисовать квадрат на изображении

	:param img:
	:param nonZeroCoordinates: получить из `highlighting_text()`
	:return:
	"""
	box = cv2.minAreaRect(nonZeroCoordinates)  # Тут получаем угол поворота, и другое
	boxPts = cv2.boxPoints(box)
	for i in range(4):
		pt1 = (boxPts[i][0], boxPts[i][1])
		pt2 = (boxPts[(i + 1) % 4][0], boxPts[(i + 1) % 4][1])
		cv2.line(img, (int(pt1[0]), int(pt1[1])), (int(pt2[0]), int(pt2[1])), (0, 255, 0), 2, cv2.LINE_AA)

	return box[2]


###

if __name__ == '__main__':
	image_origin = cv2.imread(TEST_PATH_FROM_ROTATE)
	ShowImagePlt(image_origin, "Изначально")

	image = blur_image(image_origin)
	ShowImagePlt(image, "Размытый")

	gray = gray_image(image)
	ShowImagePlt(gray, " Черно-белый")

	thresh = brighten_image(gray)
	ShowImagePlt(thresh, "Засветить")

	imageCopy, nonZeroCoordinates = highlighting_text(image, thresh)
	ShowImagePlt(imageCopy, "Выделение цветом")

	angel_dirty = draw_rectangle_in_image_and_get_angel(imageCopy, nonZeroCoordinates)
	ShowImagePlt(imageCopy, "Рамка с текстом")

	#
	print(f'Угол поворота до: {angel_dirty}')
	angle_pure = get_angel_image(angel_dirty)
	print(f'Угол поворота после: {angle_pure}')
	#

	rotated = rotation_image(image_origin, angle_pure)
	ShowImagePlt(rotated, "Итог")

	#
	cv2.imshow(f"{angel_dirty}", rotated)
	# cv2.waitKey(0)
	#

	#
	cv2.imwrite(f'{TEST_PATH_OUTPUT}image{0}-0.png', rotated)
#
