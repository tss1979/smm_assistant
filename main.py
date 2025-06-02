from datetime import datetime, timedelta

from generators.text_gen import TextGenerator
from generators.image_gen import ImageGenerator
from social_publishers.vk_publisher import VKPublisher
from config import OPENAI_API_KEY, VK_API_KEY, VK_GROUP_ID
from social_stats.vk_stats import VKStats

# if __name__ == "__main__":
#     post = TextGenerator(OPENAI_API_KEY, "Позитивный", "Лучшие миллезимы шампанского за последние 10 лет")
#     content = post.generate_text()
#     img_desc = post.generate_image_description()
#     image = ImageGenerator(OPENAI_API_KEY)
#     image_url = image.generate_image("Лучшие миллезимы шампанского за последние 10 лет")
#
#     vk_pub = VKPublisher(VK_API_KEY, VK_GROUP_ID)
#     vk_pub.publish_post(content, image_url)
#
    # vk_stats = VKStats(VK_API_KEY, VK_GROUP_ID)
    # now = datetime.now()
    # three_days_ago = now - timedelta(days=3)
    # stats_data = vk_stats.get_stats(three_days_ago.strftime('%Y-%m-%d'), now.strftime('%Y-%m-%d'))
    # print(stats_data['visitors'])
from app import create_app

app = create_app()


if __name__ == '__main__':
    app.run(debug=True)


