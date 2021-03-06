from roblox_studio import StudioClient


def main():
    studio_client = StudioClient()
    app_storage = studio_client.get_app_storage()
    print("Username:", app_storage.username)
    print("Display Name:", app_storage.display_name)
    print("User ID:", app_storage.user_id)


if __name__ == "__main__":
    main()
