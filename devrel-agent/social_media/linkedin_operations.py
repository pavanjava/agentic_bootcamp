import requests
from typing import Dict, Any
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class LinkedInPostTool:
    def __init__(self, access_token: str):
        """
        Initialize LinkedIn Poster with OAuth access token.

        Args:
            access_token (str): LinkedIn OAuth 2.0 access token
        """
        self.access_token = access_token
        self.base_url = "https://api.linkedin.com/v2"
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }

    def get_profile_id(self) -> str:
        """Get authenticated user's profile ID."""
        url = f"{self.base_url}/userinfo"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()['sub']

    def create_text_post(self, text: str, visibility: str = "PUBLIC") -> Dict[str, Any]:
        """
        Create a text-only post on LinkedIn.

        Args:
            text (str): Content of the post
            visibility (str): Post visibility - 'PUBLIC' or 'CONNECTIONS'

        Returns:
            Dict containing the response from LinkedIn API
        """
        profile_id = self.get_profile_id()

        post_data = {
            "author": f"urn:li:person:{profile_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": visibility
            }
        }

        url = f"{self.base_url}/ugcPosts"
        response = requests.post(url, headers=self.headers, json=post_data)
        response.raise_for_status()
        return response.json()


def linkedin_main(content: str) -> str:
    # Load access token from environment variable
    access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
    if not access_token:
        raise ValueError("Please set LINKEDIN_ACCESS_TOKEN environment variable")

    # Initialize the LinkedIn poster
    poster = LinkedInPostTool(access_token)

    # Example usage
    try:
        # Create a text post
        text_post = poster.create_text_post(
            text=content
        )
        return "Text post created successfully!"

    except requests.exceptions.RequestException as e:
        print(f"Error creating post: {str(e)}")


# if __name__ == "__main__":
#     main(content="Exited to share using python code")
