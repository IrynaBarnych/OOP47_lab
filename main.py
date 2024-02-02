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

# Приклад використання
record_table_app = RecordTable()

# Реєстрація та логін користувача
if record_table_app.register_user("user6", "122"):
    if record_table_app.login("user6", "122"):
        # Додавання рекорду
        record_table_app.add_record(100)
        record_table_app.add_record(150)


