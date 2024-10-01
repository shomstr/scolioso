from pathlib import Path

from typing import NoReturn, Union

import yaml
from jinja2 import Template

from bot.settings import BotDir
from bot.utils.tree import formatted_top_number, formatted_heght_tree


class JinjaTexts:
    """Класс для генерации шаблонов из yaml файла"""

    def __init__(self, file_name: str):
        """
        :param file_name: `str` - yaml файл в котором хранятся шаблоны
        """
        self.file_name = file_name

        with open(self.file_name, "r") as file:
            self.yaml = yaml.safe_load(file)

    def __get_template(self, template_name: str) -> Union[Template, NoReturn]:
        """
        Получение шаблона
        :param template_name:`str` - название шаблона
        :raise NameError если шаблон не найден
        """

        if template_name not in self.yaml:
            raise NameError(f'Template "{template_name}" not find in "{self.file_name}"')

        template_text = self.yaml[template_name]
        template = Template(template_text)

        template.globals.update(
            enumerate=enumerate,
            len=len,
            round=round,
            formatted_heght_tree=formatted_heght_tree,
            formatted_top_number=formatted_top_number,
        )

        return template

    def gettext(self, template_name: str, context: dict | None = None) -> str:
        """Генерирует текст на основе шаблона
        :param template_name: `str` - переменная в yaml файле
        :param context: `Optional[dict]` -"""

        if context is None:
            context = {}
        template = self.__get_template(template_name)

        text = template.render(context)

        text = text.replace("\n", "")
        text = text.replace("<nl>", "\n")
        return text.replace("<space>", " ")


path = Path(BotDir) / "messages.yaml"

Texts = JinjaTexts(str(path))
