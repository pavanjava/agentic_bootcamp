import webbrowser
from urllib.parse import parse_qs, urlparse
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

def get_linkedin_auth():
    # LinkedIn OAuth URL parameters
    CLIENT_ID = os.environ.get("CLIENT_ID")
    REDIRECT_URI = "https://www.linkedin.com/developers/tools/oauth/redirect"
    STATE = "1234567890"
    SCOPE = "openid email w_member_social profile"

    # Construct authorization URL
    auth_url = (
        "https://www.linkedin.com/oauth/v2/authorization?"
        f"response_type=code&"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"state={STATE}&"
        f"scope={SCOPE}"
    )

    # Open the authorization URL in browser
    print("\nOpening LinkedIn authorization page in your browser...")
    webbrowser.open(auth_url)

    # Ask user to paste the redirect URL
    print("\nAfter authorizing, you will be redirected to a new URL.")
    print("Please copy and paste the complete redirect URL here:")
    redirect_url = input().strip()

    try:
        # Parse the URL to extract the authorization code
        parsed_url = urlparse(redirect_url)
        query_params = parse_qs(parsed_url.query)

        # Extract authorization code
        auth_code = query_params.get('code', [None])[0]

        if auth_code:
            print("\nAuthorization Code Successfully Retrieved!")
            print("\nYour authorization code is:")
            print("-" * 50)
            print(auth_code)
            print("-" * 50)
            return auth_code
        else:
            print("\nError: No authorization code found in the URL.")
            return None

    except Exception as e:
        print(f"\nError parsing the URL: {str(e)}")
        return None


if __name__ == "__main__":
    get_linkedin_auth()
