import os


def execute_command(command: str) -> [None, str]:
    """
    Executes command

    Args:
        command (str): command to be executed

    Returns:
        [None, str]: output
    """

    return os.popen(command).read()
