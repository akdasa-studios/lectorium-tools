from dataclasses import dataclass

@dataclass
class Location:
    name: str
    aliases: list[str]

LOCATIONS: list[Location] = [
    Location(name='London', aliases=['Лондон']),
    Location(name='Paris', aliases=['Париж']),
    Location(name='Tokyo', aliases=['Токио']),
    Location(name='Berlin', aliases=['Берлин']),
    Location(name='Moscow', aliases=['Москва']),
    Location(name='Sydney', aliases=['Сидней']),
    Location(name='Rome', aliases=['Рим']),
    Location(name='Dubai', aliases=['Дубай']),
    Location(name='Toronto', aliases=['Торонто']),
    Location(name='Mumbai', aliases=['Мумбаи']),
    Location(name='New York', aliases=['Нью Йорк', 'Нью-Йорк']),
    Location(name='Los Angeles', aliases=['Лос Анджелес']),
    Location(name='San Francisco', aliases=['Сан Франциско', 'Сан Францыско']),
    Location(name='London', aliases=['Лондон']),
    Location(name='San Diego', aliases=['Сан Диего']),
    Location(name='Hong Kong', aliases=['Гонконг']),
    Location(name='Mexico City', aliases=['Мехико']),
    Location(name='Fiji', aliases=['Фиджи']),
    Location(name='Durban', aliases=['Дурбан']),
    Location(name='Vrindavan', aliases=['Вриндаван']),
    Location(name='Germany', aliases=['Германия']),
    Location(name='Kolkata', aliases=['Калькутта']),
    Location(name='Sanand', aliases=['Сананд']),
    Location(name='Stockholm', aliases=['Стокгольм']),
    Location(name='Hyderabad', aliases=['Хайдерабад']),
    Location(name='Hawaii', aliases=['Гавайи']),
    Location(name='Johannesburg', aliases=['Йоханнесбург']),
    Location(name='Nairobi', aliases=['Найроби']),
    Location(name='New Delhi', aliases=['Нью Дели', 'Нью-Дели']),
    Location(name='Miami', aliases=['Майами']),
    Location(name='Honolulu', aliases=['Гонолулу']),
    Location(name='Montreal', aliases=['Монреаль']),
    Location(name='Geneva', aliases=['Женева']),
    Location(name='Kolkata', aliases=['Калькута']),
    Location(name='Rome', aliases=['Рим']),
    Location(name='Chennai', aliases=['Мадрас']),
    Location(name='Mauritius', aliases=['Маврикий']),
    Location(name='Columbus', aliases=['Каламбус']),
    Location(name='Bombay', aliases=['Бомбей']),
]

def extract_location(
    path: str
) -> str:
    """
    Extract location from path based on the location names and
    returns it's canonical name. Otherwise raises an exception.
    """
    for location in LOCATIONS:
        for alias in location.aliases:
            if alias in path:
                return (location.name, alias)
    raise Exception(f"Location not found in path {path}")
