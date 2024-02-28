import os

from app.config import Config


def get_project_image_cover_data(project_id):
    directory = Config.BASE_DIR + f"/app/images/{project_id}/"

    image_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if image_files:
        cover_image_path = os.path.join(directory, image_files[0])

        with open(cover_image_path, 'rb') as image_file:
            image_data = image_file.read()

        return image_data