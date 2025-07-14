from .api.config import ENDPOINT_PERSISTED_URL, ENDPOINT_LIVESTATS_URL
from requests import Session
from .api.endpoints import EndpointLeagues, EndpointEvents, EndpointTeams, EndpointMatchDetails

class LolEsportsApi:
    # Wrapper for the '/persisted' lol esports api endpoint
    def __init__(self, session: Session):
        # Before passing the session argument, update its headers with
        # the api key (session.headers.update(api_key))
        self.session = session
        self.api_url_persisted = ENDPOINT_PERSISTED_URL
        self.api_url_livestats = ENDPOINT_LIVESTATS_URL
    
    def leagues(self):
        return EndpointLeagues(self.session, self.api_url_persisted)
    
    def events(self):
        return EndpointEvents(self.session, self.api_url_persisted)

    def teams(self):
        return EndpointTeams(self.session, self.api_url_persisted)
    
    def match_details(self):
        return EndpointMatchDetails(self.session, self.api_url_livestats)