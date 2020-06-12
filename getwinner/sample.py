import random

import vk
import datetime


def get_liked_posts(default_list):
    active_list = []
    day_from, mon_from, year_from = input('Date from: ').split('.')
    day_till, mon_till, year_till = input('Date to: ').split('.')
    date_from = datetime.datetime(int(year_from), int(mon_from), int(day_from))
    from_ts = date_from.timestamp()
    date_to = datetime.datetime(int(year_till), int(mon_till), int(day_till))
    till_ts = date_to.timestamp()

    for rec in default_list:
        if int(rec['likes']['count']) + int(rec['comments']['count']) > 0 and from_ts <= rec['date'] <= till_ts:
            required = {'id': rec['id'], 'likes': rec['likes']['count'], 'comments': rec['comments']['count']}
            active_list.append(required)
    print(f'{len(active_list)=}')
    return active_list


class Selector:
    api = None
    group_id = 'club128629560'
    group_digit = '-128629560'
    domain = 'petr_fevronya_penza'
    members = {}
    members_count = 0
    post_list = []

    def __init__(self):
        # vk_api_token = "cbfc5973733d86a6024136f9b0adadf77ac0e188e91d8cd1b9d38dd8327d89e551e7e626029062ae9a20d"
        vk_api_token = "f5fb7becf5fb7becf5fb7bece4f589f7fcff5fbf5fb7becab1b8692e9887b40c93c8172"
        session = vk.Session(access_token=vk_api_token)
        self.api = vk.API(session)

        self.members_count = self.count_members()
        self.create_dict_members()
        raw_list = self.walk_by_posts()
        # Remove posts with no likes and comments
        self.post_list = get_liked_posts(raw_list)
        print(f"Work complete. List of all posts contains {len(self.post_list)}")

    # Quantity of all posts on the wall
    def count_wall_posts(self):
        posts = self.api.wall.get(
            domain=self.domain,
            count=1,
            v=5.107
        )
        return posts['count']

    # Number of all members
    def count_members(self) -> int:
        return int(
            self.api.groups.getMembers(
                group_id=self.group_id[4:],
                count=1,
                v=5.107
            )['count']
        )

    # Get all posts to a raw list
    def walk_by_posts(self):
        list_post = []
        posts_total = posts_left = self.count_wall_posts()
        offset = 0
        while posts_left > 100:
            list_post += self.api.wall.get(
                domain=self.domain,
                count=100,
                offset=offset,
                v=5.107
            )['items']
            offset += 101
            posts_left -= 100
            print(f"Obtaining posts from VK... {posts_left} of {posts_total} left")
        return list_post

    # Returns a list of users who liked the post with 'post_id'
    def get_users_who_liked(self, post_id):
        users_list = self.api.likes.getList(
            type='post',
            item_id=post_id,
            owner_id=self.group_digit,
            count=1000,
            v=5.107
        )
        return users_list['items']

    # Picks all members of a certain group and puts 'em into a dictionary
    # {member_id : {name: 'Ivan Ivanov', likes: 0, comments: 0} }
    def create_dict_members(self):
        raw_list = []
        counter = self.members_count
        print(f"Put all {counter} members into a dictionary")
        offset = 0
        while counter > 1000:
            iter_list = self.api.groups.getMembers(
                group_id=self.group_id[4:],
                count=1000,
                offset=offset,
                fields='first_name, last_name',
                v=5.107
            )
            offset += 1001
            counter -= 1000
            raw_list += iter_list['items']
        else:
            raw_list = self.api.groups.getMembers(
                group_id=self.group_id[4:],
                count=1000,
                fields='first_name, last_name',
                v=5.107
            )['items']
        # dictionary
        for user in raw_list:
            if user['first_name'] != 'DELETED':
                self.members[user['id']] = {
                    'name': f"{user['first_name']} {user['last_name']}",
                    'likes': 0,
                    'comments': 0
                }
        print(f'{len(self.members)=}')
        return self.members

    # Adds value of likes to a dictionary
    def count_likes(self):
        for post in self.post_list:
            likers_list = self.get_users_who_liked(post_id=post['id'])
            for liker in likers_list:
                member = self.members.get(liker)
                if member is not None:
                    member['likes'] += 1


if __name__ == '__main__':
    sel = Selector()
    sel.count_likes()
    likers = []
    for x in sel.members:
        mem = sel.members.get(x)
        if mem['likes'] > 0:
            print(f"{mem['name']} {mem['likes']}")
            likers.append(mem['name'])
    print(f"{len(likers)=}")
    winner_id = random.randint(0, len(likers))
    print(f"The winner is {likers[winner_id]}")
