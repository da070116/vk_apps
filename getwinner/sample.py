import vk


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
        self.get_all_users()
        self.post_list = self.walk_by_posts()
        # Remove posts with no likes and comments
        self.post_list = self.filter_active_posts()
        print(f"Work complete. List of all posts contains {len(self.post_list)}")

    def about(self):
        about_str = self.api.groups.getById(
            group_id=self.group_id,
            fields="description",
            v=5.21
        )
        return about_str[0]['name']

    def count_wall_posts(self):
        posts = self.api.wall.get(
            domain=self.domain,
            count=1,
            v=5.107
        )
        return posts['count']

    def count_members(self):
        return self.api.groups.getMembers(
            group_id=self.group_id[4:],
            count=1,
            v=5.107
        )['count']

    def walk_by_posts(self):
        list_post = []
        posts_left = self.count_wall_posts()
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
            print(f"Obtaining posts from VK... {posts_left} left")
        return list_post

    def filter_active_posts(self):
        active_list = []
        for rec in self.post_list:
          #  if int(rec['likes']['count']) + int(rec['comments']['count']) > 0:
            if int(rec['likes']['count']) > 0:    # считать только лайки
                active_list.append(rec)
        return active_list

    def get_users_who_liked(self, post_id):
        users_list = self.api.likes.getList(
            type='post',
            item_id=post_id,
            owner_id=self.group_digit,
            count=1000,
            v=5.107
        )
        return users_list['items']

    def get_all_users(self):
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

        for user in raw_list:
            self.members[user['id']] = {
                'name': f"{user['first_name']} {user['last_name']}",
                'likes': 0,
                'comments': 0
            }
        return

    def count_likes(self):
        for post in self.post_list:
            liked_by = self.get_users_who_liked(post_id=post['id'])
            print(f'{post["id"]=} {liked_by=}')


if __name__ == '__main__':
    sel = Selector()
    # print(sel.members)
  #  sel.count_likes()

    for x in sel.post_list:
        print(x)