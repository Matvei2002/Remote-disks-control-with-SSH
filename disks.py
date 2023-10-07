import paramiko
import subprocess
import os


# Функция для получения информации о накопителях на удаленном компьютере
def get_storage_info(remote_host, remote_user, remote_password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(remote_host, username=remote_user, password=remote_password)
    
    # Выполнить команду на удаленном компьютере для получения информации о накопителях
    command = "lsblk -o NAME,SIZE,MODEL --json"
    stdin, stdout, stderr = ssh.exec_command(command)
    storage_info = stdout.read().decode('utf-8')
    
    ssh.close()
    
    return storage_info


# Функция для отображения списка накопителей с использованием Dialog
def display_storage_list(storage_info):
    with open("storage_info.txt", "w") as file:
        file.write(storage_info)
    
    # Отобразить список накопителей с использованием dialog
    os.system("dialog --textbox storage_info.txt 0 0")

if __name__ == "__main__":
    remote_host = input("Введите удаленный хост: ")
    remote_user = input("Введите имя пользователя: ")
    remote_password = input("Введите пароль: ")
    
    storage_info = get_storage_info(remote_host, remote_user, remote_password)
    display_storage_list(storage_info)
