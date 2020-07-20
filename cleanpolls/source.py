import vk


class PollsCleaner:
    api: vk.API = None
    group_digit = '-197234531'
    group_id = 'club197234531'

    def __init__(self):
        # vk_api_token = "f5fb7becf5fb7becf5fb7bece4f589f7fcff5fbf5fb7becab1b8692e9887b40c93c8172"
        # another token
        vk_token = 'f0a8ce42acc97e4af4a8dbd76f3ec99fcafa851eafd8dde0e99a17954fb86340d06fc019d7b4cd0e82ce8'

        # session = vk.Session(access_token=vk_api_token)
        session = vk.Session(access_token=vk_token)
        self.api = vk.API(session)

    def check_poll(self):
        votes = []
        answer_ids_dict = {}
        top_wall_posts = self.api.wall.get(
            owner_id=self.group_digit,
            offset=0,
            count=5,
            v='5.120'
        )
        for item in top_wall_posts['items']:
            if "attachments" in item.keys() and item["attachments"][0]["type"] == "poll":
                poll_dict = (item["attachments"][0]["poll"])
                for answer in poll_dict['answers']:
                    answer_ids_dict[str(answer['id'])] = answer['text']
                votes = self.api.polls.getVoters(
                    owner_id=poll_dict["owner_id"],
                    poll_id=poll_dict["id"],
                    fields='online',
                    answer_ids=", ".join(answer_ids_dict.keys()),
                    v='5.120'
                )
        votes_count_dict = {}
        for v in votes:
            # text = answer_ids_dict[str(v['answer_id'])]
            person_names = [f"{x['first_name']} {x['last_name']}" for x in v['users']['items']]
            person_ids = [x['id'] for x in v['users']['items']]
            # print(f"{v['answer_id']} (\"{text}\"): {len(v['users']['items'])} votes by")
            # print(", ".join(person_names))
        #
            for i, person in enumerate(person_names):
                if person not in votes_count_dict.keys():
                    votes_count_dict[person] = {'id': person_ids[i], 'votes': 1}
                else:
                    votes_count_dict[person]['votes'] = votes_count_dict[person]['votes'] + 1
        print(votes_count_dict)
        print(len(votes))

        for key, user in votes_count_dict.items():
            if user['votes'] > (len(votes) / 2):
                print(f"Remove votes by {key} with id={user['id']} - more than half")
            elif user['votes'] < 3:
                print(f"Remove votes by {key} with id={user['id']} - less than minimum")


poll = PollsCleaner()
poll.check_poll()

# TODO https://vk.com/dev/implicit_flow_user
# https://oauth.vk.com/authorize?client_id=7545029&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=wall&response_type=token&v=5.120&state=123456
