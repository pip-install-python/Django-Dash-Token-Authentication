from ninja import Router
from account.models import Profile
import os
# Create your views here.
router = Router()


@router.post("/login")
def login_user(request, username: str = Form(...), password: str = Form(...)):
    print('login_user /login')
    print(f'request: {request}')
    print(f'username: {username}')
    print(f'password: {password}')
    user = auth_authenticate(username=username, password=password)
    central_time = pytz.timezone('US/Central')
    current_time = datetime.now(central_time)
    current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    if user is not None:
        login(request, user)
        request.content_params = {'Success': f"Logged in: {user.username} at {current_time}"}
        return {'username': username, 'email': user.email, 'logged_in': True, 'time_logged_in': current_time,}
    else:
        user = User.objects.get(email=username)
        if user:
            user = auth_authenticate(username=user.username, password=password)
            login(request, user)
            return {'username': username, 'email': user.email, 'logged_in': True, 'time_logged_in': current_time,}
        else:
            request.content_params = {'Error': f'User Doesn\'t Exist'}
            return {'Error': f'User Doesn\'t Exist'}


@router.post("/register")
def register(request, username: str = Form(...), email: str = Form(...), password: str = Form(...),
             password_checker: str = Form(...), birthday: str = Form(...), theme: str = Form(...), about: str = Form(...), avatar: str = Form(...)):
    # Request all Users on Application
    users = User.objects.all()
    # check username vs user in database
    user_in_users = users.values_list('username', flat=True)
    # print('user_in_users', list(user_in_users))

    emails = users.values_list('email', flat=True)

    email_checker = validate_email(email)
    print('Testing email_checker')
    print(email_checker)

    if username in list(user_in_users):
        print('Username already taken')
        return {'Username': 'already taken'}
    elif email in list(emails):
        print('Email already taken')
        return {'Email': 'already taken'}
    elif validate_email(email):
        if password == password_checker:
            print('Passwords match')
            user = User.objects.create_user(username, email, password)
            user.save()
            print(user)
            login(request, user)
            profile_url_location = username.replace(' ', '-')
            Profile.objects.create(
                user=user,
                avatar=avatar,
                url=f'www.pipinstallpython.com/{profile_url_location}',
                description=about,
                donation_link='AddDonationLink.com',
                youtube_link='AddYoutubeLink.com',
                reddit_link='AddRedditLink.com',
                github_link='AddGithubLink.com',
                discord_link='AddDiscordLink.com',
                snapchat_link='AddSnapchatLink.com',
                dm_link='AddDirectMessageLink.com',
                website_link='AddWebsiteLink.com',
                theme=theme,
                birthday=birthday,

                credits=5
            )
            return {'message': 'User Created'}
        else:
            print('Passwords don\'t match')
            return {'Passwords': 'Do Not Match'}
    else:
        print('Email not valid')
        return {'Email': 'not valid'}


@router.get("/account")
def account_info(request, username: str):
    print('requesting account info on:', username)
    # Request all Users on Application
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    print(profile.__dict__)

    context = {
        'email': user.email,
        'avatar': str(profile.avatar),
        'url': profile.url,
        'description': profile.description,
        'donation_link': profile.donation_link,
        'youtube_link': profile.youtube_link,
        'discord_link': profile.discord_link,
        'reddit_link': profile.reddit_link,
        'github_link': profile.github_link,
        'snapchat_link': profile.snapchat_link,
        'dm_link': profile.dm_link,
        'website_link': profile.website_link,
        'credits': profile.credits,
        'qr_image': str(profile.qr_image),
        'theme': profile.theme,
        'birthday': profile.birthday,
        'lat': profile.lat,
        'lon': profile.lon
    }
    # context_data = json.dumps(context)
    # # Access all fields
    # for field in profile._meta.get_fields():
    #     print(getattr(profile, field.name))
    return context

def avatar_upload_to(instance, filename):
    # Get the username of the user
    username = instance.user.username
    # Use the username to create a folder in the avatars folder
    folder = f'avatars/{username}'
    # Return the path to the avatar image
    return os.path.join(folder, filename)

@router.post('/account_update')
def account_update(request, username: str = Form(...), email: str = Form(...), avatar: str = Form(...), description: str = Form(...), donation_link: str = Form(...), youtube_link: str = Form(...), discord_link: str = Form(...), reddit_link: str = Form(...), github_link: str = Form(...), snapchat_link: str = Form(...), dm_link: str = Form(...), website_link: str = Form(...), theme: str = Form(...),  ):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)

    user.email = email

    profile.avatar = avatar

    profile.description = description

    profile.website_link = website_link

    profile.github_link = github_link

    profile.reddit_link = reddit_link

    profile.donation_link = donation_link

    profile.youtube_link = youtube_link

    profile.snapchat_link = snapchat_link

    profile.dm_link = dm_link

    profile.discord_link = discord_link

    profile.theme = theme
    user.save()
    profile.save()

    context = {
        'email': user.email,
        'avatar': str(profile.avatar),
        'url': profile.url,
        'description': profile.description,
        'donation_link': profile.donation_link,
        'youtube_link': profile.youtube_link,
        'discord_link': profile.discord_link,
        'reddit_link': profile.reddit_link,
        'github_link': profile.github_link,
        'snapchat_link': profile.snapchat_link,
        'dm_link': profile.dm_link,
        'website_link': profile.website_link,
        'credits': profile.credits,
        'qr_image': str(profile.qr_image),
        'theme': profile.theme,
        'birthday': profile.birthday,
        'lat': profile.lat,
        'lon': profile.lon
    }

    return context


@router.post("/account_location")
def account_location(request, account: str, lat:  str = Form(...), lon:  str = Form(...)):
    if not all([account, lat, lon]):
        return {"error": "Account, lat and lon are required fields."}
    # Perform actions with the received data
    user = User.objects.get(username=str(account))

    profile = Profile.objects.get(user=user)

    profile.lat = float(lat)
    profile.lon = float(lon)
    profile.save()
    return {"message": "Location added successfully."}


if __name__ == '__main__':
    print('testing')