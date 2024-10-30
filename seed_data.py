from datetime import datetime, timedelta
from app import create_app, db, bcrypt
from models import Movie, Showtime, Seat, User, Reservation  # Импортируем модели
from random import randint

def add_test_data():
    # Сохранение всех данных в БД
    list_test_films = [
        ["Матрица", "Хакер узнает правду о своей реальности и присоединяется к восстанию против машин.", "Научная фантастика"],
        ["Начало", "Вор, способный проникать в сны, берется за последнее задание — внедрить идею в чей-то разум.", "Боевик"],
        ["Интерстеллар", "Группа исследователей отправляется через червоточину в космосе, чтобы спасти человечество.", "Научная фантастика"],
        ["Крестный отец", "Стареющий глава мафиозной династии передает контроль над своим бизнесом своему неохотному сыну.", "Криминал"],
        ["Криминальное чтиво", "Жизни двух наемных убийц, боксера и других героев переплетаются в ряде неожиданных событий.", "Криминал"],
        ["Побег из Шоушенка", "Двое заключенных сближаются за долгие годы, находя утешение и искупление в добрых поступках.", "Драма"],
        ["Бойцовский клуб", "Разочарованный офисный работник создает подпольный бойцовский клуб, который превращается во многое другое.", "Драма"],
        ["Темный рыцарь", "Бэтмен должен противостоять загадочному преступнику Джокеру, угрожающему Готэму.", "Боевик"],
        ["Форрест Гамп", "История простого человека, который оказывается свидетелем ключевых событий в истории Америки.", "Драма"],
        ["Список Шиндлера", "История оскароносного бизнесмена, который спасает евреев в годы Холокоста.", "Исторический"],
        ["Зеленая миля", "Заключенный с необычными способностями изменяет жизнь тюремных охранников на 'Зеленой миле'.", "Драма"],
        ["Властелин колец: Братство кольца", "Молодой хоббит отправляется в опасное путешествие, чтобы уничтожить могущественное кольцо.", "Фэнтези"],
        ["Титаник", "История любви на борту обреченного лайнера 'Титаник'.", "Драма"],
        ["Звёздные войны: Империя наносит ответный удар", "Повстанцы сражаются против Империи, а Люк узнает секреты своего прошлого.", "Фантастика"],
        ["Гладиатор", "Римский генерал, ставший рабом, стремится отомстить императору, убившему его семью.", "Исторический"],
        ["Семь", "Два детектива расследуют серию убийств, вдохновленных семью смертными грехами.", "Триллер"],
        ["Чужой", "Экипаж космического корабля сталкивается с агрессивной формой жизни на борту.", "Ужасы"],
        ["Один дома", "Мальчик остается один дома на Рождество и противостоит грабителям.", "Комедия"],
        ["Рататуй", "Крыса с талантом к кулинарии помогает молодому повару преуспеть в ресторане.", "Анимация"],
        ["Гарри Поттер и философский камень", "Мальчик-волшебник начинает учебу в школе магии Хогвартс.", "Фэнтези"]
    ]
    user_data = [
        {"username": "admin", "email": "admin@example.com", "password": "adminpassword", "role": "admin"},
        {"username": "user1", "email": "user1@example.com", "password": "user1password", "role": "user"},
        {"username": "user2", "email": "user2@example.com", "password": "user2password", "role": "user"}
    ]

    # Создание пользователей с хешированием пароля
    users = []
    for data in user_data:
        password_hash = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
        user = User(
            username=data["username"],
            email=data["email"],
            password_hash=password_hash,
            role=data["role"]
        )
        users.append(user)

    # Добавление пользователей в БД
    db.session.add_all(users)

    # Добавление фильмов
    movies = []
    for film in list_test_films:
        movies.append(Movie(
            title=film[0],
            description=film[1],
            genre=film[2]
        ))

    # Сохранение фильмов в БД
    db.session.add_all(movies)
    db.session.commit()

    # Добавление сеансов и мест для каждого фильма
    showtimes = []
    seats = []
    reservations = []
    current_date = datetime.now()

    for movie in movies:
        for i in range(2):  # Создаем 2 сеанса для каждого фильма
            showtime_date = current_date + timedelta(days=randint(1,5), hours=randint(12,23), minutes=randint(0, 59))  # Устанавливаем время 18:00 с интервалом в 1 день
            showtime = Showtime(
                movie_id=movie.id,
                showtime_date=showtime_date
            )
            showtimes.append(showtime)
            
            # Добавление мест для каждого сеанса (например, 5 мест)
            for j in range(7):
                seat_number = f"A{j+1}"  # Номера мест: A1, A2, ..., A5
                seat = Seat(
                    seat_number=seat_number,
                    is_reserved=False,
                    showtime=showtime
                )
                seats.append(seat)

    # Сохранение сеансов и мест в БД
    db.session.add_all(showtimes + seats)
    db.session.commit()

    # Добавление бронирований для пользователей
    for showtime in showtimes:
        reserved_seats = ["A1", "A2"]  # Пример забронированных мест
        reservation = Reservation(
            user_id=users[1].id,  # Связываем бронирование с user1
            showtime_id=showtime.id,
            seats=", ".join(reserved_seats)
        )
        reservations.append(reservation)
        
        # Обновляем статус мест как забронированных
        for seat in seats:
            if seat.showtime_id == showtime.id and seat.seat_number in reserved_seats:
                seat.is_reserved = True

    # Сохранение бронирований в БД
    db.session.add_all(reservations)

    
    db.session.add_all(movies)
    db.session.commit()
    
    showtimes = []
    current_date = datetime.now()

    for movie in movies:
        for i in range(3):  # Добавляем по 3 сеанса для каждого фильма
            showtime_date = current_date + timedelta(days=i, hours=18)  # Устанавливаем время на 18:00, 18:00 на следующий день и так далее
            showtimes.append(Showtime(
                movie_id=movie.id,
                showtime_date=showtime_date
            ))

    # Сохранение сеансов в БД
    db.session.add_all(showtimes)
    db.session.commit()
    print("Test data added successfully!")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():  # Инициализация контекста приложения
        add_test_data()
