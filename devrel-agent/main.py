from llama_deploy import LlamaDeployClient, ControlPlaneConfig
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

# points to deployed control plane
client = LlamaDeployClient(ControlPlaneConfig())

while True:
    system_prompt = input("Enter system query (or 'bye'/'exit' to quit): ")
    user_query = input("Enter your query (or 'bye'/'exit' to quit): ")

    # Check for exit conditions
    if user_query.lower() in ['bye', 'exit']:
        print("Goodbye!")
        break

    session = client.create_session()
    result3 = session.run(service_name=os.environ.get('WORKFLOW_SERVICE_NAME'), input=user_query,
                          system_prompt=system_prompt)
    # print(f'response from react_workflow is {result3}')
