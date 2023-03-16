import logging


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def read_data_from_file(filename: str) -> list[str]:
    with open(filename, "r") as _file:
        content = _file.read().splitlines()
        return [record for record in content]


def write_to_file(filename, record: str):
    try:
        with open(filename, "a") as _file:
            _file.write(record + "\n")
    except Exception as e:
        logging.error(
            f"Error while writing to file: {e}\nCould not write record: {record} to {filename}\n")
