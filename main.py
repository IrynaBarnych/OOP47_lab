import redis

# підключення до локального серверу
r = redis.Redis(host='localhost', port=6379, db = 0)
#створення числового ключа
r.set('counter', 100)
#інкрементування
r.incr('counter')
r.incr('counter')
r.incr('counter')
#декрементування
r.decr("counter")
value = r.get('counter')
print(value)

# Додавання геоданих

r.geoadd('cities', (-97.7431, 30.2672, 'Austin'))
r.geoadd('cities', (-118.2437, 34.0522, 'Los Angeles'))
# Обчислення відстані між двома точками
distance = r.geodist('cities', 'Austin', 'Los Angeles', unit='km')
print(f"Відстань між Austin та Los Angeles: {distance} км")

#


# Отримання місцеположення

location = r.geopos('cities', 'Austin')

print(f"Місцеположення Austin: {location}")