import requests
import vk_api

class VK2Publisher:
    def __init__(self, token):
        self.vk_session = vk_api.VkApi(token=token)
        self.vk = self.vk_session.get_api()
        self.user_id = self.vk.users.get()[0]['id']

    def upload_image(self, image_url):
        # 1. Получаем адрес сервера для загрузки фото
        upload_url = self.vk.photos.getWallUploadServer()['upload_url']

        # 2. Скачиваем изображение по ссылке
        response = requests.get(image_url)
        files = {'photo': ('image.jpg', response.content, 'image/jpeg')}

        # 3. Загружаем фото на сервер VK
        upload_response = requests.post(upload_url, files=files).json()

        # 4. Сохраняем фото на стене
        saved_photo = self.vk.photos.saveWallPhoto(
            photo=upload_response['photo'],
            server=upload_response['server'],
            hash=upload_response['hash']
        )[0]

        # 5. Возвращаем attachment строку формата photo<owner_id>_<id>
        return f"photo{saved_photo['owner_id']}_{saved_photo['id']}"

    def publish_post(self, content, image_url=None):
        attachments = []

        if image_url:
            try:
                attachment_photo = self.upload_image(image_url)
                attachments.append(attachment_photo)
            except Exception as e:
                print(f"[Ошибка загрузки изображения]: {e}")

        self.vk.wall.post(
            owner_id=self.user_id,
            message=content,
            attachments=','.join(attachments)
        )
