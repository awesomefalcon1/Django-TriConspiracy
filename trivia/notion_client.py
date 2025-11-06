import os
import requests
from typing import Any, Dict, List, Optional


NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_DATABASE_EVENTS = os.getenv('NOTION_DATABASE_EVENTS')
NOTION_DATABASE_QUESTIONS = os.getenv('NOTION_DATABASE_QUESTIONS')
NOTION_DATABASE_PRIZES = os.getenv('NOTION_DATABASE_PRIZES')
NOTION_DATABASE_PLACEMENTS = os.getenv('NOTION_DATABASE_PLACEMENTS')


class NotionClient:
    base_url = 'https://api.notion.com/v1'
    notion_version = '2022-06-28'

    def __init__(self) -> None:
        if not NOTION_API_KEY:
            raise RuntimeError('NOTION_API_KEY not set')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {NOTION_API_KEY}',
            'Notion-Version': self.notion_version,
            'Content-Type': 'application/json',
        })

    # Events
    def list_events(self) -> List[Dict[str, Any]]:
        resp = self.session.post(f'{self.base_url}/databases/{NOTION_DATABASE_EVENTS}/query', json={})
        resp.raise_for_status()
        return [self._map_event(page) for page in resp.json().get('results', [])]

    def get_event(self, page_id: str) -> Dict[str, Any]:
        resp = self.session.get(f'{self.base_url}/pages/{page_id}')
        resp.raise_for_status()
        return self._map_event(resp.json())

    def create_event(self, title: str, description: str, starts_at_iso: Optional[str], location: str) -> Dict[str, Any]:
        props: Dict[str, Any] = {
            'Title': {'title': [{'text': {'content': title}}]},
            'Description': {'rich_text': [{'text': {'content': description}}]} if description else {'rich_text': []},
            'Location': {'rich_text': [{'text': {'content': location}}]} if location else {'rich_text': []},
        }
        if starts_at_iso:
            props['Starts At'] = {'date': {'start': starts_at_iso}}
        payload = {'parent': {'database_id': NOTION_DATABASE_EVENTS}, 'properties': props}
        resp = self.session.post(f'{self.base_url}/pages', json=payload)
        resp.raise_for_status()
        return self._map_event(resp.json())

    # Questions
    def list_questions(self, event_page_id: str) -> List[Dict[str, Any]]:
        filter_obj = {
            'filter': {
                'property': 'EventId',
                'rich_text': {'equals': event_page_id},
            }
        }
        resp = self.session.post(f'{self.base_url}/databases/{NOTION_DATABASE_QUESTIONS}/query', json=filter_obj)
        resp.raise_for_status()
        return [self._map_question(page) for page in resp.json().get('results', [])]

    def create_question(self, event_page_id: str, text: str, a: str, b: str, c: str, d: str, correct: str) -> Dict[str, Any]:
        props = {
            'Text': {'title': [{'text': {'content': text}}]},
            'EventId': {'rich_text': [{'text': {'content': event_page_id}}]},
            'Choice A': {'rich_text': [{'text': {'content': a}}]},
            'Choice B': {'rich_text': [{'text': {'content': b}}]},
            'Choice C': {'rich_text': [{'text': {'content': c}}]} if c else {'rich_text': []},
            'Choice D': {'rich_text': [{'text': {'content': d}}]} if d else {'rich_text': []},
            'Correct': {'select': {'name': correct}},
        }
        payload = {'parent': {'database_id': NOTION_DATABASE_QUESTIONS}, 'properties': props}
        resp = self.session.post(f'{self.base_url}/pages', json=payload)
        resp.raise_for_status()
        return self._map_question(resp.json())

    # Prizes
    def list_prizes(self, event_page_id: str) -> List[Dict[str, Any]]:
        filter_obj = {'filter': {'property': 'EventId', 'rich_text': {'equals': event_page_id}}}
        resp = self.session.post(f'{self.base_url}/databases/{NOTION_DATABASE_PRIZES}/query', json=filter_obj)
        resp.raise_for_status()
        items = [self._map_prize(page) for page in resp.json().get('results', [])]
        return sorted(items, key=lambda x: x.get('rank', 0))

    def create_prize(self, event_page_id: str, name: str, description: str, rank: int, value: str) -> Dict[str, Any]:
        props = {
            'Name': {'title': [{'text': {'content': name}}]},
            'EventId': {'rich_text': [{'text': {'content': event_page_id}}]},
            'Description': {'rich_text': [{'text': {'content': description}}]} if description else {'rich_text': []},
            'Rank': {'number': rank},
            'Value': {'number': float(value or 0)},
        }
        payload = {'parent': {'database_id': NOTION_DATABASE_PRIZES}, 'properties': props}
        resp = self.session.post(f'{self.base_url}/pages', json=payload)
        resp.raise_for_status()
        return self._map_prize(resp.json())

    # Placements
    def list_placements(self, event_page_id: str) -> List[Dict[str, Any]]:
        filter_obj = {'filter': {'property': 'EventId', 'rich_text': {'equals': event_page_id}}}
        resp = self.session.post(f'{self.base_url}/databases/{NOTION_DATABASE_PLACEMENTS}/query', json=filter_obj)
        resp.raise_for_status()
        items = [self._map_placement(page) for page in resp.json().get('results', [])]
        return sorted(items, key=lambda x: x.get('rank', 0))

    def create_placement(self, event_page_id: str, participant_name: str, score: int, rank: int) -> Dict[str, Any]:
        props = {
            'Participant': {'title': [{'text': {'content': participant_name}}]},
            'EventId': {'rich_text': [{'text': {'content': event_page_id}}]},
            'Score': {'number': score},
            'Rank': {'number': rank},
        }
        payload = {'parent': {'database_id': NOTION_DATABASE_PLACEMENTS}, 'properties': props}
        resp = self.session.post(f'{self.base_url}/pages', json=payload)
        resp.raise_for_status()
        return self._map_placement(resp.json())

    # Mapping helpers
    def _map_event(self, page: Dict[str, Any]) -> Dict[str, Any]:
        props = page.get('properties', {})
        title = self._get_title(props.get('Title'))
        description = self._get_rich_text(props.get('Description'))
        location = self._get_rich_text(props.get('Location'))
        starts_at = (props.get('Starts At') or {}).get('date') or {}
        return {
            'id': page.get('id'),
            'title': title,
            'description': description,
            'location': location,
            'starts_at': starts_at.get('start'),
        }

    def _map_question(self, page: Dict[str, Any]) -> Dict[str, Any]:
        props = page.get('properties', {})
        return {
            'id': page.get('id'),
            'event_id': self._get_rich_text(props.get('EventId')),
            'text': self._get_title(props.get('Text')),
            'choice_a': self._get_rich_text(props.get('Choice A')),
            'choice_b': self._get_rich_text(props.get('Choice B')),
            'choice_c': self._get_rich_text(props.get('Choice C')),
            'choice_d': self._get_rich_text(props.get('Choice D')),
            'correct_choice': (props.get('Correct') or {}).get('select', {}).get('name') or 'A',
        }

    def _map_prize(self, page: Dict[str, Any]) -> Dict[str, Any]:
        props = page.get('properties', {})
        return {
            'id': page.get('id'),
            'event_id': self._get_rich_text(props.get('EventId')),
            'name': self._get_title(props.get('Name')),
            'description': self._get_rich_text(props.get('Description')),
            'rank': (props.get('Rank') or {}).get('number') or 0,
            'value': (props.get('Value') or {}).get('number') or 0.0,
        }

    def _map_placement(self, page: Dict[str, Any]) -> Dict[str, Any]:
        props = page.get('properties', {})
        return {
            'id': page.get('id'),
            'event_id': self._get_rich_text(props.get('EventId')),
            'participant_name': self._get_title(props.get('Participant')),
            'score': (props.get('Score') or {}).get('number') or 0,
            'rank': (props.get('Rank') or {}).get('number') or 0,
        }

    def _get_title(self, prop: Optional[Dict[str, Any]]) -> str:
        if not prop:
            return ''
        items = prop.get('title') or []
        return ''.join([(it.get('plain_text') or '') for it in items])

    def _get_rich_text(self, prop: Optional[Dict[str, Any]]) -> str:
        if not prop:
            return ''
        items = prop.get('rich_text') or []
        return ''.join([(it.get('plain_text') or '') for it in items])


