import requests
import colorama


def login(username, password):
    print(colorama.Fore.GREEN + f'Testing Login: username: {username}, password: {password}'+ colorama.Fore.RESET)
    url_login = f'http://127.0.0.1:8000/api/account/login'

    response = requests.post(url_login, data={'username': username, 'password': password})
    print(response.json())
    if response.status_code == 200:

        if response.json() == {'Error': "User Doesn't Exist"}:
            print(colorama.Fore.RED + f"Login Failed: {username}", colorama.Fore.RESET)
            return False
        print(colorama.Fore.GREEN + f"Login Successful: {response.json()}")
        print(colorama.Fore.YELLOW + f'{response.headers}')

        print(colorama.Fore.RESET)
        print(response.json())
        return response.json()
    else:
        print(colorama.Fore.RED + f"Login Failed: {username}")
        print(colorama.Fore.RESET)
        return False


def register(username, email, password, password_checker, birthday, theme, about, avatar):
    # print('Testing Register')
    url_register = 'http://127.0.0.1:8000/api/account/register'

    print(f'register(username: {username}, email: {email}, password: {password}, password_checker: {password_checker}, birthday: {birthday}, theme: {theme}, about: {about}, avatar: {avatar}):')

    response = requests.post(url_register, data={'username': username, 'email': email, 'password': password, 'password_checker': password_checker, 'birthday': birthday, 'theme': theme, 'about': about, 'avatar': avatar})

    if response.json() == {'message': 'User Created'}:
        print(colorama.Fore.GREEN + f"Registration Successful for {username}:", f"{response.json()}")
        print(colorama.Fore.RESET)
        return response.json()
    else:
        print(colorama.Fore.RED + f"Registration Failed for {username}:", f"{response.json()}")
        print(colorama.Fore.RESET)
        return False


def create_user_token(username, password):

    url_login = f'http://127.0.0.1:8000/api/token/pair'

    print(f'create_user_token(username: {username}, password: {password}):')

    curl_body = {
        'password': password,
        'username': username
    }

    response = requests.post(url_login, json=curl_body)
    if response.status_code == 200:
        print(colorama.Fore.GREEN + f"Login Successful: {response.status_code}", colorama.Fore.RESET)
    else:
        print(colorama.Fore.RED + f"Login Failed: {username}", colorama.Fore.RESET)

    print('headers')
    print(response.headers)
    print('response')
    print(response.json())
    return response.json()


def refresh_user_token(refresh_token):
    refresh_token_url = f'http://127.0.0.1:8000/api/token/refresh'

    print(f'refresh_user_token({refresh_token}):')

    curl_body = {
        'refresh': refresh_token
    }

    response = requests.post(refresh_token_url, json=curl_body)
    if response.status_code == 200:
        print(colorama.Fore.GREEN + f"Login Successful: {response.status_code}", colorama.Fore.RESET)
    else:
        print(colorama.Fore.RED + f"Login Failed: {response.status_code}", colorama.Fore.RESET)
    print('headers')
    print(response.headers)
    print('access_token')
    print(response.json())
    return response.json()


def verify_user_token(access_token):
    print(f'verify_user_token({access_token}):')
    verify_token_url = f'http://127.0.0.1:8000/api/token/verify'

    curl_body = {
        'token': access_token
    }

    response = requests.post(verify_token_url, json=curl_body)

    if response.status_code == 200:
        print(colorama.Fore.GREEN + f"Login Successful: {response.status_code}", colorama.Fore.RESET)
    else:
        print(colorama.Fore.RED + f"Login Failed: {response.status_code}: {response}", colorama.Fore.RESET)

    print('headers')
    print(response.headers)
    print('access_token')

    if response.json() == {}:
        return True
    else:
        return False

def get_user_info(username):
    print(f'get_user_info({username}):')
    url_user_info = f'http://127.0.0.1:8000/api/account/account?username={username}'

    response = requests.get(url_user_info)
    print(response)
    return response.json()


def account_location(account:str, lat:float, lon:float):
    url_account_location = f'http://127.0.0.1:8000/api/account/account_location?account={account}'

    print(f'account_location(account:{account}, lat:{lat}, lon:{lon}):')
    print(account)
    print(f'lat:{lat}, lon: {lon}')
    print()
    response=requests.post(url_account_location, data={'lat':lat, 'lon':lon})

    return response.json()


def update_account(username, email, avatar, description, donation, youtube, discord, reddit, github, snapchat, dm,
                   website, theme):
    print(f'update_account(username: {username}, email: {email}, avatar: {avatar}, description: {description}, donation: {donation}, youtube: {youtube}, discord: {discord}, reddit: {reddit}, github: {github}, snapchat:{snapchat}, dm: {dm}, website: {website}, theme:{theme}):')

    url_account_update = f'http://127.0.0.1:8000/api/account/account_update'

    response = requests.post(url_account_update, data={'username': username, 'email': email, 'avatar': avatar, 'description': description, 'donation_link':donation, 'youtube_link': youtube, 'discord_link': discord, 'reddit_link':reddit, 'github_link':github, 'snapchat_link': snapchat, 'dm_link': dm,
                                                       'website_link': website, 'theme': theme})

    return response.json()

if __name__ == '__main__':
    print('Testing')
