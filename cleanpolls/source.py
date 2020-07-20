import vk


class PollsCleaner:
    api: vk.API = None
    group_digit = '-197234531'
    group_id = 'club197234531'

    def __init__(self):
        vk_api_token = "f5fb7becf5fb7becf5fb7bece4f589f7fcff5fbf5fb7becab1b8692e9887b40c93c8172"
        session = vk.Session(access_token=vk_api_token)
        self.api = vk.API(session)

    def get_poll(self):
        top_wall_posts = self.api.wall.get(
            owner_id=self.group_digit,
            offset=0,
            count=5,
            v='5.120'
        )
        for item in top_wall_posts['items']:
            if "attachments" in item.keys() and item["attachments"][0]["type"] == "poll":
                poll_dict = (item["attachments"][0]["poll"])
                print(f'owner id: {poll_dict["owner_id"]}')
                print(f'poll id: {poll_dict["id"]}')
                answers_ids_list = []
                print(poll_dict['answers'])
                for answer in poll_dict['answers']:
                    answers_ids_list.append(answer['id'])

                voters = self.api.polls.getVoters(
                    owner_id=poll_dict["owner_id"],
                    poll_id=poll_dict["id"],
                    answers_ids=answers_ids_list,
                    v='5.120'
                )
                print(voters)


poll = PollsCleaner()
poll.get_poll()

# TODO https://vk.com/dev/implicit_flow_user
