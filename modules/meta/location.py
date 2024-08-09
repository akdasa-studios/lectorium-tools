from dataclasses import dataclass

@dataclass
class Location:
    code: str
    aliases: list[str]
    canonical_names: dict[str, str]

LOCATIONS: list[Location] = [
    Location(
        code='moskow',
        aliases=['Moskow', 'Москва', 'Moscow'],
        canonical_names={ 'en': 'Moscow', 'ru': 'Москва', }),
    Location(
        code='chicago',
        aliases=['Чикаго'],
        canonical_names={ 'en': 'Chicago', 'ru': 'Чикаго', }),
    Location(
        code='london',
        aliases=['Лондон'],
        canonical_names={ 'en': 'London', 'ru': 'Лондон', }),
    Location(
        code='paris',
        aliases=['Париж'],
        canonical_names={'en': 'Paris', 'ru': 'Париж'}),
    Location(
        code='tokyo',
        aliases=['Токио'],
        canonical_names={'en': 'Tokyo', 'ru': 'Токио'}),
    Location(
        code='berlin',
        aliases=['Берлин'],
        canonical_names={'en': 'Berlin', 'ru': 'Берлин'}),
    Location(
        code='moscow',
        aliases=['Москва'],
        canonical_names={'en': 'Moscow', 'ru': 'Москва'}),
    Location(
        code='sydney',
        aliases=['Сидней'],
        canonical_names={'en': 'Sydney', 'ru': 'Сидней'}),
    Location(
        code='rome',
        aliases=['Рим'],
        canonical_names={'en': 'Rome', 'ru': 'Рим'}),
    Location(
        code='dubai',
        aliases=['Дубай'],
        canonical_names={'en': 'Dubai', 'ru': 'Дубай'}),
    Location(
        code='toronto',
        aliases=['Торонто'],
        canonical_names={'en': 'Toronto', 'ru': 'Торонто'}),
    Location(
        code='mumbai',
        aliases=['Мумбаи'],
        canonical_names={'en': 'Mumbai', 'ru': 'Мумбаи'}),
    Location(
        code='new-york',
        aliases=['Нью Йорк', 'Нью-Йорк'],
        canonical_names={'en': 'New York', 'ru': 'Нью Йорк'}),
    Location(
        code='los-angeles',
        aliases=['Лос Анджелес', 'Лос-Анджелес'],
        canonical_names={'en': 'Los Angeles', 'ru': 'Лос Анджелес'}),
    Location(
        code='san-francisco',
        aliases=['Сан Франциско', 'Сан Францыско', 'Сан-Франциско'],
        canonical_names={'en': 'San Francisco', 'ru': 'Сан Франциско'}),
    Location(
        code='san-diego',
        aliases=['Сан Диего'],
        canonical_names={'en': 'San Diego', 'ru': 'Сан Диего'}),
    Location(
        code='hong-kong',
        aliases=['Гонконг'],
        canonical_names={'en': 'Hong Kong', 'ru': 'Гонконг'}),
    Location(
        code='mexico-city',
        aliases=['Мехико'],
        canonical_names={'en': 'Mexico City', 'ru': 'Мехико'}),
    Location(
        code='fiji',
        aliases=['Фиджи'],
        canonical_names={'en': 'Fiji', 'ru': 'Фиджи'}),
    Location(
        code='durban',
        aliases=['Дурбан'],
        canonical_names={'en': 'Durban', 'ru': 'Дурбан'}),
    Location(
        code='vrindavan',
        aliases=['Вриндаван'],
        canonical_names={'en': 'Vrindavan', 'ru': 'Вриндаван'}),
    Location(
        code='germany',
        aliases=['Германия'],
        canonical_names={'en': 'Germany', 'ru': 'Германия'}),
    Location(
        code='kolkata',
        aliases=['Калькутта'],
        canonical_names={'en': 'Kolkata', 'ru': 'Калькутта'}),
    Location(
        code='sanand',
        aliases=['Сананд'],
        canonical_names={'en': 'Sanand', 'ru': 'Сананд'}),
    Location(
        code='stockholm',
        aliases=['Стокгольм'],
        canonical_names={'en': 'Stockholm', 'ru': 'Стокгольм'}),
    Location(
        code='hyderabad',
        aliases=['Хайдерабад'],
        canonical_names={'en': 'Hyderabad', 'ru': 'Хайдерабад'}),
    Location(
        code='hawaii',
        aliases=['Гавайи', 'Гаваи'],
        canonical_names={'en': 'Hawaii', 'ru': 'Гавайи'}),
    Location(
        code='johannesburg',
        aliases=['Йоханнесбург'],
        canonical_names={'en': 'Johannesburg', 'ru': 'Йоханнесбург'}),
    Location(
        code='nairobi',
        aliases=['Найроби'],
        canonical_names={'en': 'Nairobi', 'ru': 'Найроби'}),
    Location(
        code='new-delhi',
        aliases=['Нью Дели', 'Нью-Дели', 'Дели'],
        canonical_names={'en': 'New Delhi', 'ru': 'Нью Дели'}),
    Location(
        code='miami',
        aliases=['Майами'],
        canonical_names={'en': 'Miami', 'ru': 'Майами'}),
    Location(
        code='honolulu',
        aliases=['Гонолулу'],
        canonical_names={'en': 'Honolulu', 'ru': 'Гонолулу'}),
    Location(
        code='montreal',
        aliases=['Монреаль'],
        canonical_names={'en': 'Montreal', 'ru': 'Монреаль'}),
    Location(
        code='geneva',
        aliases=['Женева'],
        canonical_names={'en': 'Geneva', 'ru': 'Женева'}),
    Location(
        code='kolkata',
        aliases=['Калькута'],
        canonical_names={'en': 'Kolkata', 'ru': 'Калькута'}),
    Location(
        code='rome',
        aliases=['Рим'],
        canonical_names={'en': 'Rome', 'ru': 'Рим'}),
    Location(
        code='chennai',
        aliases=['Мадрас'],
        canonical_names={'en': 'Chennai', 'ru': 'Мадрас'}),
    Location(
        code='mauritius',
        aliases=['Маврикий'],
        canonical_names={'en': 'Mauritius', 'ru': 'Маврикий'}),
    Location(
        code='columbus',
        aliases=['Каламбус'],
        canonical_names={'en': 'Columbus', 'ru': 'Каламбус'}),
    Location(
        code='bombay',
        aliases=['Бомбей'],
        canonical_names={'en': 'Bombay', 'ru': 'Бомбей'}),
    Location(
        code='mayapur',
        aliases=['Майапур'],
        canonical_names={'en': 'Mayapur', 'ru': 'Майапур'}),
    Location(
        code='detroit',
        aliases=['Детройт'],
        canonical_names={'en': 'Detroit', 'ru': 'Детройт'}),
    Location(
        code='dallas',
        aliases=['Даллас'],
        canonical_names={'en': 'Dallas', 'ru': 'Даллас'}),
    Location(
        code='laguna-beach',
        aliases=['Лагуна-Бич'],
        canonical_names={'en': 'Laguna Beach', 'ru': 'Лагуна-Бич'}),
    Location(
        code='karakas',
        aliases=['Каракас'],
        canonical_names={'en': 'Karakas', 'ru': 'Каракас'}),
    Location(
        code='san-diego',
        aliases=['Сан-Диего'],
        canonical_names={'en': 'San Diego', 'ru': 'Сан Диего'}),
    Location(
        code='philadelphia',
        aliases=['Филадельфия'],
        canonical_names={'en': 'Philadelphia', 'ru': 'Филадельфия'}),
    Location(
        code='tirupati',
        aliases=['Тирупати'],
        canonical_names={'en': 'Tirupati', 'ru': 'Тирупати'}),
    Location(
        code='melbourne',
        aliases=['Мельбурн'],
        canonical_names={'en': 'Melbourne', 'ru': 'Мельбурн'}),
    Location(
        code='denver',
        aliases=['Денвер'],
        canonical_names={'en': 'Denver', 'ru': 'Денвер'}),
    Location(
        code='denver',
        aliases=['Неллор'],
        canonical_names={'en': 'Nellore', 'ru': 'Неллор'}),
    Location(
        code='boston',
        aliases=['Бостон'],
        canonical_names={'en': 'Boston', 'ru': 'Бостон'}),
    Location(
        code='new-orleans',
        aliases=['Новый Орлеан'],
        canonical_names={'en': 'New Orleans', 'ru': 'Новый Орлеан'}),
    Location(
        code='new-zealand',
        aliases=['Новая Зеландия'],
        canonical_names={'en': 'New Zealand', 'ru': 'Новая Зеландия'}),
    Location(
        code='montreal',
        aliases=['Монреаль'],
        canonical_names={'en': 'Montreal', 'ru': 'Монреаль'}),
    Location(
        code='tehran',
        aliases=['Тегеран'],
        canonical_names={'en': 'Tehran', 'ru': 'Тегеран'}),
]

def extract_location(
    path: str
) -> str:
    """
    Extract location from path based on the location names and
    returns it's canonical code. Otherwise raises an exception.
    """
    for location in LOCATIONS:
        for alias in location.aliases:
            if alias in path:
                return (location.code, alias)
    raise Exception(f"Location not found in path {path}")
