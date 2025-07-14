# lolesports-api-wrapper

lolesports api python wrapper + models for data safety

## Example

```python
    from requests_cache import CachedSession
    API_KEY = 'your-api-key'
    REQUEST_INTERVAL = 600 # 10 min

    session = CachedSession(
        cache_name='cache/lolesports_cache',
        expire_after=REQUEST_INTERVAL
    )
    session.headers.update({'x-api-key': API_KEY})
    
    api = LolEsportsApi(session)
    endpoint_leagues = api.leagues()
    endpoint_events = api.events()
    endpoint_teams = api.teams()
    endpoint_match_details = api.match_details()

    EXAMPLE_TEAM_ID = '100205573495116443'
    EXAMPLE_GAME_ID = '114217030657972324'
    league = endpoint_leagues.get_leagues()[0]
    tournament = endpoint_leagues.get_tournaments_for_league(league.id)[0]
    standings = endpoint_leagues.get_standings(tournament_id=tournament.id)[0]
    schedule = endpoint_events.get_schedule(league_id=league.id)
    live = endpoint_events.get_live()
    teams = endpoint_teams.get_teams(EXAMPLE_TEAM_ID)
    window = endpoint_match_details.get_window(EXAMPLE_GAME_ID)
    details = endpoint_match_details.get_details(EXAMPLE_GAME_ID)
```

## TODO

- Docstrings
- Finish wrapping EndpointEvents' api calls
- Sanitize data models. I'm going crazy with all these imports. I believe I can extend some models for other uses, like the "Team" model which is used in most endpoints. I should get which fields are common, and extend that base team model for other uses

## Credits
- [vickz84259's documentation](https://vickz84259.github.io/lolesports-api-docs/)
- [leolo's repo](https://gitlab.com/leolo/lolesports-api-python])
