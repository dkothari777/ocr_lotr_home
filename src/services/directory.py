import zipfile
import tempfile
import os


class DirectoryImageService:
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff']

    def __init__(self, path):
        actual_path, self.is_zip = self.__validate__(path)
        self.path = actual_path

    def check_for_images(self, path_to_check):
        image_files_found = False
        files = os.listdir(path_to_check)
        for file in files:
            file_extension = os.path.splitext(file)[-1].lower()
            if file_extension in self.image_extensions:
                image_files_found = True
        if not image_files_found:
            return False
        return True

    def __validate__(self, path_to_check):
        if os.path.exists(path_to_check):
            if os.path.isdir(path_to_check):
                if self.check_for_images(path_to_check):
                    return path_to_check, False
                else:
                    raise Exception(f"No image files found in the directory: {path_to_check}.")
            if zipfile.is_zipfile(path_to_check):
                actual_path = self.__unzip__(path_to_check)
                if self.check_for_images(actual_path):
                    return actual_path, True
                else:
                    self.cleanup(actual_path)
                    raise Exception(f"No image files found in the zipfile: {path_to_check}.")
            raise Exception(f"No images found in zip or directory: {path_to_check}")

    @staticmethod
    def __unzip__(path):
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
        return temp_dir

    def list_images(self):
        images_files = []
        files = os.listdir(self.path)
        for file in files:
            file_extension = os.path.splitext(file)[-1].lower()
            if file_extension in self.image_extensions:
                images_files.append(self.path + "/" + file)
        return sorted(images_files)

    def cleanup(self, path=None):
        real_path = path if path else self.path
        if self.is_zip:
            os.rmdir(real_path)
