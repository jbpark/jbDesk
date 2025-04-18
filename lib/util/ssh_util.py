import logging

import paramiko

from lib.util.encoding_util import decrypt_cipher_text

# logging.basicConfig(level=logging.DEBUG)

def get_ssh_user_info(ssh_user_infos, host_ip, first_index, check_sudo=True):
    attempts = 0  # Counter for keeping track of attempts

    sorted_infos = sorted(ssh_user_infos, key=lambda x: (x.index != first_index, x.index))

    for ssh_connect_info in sorted_infos:
        user_name = ssh_connect_info.user_name
        password = decrypt_cipher_text(ssh_connect_info.password)
        print(f"Attempting attempts:{attempts}, index:{ssh_connect_info.index}")

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            client.connect(host_ip, username=user_name, password=password, timeout=2)
            print(f"[>] Valid password found index:{ssh_connect_info.index}")
            client.close()
            return ssh_connect_info
        except paramiko.AuthenticationException:
            print("Invalid password!")
        except Exception as e:
            print(f"Connection failed: {e}")
        finally:
            client.close()

        attempts += 1  # Increment the attempts counter for each password

    return None
