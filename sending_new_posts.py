import os
import methods_for_db
import vk_messages
import groups_tools
import settings

def send_new_posts_to_all_users():
    all_users_ids = get_all_users_ids()
    for user_id in all_users_ids:
        posts_for_this_user = []

        cur_user_groups = methods_for_db.get_user_groups(user_id)

        for cur_group_id in cur_user_groups:
            posts_for_this_user.extend(groups_tools.get_posts(user_id, cur_group_id))

        for post in posts_for_this_user:
            if post['marked_as_ads'] == 0:
                post_info = "wall" + str(post['from_id']) + "_" + str(post['id'])
                vk_messages.send_post_to_user(user_id, post_info)


def get_all_users_ids():
    my_directory = settings.directory_with_users
    files = os.listdir(my_directory)
    ans = []
    for file in files:
        ans.append(file[:-3:])

    return ans
