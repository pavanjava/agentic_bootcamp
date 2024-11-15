from dotenv import load_dotenv, find_dotenv
from social_media.linkedin_operations import linkedin_main
from dev_actions.devops_tools import terraform_main, kubernetes_main
import logging
import os

load_dotenv(find_dotenv())

logging.basicConfig(level=int(os.environ['INFO']))
logger = logging.getLogger(__name__)


def post_to_linkedin(content: str) -> str:
    """This tool is used to publish content to LinkedIn"""
    return linkedin_main(content=content)


def burn_story_in_jira(no_of_hours: str) -> str:
    """This tool is used to burn some story points in jira task"""
    return f"task updated"


def create_terraform_code(content: str) -> str:
    """This tool is used to save the terraform code"""
    return terraform_main(content=content)


def create_k8s_code(content: str) -> str:
    """This tool is used to save the kubernetes config code"""
    return kubernetes_main(content=content)
