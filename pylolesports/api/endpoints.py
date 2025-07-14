from typing import List

from requests import Session
from .data_models import LeaguesModels, EventsModels, TeamsModels, MatchDetailsModels
from .config import Locales
from .endpoints_raw import EndpointLeaguesRaw, EndpointEventsRaw, EndpointTeamsRaw, EndpointMatchDetailsRaw

# TODO@auesw Docstrings and type hintings
# TODO Finish EndpointEvents methods

# Unofficial documentation: https://vickz84259.github.io/lolesports-api-docs/#operation/getWindow
"""
When inserting data into my custom data models, I decided to unpack the
dictionary by calling **dict. This was done for safety reasons, since if
an unexpected field is found in the dictionary, the code will raise an
error. This should give me the opportunity to detect any new data being
received.

Also, using dataclasses allow me to detect if the queried dictionary
does not contain an expected field. The code should raise an error in
this case
"""

class BaseEndpoint:
    def __init__(self, session: Session, api_url: str):
        self.session = session
        self.api_url = api_url

class EndpointLeagues(BaseEndpoint):
    def __init__(self, session, api_url):
        super().__init__(session, api_url)
        self.api_raw = EndpointLeaguesRaw(self.session, self.api_url)

    def get_leagues(self, hl: str = Locales.english_us) -> List[LeaguesModels.League]:
        league_list = []
        data = self.api_raw.get_leagues(hl)
        for league in data['data']['leagues']:
            league_list.append(LeaguesModels.League(**league))
        return league_list

    def get_tournaments_for_league(self, league_id: int, hl: str = Locales.english_us) -> List[LeaguesModels.LeagueTournament]:
        tournament_list = []
        leagues = self.api_raw.get_tournaments_for_league(hl, league_id)
        for league in leagues['data']['leagues']:
            for tournament in league['tournaments']:
                tournament_list.append(LeaguesModels.LeagueTournament(**tournament))
        return tournament_list

    def get_standings(self, hl: str = Locales.english_us, tournament_id=None) -> List[LeaguesModels.Standing]:
        standings_list = []

        def get_teams_in_match(match_: dict) -> List[LeaguesModels.LeagueStandingsMatchTeam]:
            team_list = []
            for team in match_['teams']:
                t = LeaguesModels.LeagueStandingsMatchTeam(**team)
                
                if team['result']:
                    t.result = LeaguesModels.LeagueStandingsTeamResult(**team['result'])
                
                team_list.append(t)
            return team_list
        
        def get_matches_in_section(section: dict) -> List[LeaguesModels.LeagueStandingsMatch]:
            match_list = []
            teams_in_match = []
            for match_ in section['matches']:
                teams_in_match = get_teams_in_match(match_)

                m = LeaguesModels.LeagueStandingsMatch(**match_)
                m.teams = teams_in_match
                match_list.append(m)
            return match_list
        
        def get_rankings_in_section(section: dict) -> List[LeaguesModels.LeagueStandingsRanking]:
            def get_teams_in_ranking(ranking: dict) -> List[LeaguesModels.LeagueStandingsRankingTeam]:
                team_list = []
                for team in ranking:
                    t = LeaguesModels.LeagueStandingsRankingTeam(**team)
                    t.record = LeaguesModels.LeagueStandingsTeamRecord(
                        losses=team['record']['losses'], wins=team['record']['wins'])

                    team_list.append(t)
                return team_list

            rankings = []
            for ranking in section['rankings']:
                r = LeaguesModels.LeagueStandingsRanking(**ranking)
                r.teams = get_teams_in_ranking(ranking)
                rankings.append(r)
            return rankings

        def get_sections_in_stage(stage: dict) -> List[LeaguesModels.LeagueStandingsSection]:
            sections = []
            for section in stage['sections']:

                s = LeaguesModels.LeagueStandingsSection(**section)
                s.matches = get_matches_in_section(section)
                s.rankings = get_rankings_in_section(section)
                sections.append(s)
            return sections
        
        def get_stages_in_standings(standings: dict) -> List[LeaguesModels.LeagueStandingsStage]:
            stages_list = []
            for stage in standings['stages']:
                stages_list.append(LeaguesModels.LeagueStandingsStage(
                    name=stage['name'],
                    type=stage['type'],
                    slug=stage['slug'],
                    sections=get_sections_in_stage(stage)
                ))
            return stages_list
        
        data = self.api_raw.get_standings(hl, tournament_id)
        for standing in data['data']['standings']:
            standings_list.append(LeaguesModels.Standing(get_stages_in_standings(standing)))

        return standings_list

class EndpointEvents(BaseEndpoint) :
    def __init__(self, session, api_url):
        super().__init__(session, api_url)
        self.api_raw = EndpointEventsRaw(self.session, self.api_url)

    def get_schedule(self, hl:str=Locales.english_us, league_id=None, page_token=None) -> EventsModels.Schedule:
        def get_pages_from_schedule(schedule: dict) -> EventsModels.EventSchedulePages:
            return EventsModels.EventSchedulePages(**schedule['pages'])

        def get_teams_from_match(match_: dict) -> List[EventsModels.EventScheduleMatchTeam]:
            teams = []
            for team in match_['teams']:
                t = EventsModels.EventScheduleMatchTeam(**team)
                t.result = EventsModels.EventScheduleTeamResult(**team['result'])
                t.record = EventsModels.EventScheduleTeamRecord(**team['record'])
                teams.append(t)
            return teams

        def get_strategy_from_match(match_: dict) -> EventsModels.EventScheduleStrategy:
            return EventsModels.EventScheduleStrategy(match_['strategy'])

        def get_match_from_event(event: dict) -> EventsModels.EventScheduleMatch:
            m = EventsModels.EventScheduleMatch(**event['match'])
            m.teams = get_teams_from_match(event['match'])
            m.strategy = get_strategy_from_match(event['match'])
            return m

        def get_league_from_event(event: dict) -> EventsModels.EventScheduleLeague:
            return EventsModels.EventScheduleLeague(**event['league'])

        def get_events_from_schedule(schedule: dict) -> List[EventsModels.EventScheduleEvent]:
            events = []
            for event in schedule['events']:
                e = EventsModels.EventScheduleEvent(**event)
                e.match = get_match_from_event(event)
                e.league = get_league_from_event(event)
                events.append(e)
            return events
        
        data = self.api_raw.get_schedule(hl, league_id, page_token)
        schedule = EventsModels.Schedule(**data['data']['schedule'])
        schedule.pages = get_pages_from_schedule(data['data']['schedule'])
        schedule.events = get_events_from_schedule(data['data']['schedule'])
        return schedule

    def get_live(self, hl: str=Locales.english_us):
        # TODO Fix. I'm not interested in this endpoint right now
        return
        def get_teams_from_match(match_: dict) -> List[EventsModels.EventLiveMatchTeam]:
            teams = []
            for team in match_['teams']:
                t = EventsModels.EventLiveMatchTeam(**team)
                t.result = EventsModels.EventLiveTeamResult(**team['result'])
                t.record = EventsModels.EventLiveTeamRecord(**team['record'])
            return teams
        
        def get_strategy_from_match(match_: dict) -> EventsModels.EventLiveStrategy:
            return EventsModels.EventLiveStrategy(**match_['strategy'])
    
        def get_match_from_event(event: dict) -> EventsModels.EventLiveMatch:
            m = EventsModels.EventLiveMatch(**event['match'])
            m.teams = get_teams_from_match(event['match'])
            m.strategy = get_strategy_from_match(event['match'])
            return m

        def get_league_from_event(event: dict) -> EventsModels.EventLiveLeague:
            return EventsModels.EventLiveLeague(**event['league'])

        def get_events_from_schedule(schedule: dict) -> List[EventsModels.EventLiveEvent]:
            events = []
            for event in schedule['events']:
                e = EventsModels.EventLiveEvent(**event)
                e.match = get_match_from_event(event)
                e.league = get_league_from_event(event)
                e.tournament = EventsModels.EventLiveEventTournament(**event['tournament'])

                events.append(e)
            return events
        
        data = self.api_raw.get_live(hl)
        live_schedule = EventsModels.LiveSchedule(**data['data']['schedule'])
        live_schedule.events = get_events_from_schedule(data['data']['schedule'])
        return live_schedule

    def get_completed_events(self):
        # TODO Write this method
        pass

    def get_event_details(self):
        # TODO Write this method
        pass

    def get_games(self):
        # TODO Write this method
        pass

class EndpointTeams(BaseEndpoint):
    def __init__(self, session, api_url):
        super().__init__(session, api_url)
        self.api_raw = EndpointTeamsRaw(self.session, self.api_url)
    
    def get_teams(self,  id_: List[str], hl:str= Locales.english_us) -> List[TeamsModels.Team]:
        teams = []
        data = self.api_raw.get_teams()
        for team in data['data']['teams']:
            t = TeamsModels.Team(**team)

            if team['homeLeague']:
                # During testing, there was a dict without the
                # 'homeLeague' key. I found out that there are some
                # dicts that are not about any real team (for example,
                # a TBD team which seems to be a placeholder)
                t.homeLeague = TeamsModels.HomeLeague(**team['homeLeague'])
            players = []
            for player in team['players']:
                players.append(TeamsModels.Player(**player))
            t.players = players
            teams.append(t)
        return teams
    
class EndpointMatchDetails(BaseEndpoint):
    def __init__(self, session, api_url):
        super().__init__(session, api_url)
        self.api_raw = EndpointMatchDetailsRaw(self.session, self.api_url)

    def get_window(self, game_id: int, starting_time: str = EndpointMatchDetailsRaw.get_latest_date()) -> MatchDetailsModels.Window:

        def get_game_metadata_from_window(window: dict) -> MatchDetailsModels.window.GameMetadata:
            metadata = MatchDetailsModels.window.GameMetadata(**window['gameMetadata'])
            metadata.blueTeamMetadata = MatchDetailsModels.window.TeamMetadata(**window['gameMetadata']['blueTeamMetadata'])
            metadata.redTeamMetadata = MatchDetailsModels.window.TeamMetadata(**window['gameMetadata']['blueTeamMetadata'])

            blue_participants = []
            red_participants = []
            for participant in metadata.blueTeamMetadata.participantMetadata:
                if 'esportsPlayerId' in participant.keys():
                    blue_participants.append(MatchDetailsModels.ParticipantMetadataExtended(**participant))
                else:
                    blue_participants.append(MatchDetailsModels.ParticipantMetadata(**participant))
            
            for participant in metadata.redTeamMetadata.participantMetadata:
                if 'esportsPlayerId' in participant.keys():
                    red_participants.append(MatchDetailsModels.window.ParticipantMetadataExtended(**participant))
                else:
                    red_participants.append(MatchDetailsModels.window.ParticipantMetadata(**participant))
            
            metadata.blueTeamMetadata.participantMetadata = blue_participants
            metadata.redTeamMetadata.participantMetadata = red_participants
            return metadata

        def get_frames_from_window(window: dict) -> List[MatchDetailsModels.window.WindowFrame]:
            def get_teams_stats_from_frame(frame: dict) -> dict:
                team_stats_dict = {'blue': None, 'red': None}

                blue_team_stats = MatchDetailsModels.window.TeamStats(**frame['blueTeam'])
                red_team_stats = MatchDetailsModels.window.TeamStats(**frame['redTeam'])

                blue_team_participants = []
                red_team_participants = []
                for participant in blue_team_stats.participants:
                    p = MatchDetailsModels.window.ParticipantStats(**participant)
                    blue_team_participants.append(p)
                blue_team_stats.participants = blue_team_participants

                for participant in red_team_stats.participants:
                    p = MatchDetailsModels.window.ParticipantStats(**participant)
                    red_team_participants.append(p)
                red_team_stats.participants = red_team_participants

                team_stats_dict['blue'] = (blue_team_stats)
                team_stats_dict['red'] = (red_team_stats)
                return team_stats_dict

            frames = []
            for frame in window['frames']:
                both_teams_stats = get_teams_stats_from_frame(frame)
                f = MatchDetailsModels.window.WindowFrame(**frame)
                f.blueTeam = both_teams_stats['blue']
                f.redTeam = both_teams_stats['red']
                frames.append(f)
            return frames

        data = self.api_raw.get_window(game_id, starting_time)
        window = MatchDetailsModels.window.Window(**data)
        window.gameMetadata = get_game_metadata_from_window(data)
        window.frames = get_frames_from_window(data)
        return window

    def get_details(self, game_id: int, starting_time: str = EndpointMatchDetailsRaw.get_latest_date(), participant_ids: str = None):
        data = self.api_raw.get_details(game_id, starting_time, participant_ids)
        frames = []
        for frame in data['frames']:
            f = MatchDetailsModels.details.Frame(**frame)
            participants = []
            for participant in frame['participants']:
                p = MatchDetailsModels.details.ParticipantStatsExtended(**participant)
                p.perkMetadata = MatchDetailsModels.details.PerkMetadata(**participant['perkMetadata'])
                participants.append(p)

            f.participants = participants
            frames.append(f)

        return frames
