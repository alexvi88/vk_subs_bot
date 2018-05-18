import re


def get_type_of_act(received_message):
    received_message = str.strip(received_message)

    if received_message == "?":
        return 'get_groups'

    if received_message == "- all":
        return 'remove_all'

    pattern1 = re.compile('[+-] https://vk.com/[/_0-9, a-zA-Z]*')
    pattern2 = re.compile('[+-] <https://vk.com/[/_0-9a-zA-Z]*>')

    pattern1_suits = pattern1.fullmatch(received_message)
    pattern2_suits = pattern2.fullmatch(received_message)

    message_suits = (pattern1_suits is not None) or (pattern2_suits is not None)

    if not message_suits:
        return 'query_error'

    group_link = received_message[2::]

    if received_message[0] == '+':
        return ('add_group', group_link)

    if received_message[0] == '-':
        return ('remove_group', group_link)
