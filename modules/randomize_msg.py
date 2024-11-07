import random


async def get_synonyms(word):
    """Возвращает список синонимов для заданного слова."""
    synonyms = {
        "Hello": ["Hello", "Hi", "Greetings", "Salutations"],
        "I": ["I", "we"],
        "would": ["shall", "should", "will", "can", "may", "might",
                  "could have", "would"],
        "like": ["like", "want", "prefer"],
        "to": ["to"],
        "book": ["appointment", "engagement", "arrangement", "ticket",
                 "registration", "subscription", "confirm", "hold",
                 "plan", "reserve", "book"],
        "a": ["a", "one"],
        "room": ["room", "chamber", "suite"],
        "currently": ["currently", "at the moment", "right now"],
        "at": ["at", "in"],
        "your": ["your", "thee", "thy"],
        "hotel": ["hotel", "inn", "lodge"],
        "guests": ["guests", "visitors", "customers"],
    }
    return synonyms.get(word, [word])


async def generate_variations(base_sentence):
    """Генерирует одну вариацию базового предложения, используя синонимы."""
    words = base_sentence.split()
    variation = []
    for word in words:
        synonym_list = await get_synonyms(word.strip())
        variation.append(random.choice(synonym_list))
    return " ".join(variation)