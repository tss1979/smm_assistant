from generators.text_gen import TextGenerator
from generators.image_gen import ImageGenerator
from social_publishers.vk_publisher import VKPublisher
from config import OPENAI_API_KEY, VK_API_KEY, VK_GROUP_ID
from social_stats.vk_stats import VKStats

if __name__ == "__main__":
    post = TextGenerator(OPENAI_API_KEY, "Позитивный", "Шампанское Salon S")
    content = post.generate_text()
    img_desc = post.generate_image_description()
    image = ImageGenerator(OPENAI_API_KEY)
    image_url = image.generate_image("Шампанское Salon S")

    vk_pub = VKPublisher(VK_API_KEY, VK_GROUP_ID)
    vk_pub.publish_post(content, image_url)

    vk_stats = VKStats(VK_API_KEY, VK_GROUP_ID)
    followers = vk_stats.get_followers()
    print(followers)
    stats = vk_stats.get_stats("2025-01-01", "2025-05-30")
    print(stats)



