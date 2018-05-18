import vk
import settings
import methods_for_db
import datetime


def get_posts(user_id, group_id):
    if not methods_for_db.have_subs(user_id):
        return []

    last_post_date = methods_for_db.get_group_last_date(user_id, group_id)

    session = vk.Session(access_token=settings.service_key)
    vk_api = vk.API(session, v=settings.vk_api_version)

    wall = vk_api.wall.get(owner_id='-' + str(group_id),  count=10)['items']

    now_d = datetime.datetime.now()
    new_time = int(now_d.timestamp())

    ans = [rec for rec in reversed(wall) if rec['date'] > last_post_date]

    methods_for_db.update_group_last_date(user_id, group_id, new_time)

    return ans


def get_group(group_link):
    short_name = group_link[15::]
    session = vk.Session(access_token=settings.access_key)
    vk_api = vk.API(session, v=settings.vk_api_version)
    cur_group = vk_api.groups.getById(group_id = short_name)[0]

    if str(cur_group['id']) == str(settings.bot_group_id) and group_link != settings.bot_group_link:
        return 'link_error'

    return cur_group


def get_group_name(group_id):
    session = vk.Session(access_token=settings.access_key)
    vk_api = vk.API(session, v=settings.vk_api_version)
    cur_group = vk_api.groups.getById(group_id=group_id)[0]
    return cur_group['name']
