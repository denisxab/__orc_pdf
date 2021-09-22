import fitz

TEST_PATH_FROM_PDF = "test/test_pdf_template/doc08095520210906111101.pdf"
TEST_PATH_OUTPUT = "output_file/get_image_from_pdf"


class GetImageFromPdf:
	def __init__(self, file_path_pdf: str, file_path_output_img: str, limit_convert_page_from_pdf: int = None):
		"""
		Из .pdf в .png

		:param file_path_pdf: Путь к Pdf файлу
		:param file_path_output_img: Путь к папке в которую будет помещен результат
		:param limit_convert_page_from_pdf: Ограничение страниц до которой нужно конвертировать
		"""

		self._file_path_pdf: str = file_path_pdf
		self._file_path_output_img: str = file_path_output_img
		self._limit_convert_page_from_pdf: int = limit_convert_page_from_pdf

		self._pdf_obj: fitz.Document = self._open_pdf()
		self._number_of_pages: int = limit_convert_page_from_pdf \
			if limit_convert_page_from_pdf is not None and limit_convert_page_from_pdf <= len(self._pdf_obj) \
			else len(self._pdf_obj)

		self._convert_pdf_to_image()

	def _open_pdf(self) -> fitz.Document:
		"""
		# Открытия PDF файла, и получить объект fitz.Document
		:param file_path:  Путь к PDF
		"""
		return fitz.open(self._file_path_pdf)

	def _convert_pdf_to_image(self):

		# Итерация по каждой странице в pdf
		for current_page_index in range(self._number_of_pages):
			# Итерация по каждому изображению на каждой странице PDF
			for img_index, img in enumerate(self._pdf_obj.getPageImageList(current_page_index)):
				xref = img[0]  # Зарезервировать участок памяти
				image = fitz.Pixmap(self._pdf_obj, xref)
				# Eсли это чёрно-белое или цветное изображение
				if image.n < 5:
					image.writePNG("{}/image{}-{}.png".format(self._file_path_output_img, current_page_index, img_index))
				# Eсли это CMYK: конвертируем в RGB
				else:
					new_image = fitz.Pixmap(fitz.csRGB, image)
					new_image.writePNG("{}/image{}-{}.png".foramt(self._file_path_output_img, current_page_index, img_index))


if __name__ == '__main__':
	GetImageFromPdf(TEST_PATH_FROM_PDF, TEST_PATH_OUTPUT)
