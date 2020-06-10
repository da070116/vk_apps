import vk


class Selector:
    api = None
    group_id = 'club128629560'
    group_digit = '-128629560'
    domain = 'petr_fevronya_penza'
    users = {}

    def __init__(self):
        # vk_api_token = "cbfc5973733d86a6024136f9b0adadf77ac0e188e91d8cd1b9d38dd8327d89e551e7e626029062ae9a20d"
        vk_api_token = "f5fb7becf5fb7becf5fb7bece4f589f7fcff5fbf5fb7becab1b8692e9887b40c93c8172"
        session = vk.Session(access_token=vk_api_token)
        self.api = vk.API(session)
        print(self.api.getInfo())

    def about(self):
        about_str = self.api.groups.getById(group_id=self.group_id, fields="description", v=5.21)
        print(about_str[0]['name'])

    def count_wall_posts(self):
        posts = self.api.wall.get(domain=self.domain, count=1, v=5.107)
        print(posts['count'])

    def get_posts(self, limit=5):
        list_post = self.api.wall.get(domain=self.domain, count=limit, v=5.107)['items']
        for rec in list_post:
            print(rec)
            pid = rec['id']
            title = rec['text'][0: 40]
            likes = rec['likes']['count']
            reposts = rec['reposts']['count']
            comments = rec['comments']['count']
            print(f'Post #{pid}: "{title}" has {likes} like(s), {comments} comment(s) and {reposts} repost(s)')
            print("Likes are from: ")
            self.get_users_by_likes(pid)

    def get_users_by_likes(self, post_id):
        users_list = self.api.likes.getList(type='post', item_id=post_id, owner_id=self.group_digit,
                                            count=1000, v=5.107)
        print(users_list)

    def add_user(self):
        raw_userlist = self.api.groups.getMembers(group_id= self.group_id[4:], count=1000,
                                                  fields='first_name, last_name',  v=5.107)['items']
        for user in raw_userlist:

            if 'deactivated' not in user.keys():
                print(f"User[{user['id']}]: {user['first_name']} {user['last_name']}")




# get list users from likes
# https://vk.com/dev/likes.getList?params[type]=post&params[owner_id]=-128629560&params[item_id]=3205&params[filter]=likes&params[friends_only]=0&params[extended]=0&params[offset]=1&params[count]=1000&params[skip_own]=1&params[v]=5.107


if __name__ == '__main__':
    sel = Selector()
    sel.about()
    sel.add_user()
  #  sel.count_wall_posts()
  #  (sel.get_posts())
