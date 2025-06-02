from datetime import datetime, timedelta


from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from app import users_db
from app.models import User
from config import OPENAI_API_KEY
from generators.image_gen import ImageGenerator
from generators.text_gen import TextGenerator
from social_publishers.vk_publisher import VKPublisher
from social_publishers.vk_self_publisher import VK2Publisher
from social_stats.vk_stats import VKStats

smm_bp = Blueprint('smm', __name__, url_prefix='/smm', template_folder='templates')

@smm_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        current_user.vk_api_key = request.form.get('vk_api_key')
        current_user.vk_group_id = request.form.get('vk_group_id')
        users_db.session.commit()
    return render_template('dashboard.html', user=current_user)


@smm_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        current_user.vk_api_key = request.form['vk_api_key']
        current_user.vk_group_id = request.form['vk_group_id']
        users_db.session.commit()
        flash('Settings saved successfully.')
    return render_template('settings.html', user=current_user)

@smm_bp.route('/post_generator', methods=['GET', 'POST'])
@login_required
def post_generator():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'generate':
            tone = request.form['tone']
            topic = request.form['topic']
            generate_image = 'generate_image' in request.form
            auto_post = 'auto_post' in request.form
            openai_key = OPENAI_API_KEY
            user = User.query.filter_by(id=current_user.id).first()
            text_generator = TextGenerator(openai_key, tone, topic)
            content = text_generator.generate_text()

            session['post_content'] = content

            if generate_image:
                img_desc = text_generator.generate_image_description()
                image_generator = ImageGenerator(openai_key)
                image_url = image_generator.generate_image(img_desc)
                session['image_url'] = image_url

            else:
                image_url = None
            if auto_post:
                if content:
                    vk_publisher = VKPublisher(user.vk_api_key, user.vk_group_id)
                    vk_publisher.publish_post(content, image_url)
                    flash('Пост успешно опубликован.')
                else:
                    flash('Пост не найден.')
            return render_template('post_generator.html', user=current_user, post_content=content, image_url=image_url)

        elif action == 'publish':
            content = session.get('post_content')
            image_url = session.get('image_url')

            if content:
                # vk_publisher = VKPublisher(current_user.vk_api_key, current_user.vk_group_id)
                vk_publisher = VK2Publisher(current_user.vk_api_key)
                vk_publisher.publish_post(content, image_url)
                flash('Пост успешно опубликован.')
            else:
                flash('Нет контента для публикации.')
            return render_template('post_generator.html', user=current_user, post_content=content, image_url=image_url)

    return render_template('post_generator.html')

@smm_bp.route('/vk_stats', methods=['GET', 'POST'])
@login_required
def vk_stats():
    now = datetime.now()
    three_days_ago = now - timedelta(days=3)
    vk_stats = VKStats(current_user.vk_api_key, current_user.vk_group_id)
    followers = vk_stats.get_followers()
    stats_data = vk_stats.get_stats(three_days_ago.strftime('%Y-%m-%d'), now.strftime('%Y-%m-%d'))
    stats = {
        'views': stats_data['visitors']['views'],
        'followers': followers
    }

    return render_template('vk_stats.html', stats=stats)