from datetime import datetime
from .models import *

# def searching_for_next_match(matches:list[Match]) -> Match:
#     date_today = datetime.now().astimezone()
#     next_match = None
#     for match in matches:
#         match_datetime = datetime.combine(match.match_date, match.match_time)
#         match_datetime_tz = match_datetime.astimezone()
#         if match_datetime_tz > date_today:
#             if next_match is None or match.match_date < next_match.match_date:
#                 next_match = match

#     return next_match

def searching_for_next_matches(matches:list[Match]) -> list[Match]:
    date_today = datetime.now().astimezone()
    next_matches = []
    for match in matches:
        match_datetime = datetime.combine(match.match_date, match.match_time)
        match_datetime_tz = match_datetime.astimezone()
        if match_datetime_tz > date_today:
                next_matches.append(match)

    return next_matches

# def searching_for_last_match(matches:list[Match]) -> Match:
#     date_today = datetime.now().astimezone()
#     last_match = None
#     for match in matches:
#         match_datetime = datetime.combine(match.match_date, match.match_time)
#         match_datetime_tz = match_datetime.astimezone()
#         if match_datetime_tz < date_today:
#             if last_match is None:
#                 last_match = match
#             else:
#                 last_match_datetime = datetime.combine(last_match.match_date, last_match.match_time)
#                 if last_match is None or match_datetime > last_match_datetime:
#                     last_match = match

#     return last_match

def match_history(matches:list[Match]) -> list[Match]:
    date_today = datetime.now().astimezone()
    match_history = []
    for match in matches:
        match_datetime = datetime.combine(match.match_date, match.match_time)
        match_datetime_tz = match_datetime.astimezone()
        if match_datetime_tz < date_today:
            match_history.append(match)
            
    return match_history