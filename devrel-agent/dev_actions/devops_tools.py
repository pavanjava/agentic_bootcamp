class TerraformTools:
    def __init__(self):
        pass

    def create_terraform_file(self, content: str):
        with open('terraform.tf', mode='w') as file:
            file.write(content)


class KubernetesTools:
    def __init__(self):
        pass

    def create_kubernetes_file(self, content: str):
        with open('k8s_config.yml', mode='w') as file:
            file.write(content)


def terraform_main(content: str):
    tf_tools = TerraformTools()
    tf_tools.create_terraform_file(content=content)


def kubernetes_main(content: str):
    k8s_tools = KubernetesTools()
    k8s_tools.create_kubernetes_file(content=content)
