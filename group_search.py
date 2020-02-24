from class_for_search import VkApiWork
import time


data_from_api = VkApiWork()

def main():

    params = {
        'access_token': data_from_api.access_token,
        'v': data_from_api.version
        }

    user_id, friends = data_from_api.get_user_friends(params)
    groups = data_from_api.get_groups(user_id, params)
    my_groups = [(group['id'], group['name']) for group in groups]

    friend_groups_overall = set()
    len_friends = len(friends)

    for i, friend in enumerate(friends):
        print(f'{i+1} from {len_friends} friends')
        print(f'User Group processing {friend["first_name"]} {friend["last_name"]}')
        friend_groups_json = data_from_api.get_groups(friend['id'], params)
        try:
            friend_groups_list = [(group['id'], group['name']) for group in friend_groups_json]
        except:
            time.sleep(3)
            continue
        friend_groups_overall = friend_groups_overall.union(friend_groups_list)


    result_set = set(my_groups).difference(friend_groups_overall)


    def write_json_data(filename, text):
        with open(filename, mode='w', encoding='utf-8') as file:
            file.write(text)

    result_groups_ids = [group_id for group_id, name in result_set]
    result_groups_json = []
    for group in groups:
        if group['id'] in result_groups_ids:
            result_groups_json.append({k: v for k, v in group.items() if (k in ('id', 'name', 'members_count'))})
    write_json_data('groups.json', str(result_groups_json))
    print('Processed successfully, the result is saved in a file groups.json')

if __name__ == "__main__":
    main()
