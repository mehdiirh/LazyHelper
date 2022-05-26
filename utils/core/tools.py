import os
import subprocess
import tempfile


def execute_command(command: str) -> [None, str]:
    """
    Executes command

    Args:
        command (str): command to be executed

    Returns:
        [None, str]: output
    """

    return os.popen(command).read()


def copy_content_to_clipboard(content):
    """
    Copy content to clipboard

    Args:
        content (str): content to be copied

    Returns:
        bool: True if content is copied
    """

    content = str(content)
    with tempfile.NamedTemporaryFile(mode='w+t') as f:
        f.write(content)
        f.flush()
        return_code = subprocess.call(
            ['xclip', '-d', ':0', '-selection', 'clipboard', f.name],
            stdout=subprocess.PIPE,
        )

        status = True if return_code == 0 else False
        return status


def linux_package_installed(package_name: str) -> bool:
    """
    Check if a linux package is installed

    Args:
        package_name (str): package name

    Returns:
        bool: True if package is installed
    """

    return_code = subprocess.call(
        ['which', package_name],
        stdout=subprocess.PIPE,
    )

    status = True if return_code == 0 else False
    return status
