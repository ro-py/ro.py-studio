from roblox_studio import StudioClient


def main():
    studio_client = StudioClient()
    cookies = studio_client.get_cookies()
    for url, url_cookies in cookies.items():
        print(url)
        for cookie_name, cookie in url_cookies.items():
            print(f"\t{cookie_name}: {cookie}")


if __name__ == "__main__":
    main()
