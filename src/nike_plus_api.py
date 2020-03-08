import json
import requests

from src.bearer import bearer
import src.run_metrics as metrics

NIKE_API_BASE = 'https://api.nike.com/sport/v3/me/'

######################  endpoints for getting activities  ######################
# param: integer (unix time epoch)
NIKE_API_AFTER_TIME = NIKE_API_BASE + 'activities/after_time/{}'
# param: activity uuid
NIKE_API_AFTER_ID   = NIKE_API_BASE + 'activities/after_id/{}'

###############  endpoints for grabbing metrics from activities  ###############
# param: activity uuid
NIKE_API_ALL_METRICS = NIKE_API_BASE + 'activity/{}?metrics=ALL'

######################  api request authorization header  ######################
HEADERS = {'Authorization': 'Bearer {}'.format(bearer)}

class NikeApiReq(object):
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.response = ''
    
    def get(self, arg):
        try:
            self.response = requests.get(self.endpoint.format(arg), headers=HEADERS)
        except requests.exceptions.HTTPError as e:
            print('HTTP GET error: {}'.format(e))

        if not self.response.ok:
            print('HTTP GET Failed: {}'.format(self.response.status_code))
            print(' Check \"Bearer\" authorization token validity '.center(60, '*'))
            return False
        
        return True


class NikeApiActivitiesAfterTimeReq(NikeApiReq):
    def __init__(self):
        super().__init__(NIKE_API_AFTER_ID)
    
    def get(self, arg: str):
        super().get(arg)


# TODO: implement parser for this request type
#       to accomodate a paging check in initial
#       `NikeApiActivitiesAfterTimeReq`
class NikeApiActivitiesAfterUUIDReq(NikeApiReq):
    def __init__(self):
        super().__init__(NIKE_API_AFTER_TIME)
    
    def get(self, arg: int):
        super().get(arg)


class NikeApiAllMetricsReq(NikeApiReq):
    def __init__(self):
        super().__init__(NIKE_API_ALL_METRICS)
    
    def get(self, arg: str):
        super().get(arg)


class NikeApiParser(object):
    def __init__(self, req: NikeApiReq):
        self.req  = req
        self.resp = req.response.json()

    def parse(self):
        pass


class NikeApiAfterTimeParser(NikeApiParser):
    def __init__(self, req: NikeApiActivitiesAfterTimeReq):
        super().__init__(req)
        self.activity_uuids = []

    def parse_uuids(self):

        try:
            activities = self.resp['activities']
        except KeyError:
            print('Either request error or format changed')
            return

        for activity in activities:
            try:
                self.activity_uuids += [activity['id']]
            except KeyError:
                # TODO: handle this
                print('Either request type error or format changed')


class NikeApiAllMetricsParser(NikeApiParser):
    def __init__(self, req: NikeApiAllMetricsReq):
        super().__init__(req)
        self.metrics = metrics.RunMetric()
    
    def parse(self):

        try:
            start = self.resp['start_epoch_ms']
            end   = self.resp['end_epoch_ms']
        except KeyError:
            print('Unable to extract time stamps')
        
        self.metrics.time_stamp = start
        self.metrics.total_time = metrics.ms_to_min(end-start)

        try:
            summaries = self.resp['summaries']
        except KeyError:
            # TODO: handle better
            print('Invalid API response')
            return

        for summary in summaries:
            try:
                metric = summary['metric']
            except KeyError:
                print('Invalid API response')
                continue

            if metric == 'speed':
                try:
                    self.metrics.speed = metrics.kmph_to_mph(summary['value'])
                except KeyError:
                    print('Unable to parse out speed value, incorrect response type?')
            elif metric == 'pace':
                try:
                    self.metrics.pace = metrics.min_per_km_to_min_per_mile(summary['value'])
                except KeyError:
                    print('Unable to parse out pace value, incorrect response type?')
            elif metric == 'calories':
                try:
                    self.metrics.calories = summary['value']
                except KeyError:
                    print('Unable to parse out calories value, incorrect response type?')
            elif metric == 'distance':
                try:
                    self.metrics.distance = metrics.km_to_miles(summary['value'])
                except KeyError:
                    print('Unable to parse out distance value, incorrect response type?')
