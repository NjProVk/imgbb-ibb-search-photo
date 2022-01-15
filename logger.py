from datetime import datetime

with open('ibb.log', 'w+', encoding='utf-8') as clear:
    pass


def log(message_log='None', status='MESSAGE'):
    with open('ibb.log', 'a', encoding='utf-8') as log_save:
        time = datetime.now().strftime("%H:%M:%S")
        log_save.write(f"[{time}] - {status}: {message_log}\n")

#  Version 1.0.5 create by NjProVk
