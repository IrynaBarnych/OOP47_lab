import redis
import bcrypt

class RecordTable:
    def __init__(self):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
        self.current_user = None

    def register_user(self, username, password):
        if self.redis_client.hexists(username, 'password_hash'):
            print("Користувач вже існує.")
            return False
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.redis_client.hset(username, 'password_hash', password_hash)
        print(f"Користувач {username} успішно зареєстрований.")
        return True

    def login(self, username, password):
        stored_password_hash = self.redis_client.hget(username, 'password_hash')
        if stored_password_hash and bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
            print(f"Ви увійшли як {username}.")
            self.current_user = username
            return True
        else:
            print("Невірний логін або пароль.")
            return False

    def add_record(self, score):
        if self.current_user is not None:
            key = f"leaderboard:{self.current_user}"
            self.redis_client.zadd(key, {self.current_user: score})
            print(f"Рекорд {score} додано до таблиці рекордів.")
        else:
            print("Спочатку увійдіть у таблицю рекордів.")

    def remove_record(self, score):
        if self.current_user is not None:
            key = f"leaderboard:{self.current_user}"
            self.redis_client.zremrangebyscore(key, score, score)
            print(f"Рекорд {score} видалено з таблиці рекордів.")
        else:
            print("Спочатку увійдіть у таблицю рекордів.")

    def update_record(self, old_score, new_score):
        if self.current_user is not None:
            key = f"leaderboard:{self.current_user}"
            self.redis_client.zremrangebyscore(key, old_score, old_score)
            self.redis_client.zadd(key, {self.current_user: new_score})
            print(f"Рекорд {old_score} оновлено до {new_score} в таблиці рекордів.")
        else:
            print("Спочатку увійдіть у таблицю рекордів.")

    def clear_leaderboard(self):
        if self.current_user is not None:
            key = f"leaderboard:{self.current_user}"
            self.redis_client.delete(key)
            print("Таблицю рекордів очищено.")
        else:
            print("Спочатку увійдіть у таблицю рекордів.")

    def search_record(self, score):
        if self.current_user is not None:
            key = f"leaderboard:{self.current_user}"
            rank = self.redis_client.zrank(key, self.current_user)
            if rank is not None:
                print(f"Рекорд користувача {self.current_user} у таблиці рекордів: {score}")
            else:
                print(f"Користувач {self.current_user} відсутній у таблиці рекордів.")
        else:
            print("Спочатку увійдіть у таблицю рекордів.")

    def view_leaderboard(self):
        if self.current_user is not None:
            key = f"leaderboard:{self.current_user}"
            leaderboard = self.redis_client.zrevrangebyscore(key, '+inf', '-inf', start=0, num=10, withscores=True)
            if leaderboard:
                print("Вміст таблиці рекордів:")
                for rank, (user, score) in enumerate(leaderboard, start=1):
                    print(f"{rank}. {user}: {score}")
            else:
                print("Таблиця рекордів порожня.")
        else:
            print("Спочатку увійдіть у таблицю рекордів.")

    def view_top_scores(self):
        if self.current_user is not None:
            key = f"leaderboard:{self.current_user}"
            top_scores = self.redis_client.zrevrangebyscore(key, '+inf', '-inf', start=0, num=10, withscores=True)
            if top_scores:
                print("Найкращі десять результатів:")
                for rank, (user, score) in enumerate(top_scores, start=1):
                    print(f"{rank}. {user}: {score}")
            else:
                print("Таблиця рекордів порожня.")
        else:
            print("Спочатку увійдіть у таблицю рекордів.")

# Приклад використання
record_table_app = RecordTable()

# Реєстрація та логін користувача
if record_table_app.register_user("user1", "password123"):
    if record_table_app.login("user1", "password123"):
        # Додавання, оновлення та видалення результатів користувача з таблиці рекордів
        record_table_app.add_record(100)
        record_table_app.add_record(150)

        # Пошук результату
        record_table_app.search_record(100)

        # Оновлення результату
        record_table_app.update_record(100, 120)

        # Видалення результату
        record_table_app.remove_record(120)

        # Перегляд вмісту таблиці рекордів
        record_table_app.view_leaderboard()

        # Перегляд найкращих десяти результатів
        record_table_app.view_top_scores()
