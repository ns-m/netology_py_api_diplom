import requests
import json

class VkApiWork:


    version = 5.89
    access_token = "2a0545aa68a19df8fb37eb969049ac8c06e0f80191a7608cb539ea6bb017b01296311ece43998aee0a577"
    vk = 'https://api.vk.com/method/'

    def vk_params(self, version, access_token, vk):
        self.version = version
        self.access_token = access_token
        self.vk = vk


    def get_api_data(self, method, params):
        api_link = f'{self.vk}{method}'
        count = 1
        while True:
            response = requests.get(api_link, params=params)
            response.raise_for_status()
            response = response.json()
            print('*'*count)
            count += 1
            if 'response' in response:
                return response['response']['items']
            return response

    def get_user_friends(self, common_params):
        while True:
            user_id = input('Enter user id for analysis: ')
            params = {
                'user_id': user_id,
                'fields': 'name'
                }
            params.update(common_params)

            friends = self.get_api_data('friends.get', params)
            if 'error' in friends:
                print('User is not found. Repeat Entry')
                continue
            else:
                break
        right_friends = [friend for friend in friends if 'deactivated' not in friend]
        right_friends2 = [friend for friend in right_friends if friend['can_access_closed'] == True]
        return user_id, right_friends2

    def get_groups(self, user_id, common_params):
        params = {
            'user_id': user_id,
            'count': 1000,
            'extended': 1,
            'fields': 'members_count'
            }
        params.update(common_params)
        groups = self.get_api_data('groups.get', params)
        return groups

