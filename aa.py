import os
import subprocess

def scan_os_type():
    print("Вид операционной системы:")
    os_type = subprocess.run(["uname", "-a"], capture_output=True, text=True)
    print(os_type.stdout)

def scan_hostname():
    print("Имя узла:")
    hostname = subprocess.run(["hostname"], capture_output=True, text=True)
    print(hostname.stdout)

def check_security_updates():
    try:
        # Выполняем команду для обновления списка пакетов
        subprocess.run(['sudo', 'apt', 'update'], check=True)
        
        # Выполняем команду для получения списка обновлений
        result = subprocess.run(
            ['apt', 'list', '--upgradable'],
            check=True,
            capture_output=True,
            text=True
        )
        
        # Фильтруем только обновления безопасности
        updates = result.stdout.split('\n')
        security_updates = [update for update in updates if '/security' in update]

        if security_updates:
            print("Найдены следующие обновления безопасности:")
            for update in security_updates:
                print(update)
        else:
            print("Обновления безопасности не найдены.")
    
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды: {e}")

def scan_user_accounts():
    print("Данные учетных записей:")
    user_accounts = subprocess.run(["cat", "/etc/passwd"], capture_output=True, text=True)
    print(user_accounts.stdout)

def get_pass():
    users = []
    try:
        with open('/etc/passwd', 'r') as f:
            for line in f:
                parts = line.split(':')
                if int(parts[2]) >= 1000 and parts[6] != '/usr/sbin/nologin':
                    users.append(parts[0])
    except Exception as e:
        print(f"Ошибка при чтении /etc/passwd: {e}")
    return users

def get_password_policy(user):
    try:
        result = subprocess.run(
            ['sudo', 'chage', '-l', user],
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Ошибка при выполнении команды: {e}"
    except Exception as e:
        return f"Произошла ошибка: {e}"

# Получаем список всех пользователей
users = get_pass()

# Проверяем, удалось ли получить список пользователей
if not users:
    print("Не удалось получить список пользователей или в системе нет пользователей.")
else:
    # Для каждого пользователя выводим политику паролей
    for user in users:
        policy_info = get_password_policy(user)
        print(f"Политика паролей для пользователя {user}:\n{policy_info}\n")

def scan_registry_audit():
    print("Аудит реестра:")
    system_logs = subprocess.run(["journalctl", "-k"], capture_output=True, text=True)
    print(system_logs.stdout)


def scan_network_settings():
    print("Сетевые настройки:")
    network_settings = subprocess.run(["ip", "a"], capture_output=True, text=True)
    print(network_settings.stdout)

def scan_netbios_dns():
    print("NetBIOS и DNS:")
    netbios_dns = subprocess.run(["cat", "/etc/resolv.conf"], capture_output=True, text=True)
    print(netbios_dns.stdout)

def scan_running_services():
    print("Запущенные сервисы:")
    running_services = subprocess.run(["systemctl", "list-units", "--type=service"], capture_output=True, text=True)
    print(running_services.stdout)

def scan_filesystem():
    print("Файловая система:")
    filesystem = subprocess.run(["df", "-h"], capture_output=True, text=True)
    print(filesystem.stdout)

def get_all_users():
    users = []
    try:
        with open('/etc/passwd', 'r') as f:
            for line in f:
                parts = line.split(':')
                if int(parts[2]) >= 1000 and parts[6] != '/usr/sbin/nologin':
                    users.append(parts[0])
    except Exception as e:
        print(f"Ошибка при чтении /etc/passwd: {e}")
    return users

def get_user_id_info(user):
    try:
        result = subprocess.run(
            ['id', user],
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Ошибка при выполнении команды: {e}"
    except Exception as e:
        return f"Произошла ошибка: {e}"

def get_group_details(group_id):
    try:
        result = subprocess.run(
            ['getent', 'group', group_id],
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return f"Группа с ID {group_id} не найдена"
    except Exception as e:
        return f"Произошла ошибка: {e}"

# Получаем список всех пользователей
users = get_all_users()



def scan_disk_information():
    print("Информация о жёстких дисках:")
    disk_information = subprocess.run(["lsblk"], capture_output=True, text=True)
    print(disk_information.stdout)

def main():
    while True:
        print("nВыберите модуль для сканирования:")
        print("1. Вид операционной системы")
        print("2. Имя узла")
        print("3. Установленные обновления безопасности")
        print("4. Данные учетных записей")
        print("5. Данные паролей")
        print("6. Аудит реестра")
        print("7. Сетевые настройки")
        print("8. NetBIOS и DNS")
        print("9. Запущенные сервисы")
        print("10. Файловая система")
        print("11. Групповые политики")
        print("12. Информация о жёстких дисках")
        print("q. Выйти")

        choice = input("Введите номер модуля (или 'q' для выхода): ")

        if choice == '1':
            scan_os_type()
        elif choice == '2':
            scan_hostname()
        elif choice == '3':
            check_security_updates()
        elif choice == '4':
            scan_user_accounts()
        elif choice == '5':

            for user in users:
                policy_info = get_password_policy(user)
                print(f"Политика паролей для пользователя {user}:\n{policy_info}\n")
        elif choice == '6':
            scan_registry_audit()
        elif choice == '7':
            scan_network_settings()
        elif choice == '8':
            scan_netbios_dns()
        elif choice == '9':
            scan_running_services()
        elif choice == '10':
            scan_filesystem()
        elif choice == '11':
            # Проверяем, удалось ли получить список пользователей
            if not users:
                print("Не удалось получить список пользователей или в системе нет пользователей.")
            else:
                # Для каждого пользователя выводим информацию
                for user in users:
                    id_info = get_user_id_info(user)
                    print(f"Информация для пользователя {user}:\n{id_info}")

                    # Парсим информацию о группах из вывода команды id
                    parts = id_info.split()
                    uid_info = parts[0]
                    gid_info = parts[1]
                    groups_info = parts[2] if len(parts) > 2 else ""

                    print(f"\nДетальная информация для пользователя {user}:")
                    print(f"UID: {uid_info}")
                    print(f"GID: {gid_info}")

                    if groups_info:
                        print("Группы:")
                        groups = groups_info.split('=')[1].split(',')
                        for group in groups:
                            group_id, group_name = group.split('(')
                            group_name = group_name.rstrip(')')
                            group_details = get_group_details(group_id)
                            print(f"  - {group_name} (ID: {group_id}): {group_details}")
                    print("\n" + "="*40 + "\n")
        elif choice == '12':
            scan_disk_information()
        elif choice.lower() == 'q':
            print("Программа завершена.")
            break
        else:
            print("Неверный ввод. Попробуйте снова.")

if __name__ == "__main__":
    main()
