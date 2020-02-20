import time
import requests
import json

version = 5.8
access_token = "2a0545aa68a19df8fb37eb969049ac8c06e0f80191a7608cb539ea6bb017b01296311ece43998aee0a577"

API_VK = 'https://api.vk.com/method/'
ERROR_TOO_MANY_REQUESTS = 6


# сделать запрос к API
def get_api_data(method, params):
    api_link = '{}{}'.format(API_VK, method)
    while True:
        response = requests.get(api_link, params=params)
        response.raise_for_status()
        response = response.json()
        print('*')
        if 'response' in response:
            return response['response']['items']
        else:
            error = response['error']['error_code']
            if error == ERROR_TOO_MANY_REQUESTS:
                time.sleep(3)
                continue
            else:
                return response


# получить группы
def get_groups(user_id, common_params):
    params = {
        'user_id': user_id,
        'count': 1000,
        'extended': 1,
        'fields': 'members_count'
        }
    params.update(common_params)
    groups = get_api_data('groups.get', params)
    return groups


# получить друзей
def get_user_friends(common_params):
    while True:
        user_id = input('Введите id пользователя для анализа: ')
        params = {
            'user_id': user_id,
            'fields': 'name'
            }
        params.update(common_params)

        friends = get_api_data('friends.get', params)
        if 'error' in friends:
            print('Пользователь не найден. Повторите ввод')
            continue
        else:
            break
    # выбираем только неудаленных друзей
    valid_friends = [fr for fr in friends if 'deactivated' not in fr]
    return user_id, valid_friends


def read_json_file(filename):
    with open(filename, encoding='utf-8') as data_file:
        data = json.load(data_file)
    return data


def write_json_data(filename, text):
    with open(filename, mode='w', encoding='utf-8') as file:
        file.write(text)


def main():

    params = {
        'access_token': access_token,
        'v': version
        }

    user_id, friends = get_user_friends(params)
    groups = get_groups(user_id, params)

    # составляем список из словарей, каждый из которых - данные о друге
    my_groups = [(gr['id'], gr['name']) for gr in groups]

    friend_groups_overall = set()
    len_friends = len(friends)
    # проходимся по id valid_friends и для каждого делаем запрос групп, объединяем это в один ses
    for i, friend in enumerate(friends):
        print('{} из {} пользователей'.format(i, len_friends))
        print('Обработка групп пользователя {} {}'.format(friend['first_name'], friend['last_name']))
        friend_groups_json = get_groups(friend['id'], params)
        friend_groups_list = [(gr['id'], gr['name']) for gr in friend_groups_json]
        friend_groups_overall = friend_groups_overall.union(friend_groups_list)

    result_set = set(my_groups).difference(friend_groups_overall)

    # преобразуем итог в список с id
    result_groups_ids = [group_id for group_id, name in result_set]
    # для финального результата собираем список словарей с полями 'id', 'name', 'members_count'
    result_groups_json = []
    for gr in groups:
        if gr['id'] in result_groups_ids:
            result_groups_json.append({k: v for k, v in gr.items() if (k in ('id', 'name', 'members_count'))})
    # пишем json в файл
    write_json_data('groups_of_friends.json', str(result_groups_json))
    print('Обработано успешно, результат сохранен в файле groups_of_friends.json')


if __name__ == "__main__":
    main()
