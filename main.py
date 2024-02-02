# Завдання 2
# Реалізуйте консольний додаток «Таблиця рекордів»
# для гри. Дода-ток має дозволити працювати з таблицею
# рекордів гри. Можливості додатку:
# ■ Вхід у таблицю рекордів за логіном і паролем;
# ■ Додати результати користувача до таблиці;
# ■ Видаляти результати з таблиці;
# ■ Змінювати результат в таблиці;
# ■ Повне очищення таблиці;
# ■ Пошук даних в таблиці;
# ■ Перегляд вмісту таблиці;
# ■ Відображення найкращої десятки результатів.
# Зберігайте дані у базі даних NoSQL. Можете використовувати Redis в якості платформи.


import redis
import bcrypt

class RecordTable:
    def __init__(self):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

    def register_user(self, username, password):
        # Перевірка, чи користувач вже існує
        if self.redis_client.hexists(username, 'password_hash'):
            print("Користувач вже існує.")
            return False
        # Зберігання хешу пароля у Redis
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.redis_client.hset(username, 'password_hash', password_hash)
        print("Користувач успішно зареєстрований.")
        return True

    def login(self, username, password):
        # Перевірка логіну та пароля
        stored_password_hash = self.redis_client.hget(username, 'password_hash')
        if stored_password_hash and bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
            print(f"Ви увійшли як {username}.")
            self.current_user = username
            return True
        else:
            print("Невірний логін або пароль.")
            return False

    def add_record(self, score):
        if hasattr(self, 'current_user'):
            key = f"leaderboard:{self.current_user}"
            self.redis_client.zadd(key, {self.current_user: score})
            print(f"Рекорд {score} додано до таблиці рекордів.")
        else:
            print("Спочатку увійдіть у таблицю рекордів.")

    def add_record(self, score):
        if hasattr(self, 'current_user'):
            key = f"leaderboard:{self.current_user}"
            self.redis_client.zadd(key, {self.current_user: score})
            print(f"Рекорд {score} додано до таблиці рекордів.")
        else:
            print("Спочатку увійдіть у таблицю рекордів.")

    def remove_record(self, score):
        if hasattr(self, 'current_user'):
            key = f"leaderboard:{self.current_user}"
            self.redis_client.zremrangebyscore(key, score, score)
            print(f"Рекорд {score} видалено з таблиці рекордів.")
        else:
            print("Спочатку увійдіть у таблицю рекордів.")

    def update_record(self, old_score, new_score):
        if hasattr(self, 'current_user'):
            key = f"leaderboard:{self.current_user}"
            self.redis_client.zremrangebyscore(key, old_score, old_score)
            self.redis_client.zadd(key, {self.current_user: new_score})
            print(f"Рекорд {old_score} оновлено до {new_score} в таблиці рекордів.")
        else:
            print("Спочатку увійдіть у таблицю рекордів.")

# Приклад використання
record_table_app = RecordTable()

# Реєстрація та логін користувача
if record_table_app.register_user("user6", "122"):
    if record_table_app.login("user6", "122"):
        # Додавання та видалення результатів користувача з таблиці рекордів
        record_table_app.add_record(100)
        record_table_app.add_record(150)
        record_table_app.remove_record(100)
        record_table_app.update_record(100, 120)


