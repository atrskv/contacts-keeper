from enum import Enum


class Gender(Enum):
    male = 'Мужчина'
    female = 'Женщина'
    other = '...'
    hui = 'hui'


class Priority(Enum):
    regular = 'Обычный'
    high = 'Особой важности'


class Category(Enum):
    not_selected = 'Не выбрана'
    friends = 'Друзья'
    family = 'Семья'
    work = 'Работа'
    clients = 'Клиенты'


class Channel(Enum):
    can_call = 'Можно звонить'
    can_message = 'Можно писать сообщения'
    email_preferred = 'Предпочтительно по эл. почте'
