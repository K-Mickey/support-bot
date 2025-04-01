import json
import logging
from pathlib import Path

from bin.dialogflow import create_intent, delete_intent, list_intents
from bin.settings import settings

logger = logging.getLogger(__name__)


def training_dialogflow(
    file_path: Path, project_id: str, update: bool = False
) -> None:
    if not file_path.exists():
        raise FileNotFoundError(f'Файл {file_path} не найден')

    file = file_path.read_text(encoding='utf-8')
    intents = json.loads(file)

    if update:
        exist_intents = list_intents(project_id)
        for intent in exist_intents:
            if intent.display_name in intents:
                delete_intent(project_id, intent.name)

    for title, phrases in intents.items():
        response = create_intent(
            project_id=project_id,
            display_name=title,
            training_phrases_parts=phrases['questions'],
            message_texts=[phrases['answer']],
        )
        logger.info('Intent created: {}'.format(response))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    training_dialogflow(
        file_path=Path('src/questions-example.json'),
        project_id=settings.project_id,
        update=True,
    )
