import yaml


def load_yaml(file_path: str):
    with open(file_path, 'r') as f:
        yaml_dict = yaml.load(f, Loader=yaml.FullLoader)
    return yaml_dict


