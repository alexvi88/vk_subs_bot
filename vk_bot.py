from flask import Flask
from flask import request
import vk_messages
import typical_messages
import settings
import json
import messages_parsing
import methods_for_db
import sending_new_posts
import groups_tools


app = Flask(__name__)


@app.route('/', methods=['POST'])
def processing():

    data = json.loads(request.data)

    if 'type' not in data.keys():
        return 'ok'

    if 'secret' not in data.keys():
        return 'ok'

    if data['secret'] != settings.secret_key:
        return 'ok'

    if data['type'] == 'confirmation':
        return settings.confirmation_key

    if data['type'] == 'message_new':
        user_id = str(data['object']['user_id'])
        received_message = data['object']['body']

        if received_message == 'help':
            message = typical_messages.help_message
            vk_messages.send_message_to_user(user_id=user_id, message=message)
            return 'ok'

        type_of_act = messages_parsing.get_type_of_act(received_message)

        if type_of_act == 'query_error':
            message = typical_messages.query_error_message
            vk_messages.send_message_to_user(user_id=user_id, message=message)
            sending_new_posts.send_new_posts_to_all_users()
            return 'ok'

        if type_of_act == 'remove_all':
            methods_for_db.delete_user(user_id)
            message = typical_messages.success_message
            vk_messages.send_message_to_user(user_id=user_id, message=message)
            return 'ok'

        if type_of_act == 'get_groups':
            message = ""
            groups = methods_for_db.get_user_groups(user_id)
            if groups == 'Empty':
                message = 'У Вас нет подписок'
            else:
                for group in groups:
                    message += groups_tools.get_group_name(group) + "\n"

            vk_messages.send_message_to_user(user_id=user_id, message=message)
            sending_new_posts.send_new_posts_to_all_users()
            return 'ok'

        group_link = type_of_act[1]

        group = groups_tools.get_group(group_link)

        if group == 'link_error':
            message = typical_messages.link_error_message
            vk_messages.send_message_to_user(user_id=user_id, message=message)
            sending_new_posts.send_new_posts_to_all_users()
            return 'ok'

        group_id = group['id']

        if group['is_closed'] in [1, 2]:
            message = typical_messages.closed_group_message
            vk_messages.send_message_to_user(user_id=user_id, message=message)
            sending_new_posts.send_new_posts_to_all_users()
            return 'ok'

        if type_of_act[0] == 'add_group':
            methods_for_db.add_group_to_user(user_id, group_id)
            message = typical_messages.success_message
            vk_messages.send_message_to_user(user_id=user_id, message=message)
            sending_new_posts.send_new_posts_to_all_users()
            return 'ok'

        if type_of_act[0] == 'remove_group':
            methods_for_db.remove_group_from_user(user_id, group_id)
            message = typical_messages.success_message
            vk_messages.send_message_to_user(user_id=user_id, message=message)
            sending_new_posts.send_new_posts_to_all_users()
            return 'ok'
        return 'ok'

    return 'ok'
    
