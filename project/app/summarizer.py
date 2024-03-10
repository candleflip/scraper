"""
Модуль работы с пересказами
"""
import nltk
from newspaper import Article

from app.models.tortoise.summary_schema import TextSummary


async def generate_summary(summary_id: int, url: str) -> None:
    """
    Генерация пересказа текста на WEB-странице по ее URL

    Загрузка и парсинг страницы по переданному URL. Подготовка краткого пересказа
    текста, найденного на странице

    Args:
        summary_id: ID пересказа, заготовка для которого была добавлена в БД ранее
        url: путь до WEB-страницы, на которой расположен текст

    """
    article = Article(url=url)
    article.download()
    article.parse()

    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    finally:
        article.nlp()

    summary = article.summary
    await TextSummary.filter(id=summary_id).update(summary=summary)
