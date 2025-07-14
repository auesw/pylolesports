from requests import Response, Session
from typing import List, Any
import datetime

from .config import Locales

# TODO Docstrings and type hintings

class BaseEndpointRaw:
    def __init__(self, session: Session, api_url: str):
        self.session = session
        self.api_url = api_url

    def handle_request_exception(self, response: Response) -> None:
        try:
            response.json()
        except Exception as e:
            raise(Exception(f'{e} - Request status code: {response.status_code}'))

class EndpointLeaguesRaw(BaseEndpointRaw):
    def __init__(self, session, api_url):
        super().__init__(session, api_url)

    def get_leagues(self, hl: str = Locales.english_us) -> Any:
        response = self.session.get(self.api_url + '/getLeagues',
                                    params={'hl': hl})
        self.handle_request_exception(response)
        return response.json()
    
    def get_tournaments_for_league(self, hl: str = Locales.english_us, league_id: int = None) -> Any:
        response = self.session.get(
            self.api_url + '/getTournamentsForLeague',
            params={
                'hl': hl,
                'leagueId': league_id
            }
        )
        self.handle_request_exception(response)
        return response.json()

    def get_standings(self, hl: str = Locales.english_us, tournament_id: List[int] = None) -> Any:
        response = self.session.get(
            self.api_url + '/getStandings',
            params={
                'hl': hl,
                'tournamentId': tournament_id
            }
        )
        self.handle_request_exception(response)
        return response.json()
    
class EndpointEventsRaw(BaseEndpointRaw):
    def __init__(self, session, api_url):
        super().__init__(session, api_url)
    
    def get_schedule(self, hl: str = Locales.english_us, league_id: List[int] = None, page_token: str = None) -> Any:
        response = self.session.get(
            self.api_url + '/getSchedule',
            params={
                'hl': hl,
                'leagueId': league_id,
                'pageToken': page_token
            }
        )

        self.handle_request_exception(response)
        return response.json()

    def get_live(self, hl: str = Locales.english_us) -> dict:
        response = self.session.get(
            self.api_url + '/getLive',
            params={'hl': hl}
        )
        self.handle_request_exception(response)
        return response.json()

    def get_completed_events(self, hl: str = Locales.english_us, tournament_id: List[int] = None) -> Any:
        response = self.session.get(
            self.api_url + '/getCompletedEvents',
            params={
                'hl': hl,
                'tournamentId': tournament_id
            }
        )
        self.handle_request_exception(response)
        return response.json()

    def get_event_details(self, match_id: int, hl: str = Locales.english_us) -> Any:
        response = self.session.get(
            self.api_url + '/getEventDetails',
            params={
                'hl': hl,
                'id': match_id
            }
        )
        self.handle_request_exception(response)
        return response.json()

    def get_games(self, hl: str = Locales.english_us, match_id: List[int] = None) -> Any:
        response = self.session.get(
            self.api_url + '/getGames',
            params={
                'hl': hl,
                'id': match_id
            }
        )
        self.handle_request_exception(response)
        return response.json()

class EndpointTeamsRaw(BaseEndpointRaw):
    def __init__(self, session, api_url):
        super().__init__(session, api_url)
    
    def get_teams(self, hl: str = Locales.english_us, team_slug: str = None) -> Any:
        response = self.session.get(
            self.api_url + '/getTeams',
            params={
                'hl': hl,
                'id': team_slug
            }
        )
        self.handle_request_exception(response)
        return response.json()

class EndpointMatchDetailsRaw(BaseEndpointRaw):
    # Wrapper for the '/livestats' lol esports api endpoint
    def __init__(self, session, api_url):
        super().__init__(session, api_url)
    
    @staticmethod
    def get_latest_date() -> str:
        now = datetime.datetime.now(datetime.timezone.utc)
        now = now - datetime.timedelta(
            seconds=now.second,
            microseconds=now.microsecond
        )
        now_string = now.isoformat()
        return str(now_string).replace('+00:00', 'Z')

    def get_window(self, game_id: int, starting_time: str = get_latest_date()) -> Any:
        response = self.session.get(
            self.api_url + f'/window/{game_id}',
            params={
                'startingTime': starting_time
            }
        )
        self.handle_request_exception(response)
        return response.json()

    def get_details(self, game_id: int, starting_time: str = get_latest_date(), participant_ids: str = None) -> Any:
        response = self.session.get(
            self.api_url + f'/details/{game_id}',
            params={
                'startingTime': starting_time,
                'participantIds': participant_ids
            }
        )
        self.handle_request_exception(response)
        return response.json()

"""
class EndpointPersistedRaw:
    # Wrapper for the '/persisted' lol esports api endpoint
    def __init__(self, session: requests.Session):
        # Before passing the session argument, update its headers with
        # the api key (session.headers.update(api_key))
        self.session = session
        self.api_url = ENDPOINT_PERSISTED_URL
    
    def get_leagues(self, hl: str = Locales.english_us):
        response = self.session.get(self.api_url + '/getLeagues',
                                    params={'hl': hl})
        try:
            json: dict = response.json()
        except Exception as e:
            raise(Exception(f'{e} - Request status code: {response.status_code}'))
        return json
    
    def get_tournaments_for_league(self, hl: str = Locales.english_us, league_id=None):
        response = self.session.get(
            self.api_url + '/getTournamentsForLeague',
            params={
                'hl': hl,
                'leagueId': league_id
            }
        )

        try:
            json: dict = response.json()
        except Exception as e:
            raise(Exception(f'{e} - Request status code: {response.status_code}'))
        return json

    def get_standings(self, hl: str = Locales.english_us, tournament_id=None):
        response = self.session.get(
            self.api_url + '/getStandings',
            params={
                'hl': hl,
                'tournamentId': tournament_id
            }
        )
        # TODO Error handling

        return json.loads(response.text)['data']
    
    def get_schedule(self, hl: str = Locales.english_us, league_id=None, pageToken=None):
        response = self.session.get(
            self.api_url + '/getSchedule',
            params={
                'hl': hl,
                'leagueId': league_id,
                'pageToken': pageToken
            }
        )
        # TODO Error handling

        return json.loads(response.text)['data']

    def get_live(self, hl: str = Locales.english_us):
        response = self.session.get(
            self.api_url + '/getLive',
            params={'hl': hl}
        )
        # TODO Error handling

        return json.loads(response.text)['data']

    def get_completed_events(self, hl: str = Locales.english_us, tournament_id=None):
        response = self.session.get(
            self.api_url + '/getCompletedEvents',
            params={
                'hl': hl,
                'tournamentId': tournament_id
            }
        )
        # TODO Error handling

        return json.loads(response.text)['data']

    def get_event_details(self, match_id, hl: str = Locales.english_us):
        response = self.session.get(
            self.api_url + '/getEventDetails',
            params={
                'hl': hl,
                'id': match_id
            }
        )
        # TODO Error handling

        return json.loads(response.text)['data']

    def get_games(self, hl: str = Locales.english_us, match_id=None):
        response = self.session.get(
            self.api_url + '/getGames',
            params={
                'hl': hl,
                'id': match_id
            }
        )
        # TODO Error handling

        return json.loads(response.text)['data']

    def get_teams(self, hl: str = Locales.english_us, team_slug=None):
        response = self.session.get(
            self.api_url + '/getTeams',
            params={
                'hl': hl,
                'id': team_slug
            }
        )
        # TODO Error handling

        return json.loads(response.text)['data']

class EndpointLivestatsRaw:
    # Wrapper for the '/livestats' lol esports api endpoint
    def __init__(self, session: requests.Session):
        self.session = session
        self.api_url = ENDPOINT_LIVESTATS_URL

    def get_window(self, game_id, starting_time=get_latest_date()):
        response = self.session.get(
            self.api_url + f'/window/{game_id}',
            params={
                'startingTime': starting_time
            }
        )
        # TODO Error handling

        return json.loads(response.text)

    def get_details(self, game_id, starting_time=get_latest_date(), participant_ids=None):
        response = self.session.get(
            self.api_url + f'/details/{game_id}',
            params={
                'startingTime': starting_time,
                'participantIds': participant_ids
            }
        )
        # TODO Error handling

        return json.loads(response.text)"""