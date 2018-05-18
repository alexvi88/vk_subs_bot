from tables_for_db import Base, user_groups
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


def add_group_to_user(user_id, group_id):
    engine = create_engine("sqlite:////home/alexander888/mysite/users/" + user_id + ".db")

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    cur_session = Session()

    new_group = user_groups(group_id)

    if cur_session.query(user_groups).filter_by(group_id=group_id).first() is None:
        cur_session.add(new_group)

    cur_session.commit()
    cur_session.close()


def remove_group_from_user(user_id, del_group_id):
    engine = create_engine("sqlite:////home/alexander888/mysite/users/" + user_id + ".db")

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    cur_session = Session()

    if cur_session.query(user_groups).filter_by(group_id=del_group_id).first() is not None:
        group_to_del = cur_session.query(user_groups).filter_by(group_id=del_group_id).first()
        cur_session.delete(group_to_del)

    need_deleting = False
    need_deleting = (cur_session.query(user_groups).first() is  None)

    cur_session.commit()
    cur_session.close()

    if need_deleting:
        delete_user(user_id)


def get_user_groups(user_id):
    if not have_subs(user_id):
        return 'Empty'

    engine = create_engine("sqlite:////home/alexander888/mysite/users/" + user_id + ".db")

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    cur_session = Session()

    groups = cur_session.query(user_groups).all()
    answer = []
    for gr in groups:
        answer.append(str(gr))

    cur_session.close()

    return answer


def delete_user(user_id):
    path = "/home/alexander888/mysite/users/" + user_id + ".db"
    if have_subs(user_id):
        os.remove(path=path)


def get_group_last_date(user_id, group_id):
    engine = create_engine("sqlite:////home/alexander888/mysite/users/" + user_id + ".db")

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    cur_session = Session()

    needed_group = cur_session.query(user_groups).filter_by(group_id=group_id).first()
    ans = int(needed_group.group_last_time)

    cur_session.commit()
    cur_session.close()
    return ans


def update_group_last_date(user_id, group_id, new_time):
    engine = create_engine("sqlite:////home/alexander888/mysite/users/" + user_id + ".db")

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    cur_session = Session()

    needed_group = cur_session.query(user_groups).filter_by(group_id=group_id).first()
    needed_group.group_last_time = new_time

    cur_session.commit()
    cur_session.close()


def have_subs(user_id):
    path = "/home/alexander888/mysite/users/" + user_id + ".db"
    if os.path.exists(path):
        return True

    return False
