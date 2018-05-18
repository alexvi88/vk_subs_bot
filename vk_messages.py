import vk
import settings


def send_message_to_user(user_id, message):
    session = vk.Session()
    api = vk.API(session, v=settings.vk_api_version)
    api.messages.send(access_token=settings.access_key, user_id=user_id, message=message)


def send_post_to_user(user_id, post_info):
    session = vk.Session(access_token=settings.access_key)
    vk_api = vk.API(session, v=settings.vk_api_version)
    vk_api.messages.send(user_id=user_id, attachment=post_info, peer_id=settings.bot_group_id)
    
