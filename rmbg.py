from werkzeug.datastructures import FileStorage
from rembg import remove
from PIL import Image
from io import BytesIO

def remove_background(file: FileStorage):
        input_image = Image.open(file.stream)
        output_image = remove(input_image, post_process_mask=True)
        img_io = BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)
        return img_io
