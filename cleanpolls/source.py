import vk


class PollsCleaner:
    api = None

    group_digit = '-194461736'
    group_id = 'club194461736'

    def __init__(self):
        vk_api_token = "f5fb7becf5fb7becf5fb7bece4f589f7fcff5fbf5fb7becab1b8692e9887b40c93c8172"
        session = vk.Session(access_token=vk_api_token)
        self.api = vk.API(session)
        top_wall_posts = self.api.wall.get(
            owner_id=self.group_digit,
            offset=1,
            count=5,
            v='5.120'
        )
        for item in top_wall_posts['items']:
            if "attachments" in item.keys() and item["attachments"][0]["type"] == "poll":
                poll_dict = (item["attachments"][0]["poll"])
                print(f'{poll_dict=} \n')


poll = PollsCleaner()
