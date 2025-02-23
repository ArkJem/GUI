import yaml

def read_yaml(property_name):
    with open('./config.yml', 'r') as read_config:
        content = yaml.safe_load(read_config)
        if property_name in content:
            return content[property_name]
        else:
            return None


def edit_yaml(property_name, new_value, file_path='./config.yml'):
    try:
        with open(file_path, 'r') as read_config:
            content = yaml.safe_load(read_config) or {}

        if not isinstance(content, dict):
            print("Błąd: Plik YAML nie zawiera poprawnej struktury.")
            return

        if property_name in content:
            content[property_name] = new_value
        else:
            print(f"Właściwość '{property_name}' nie została znaleziona w pliku YAML. Tworzenie nowej właściwości.")
            content[property_name] = new_value

        with open(file_path, 'w') as write_config:
            yaml.safe_dump(content, write_config)

        print(f"Właściwość '{property_name}' została zaktualizowana na wartość '{new_value}'.")

    except yaml.YAMLError as e:
        print("Błąd parsowania pliku YAML:", e)
    except FileNotFoundError:
        print("Błąd: Plik YAML nie został znaleziony.")
    except Exception as e:
        print("Wystąpił nieoczekiwany błąd:", e)


