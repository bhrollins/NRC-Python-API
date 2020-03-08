from dataclasses import dataclass, field
from datetime import datetime
from typing import List

#################################  constants  ##################################

# minutes/kilometer to minutes/mile
MKM_TO_MM   = 1.60934
# kilometers to miles
KM_TO_MILES = 0.621371
# kilometers/hour to miles/hour
KMH_TO_MPH  = KM_TO_MILES
# milliseconds to minutes
MS_TO_MIN   = 1.66667e-5

###################################  macros  ###################################

min_per_km_to_min_per_mile = lambda x: x * MKM_TO_MM
km_to_miles = lambda x: x * KM_TO_MILES
kmph_to_mph = lambda x: x * KMH_TO_MPH
ms_to_min   = lambda x: x * MS_TO_MIN
ts_to_date  = lambda x: datetime.utcfromtimestamp(x * 1e-3).strftime('%Y-%m-%d %H:%M:%S')

###################################  types  ####################################

# units can be grabbed from API, but
#   for now we'll assume they're constant
@dataclass
class RunMetric:
    time_stamp: int   = 0   # ms
    total_time: float = 0.0 # seconds
    pace:       float = 0.0 # MKM
    calories:   float = 0.0 # KCAL
    distance:   float = 0.0 # KM
    speed:      float = 0.0 # KMH

@dataclass
class RunMetrics:
    time_stamp: List = field(default_factory=lambda: [])
    total_time: List = field(default_factory=lambda: [])
    pace:       List = field(default_factory=lambda: [])
    calories:   List = field(default_factory=lambda: [])
    distance:   List = field(default_factory=lambda: [])
    speed:      List = field(default_factory=lambda: [])

    def append(self, metric: RunMetric):
        self.time_stamp += [metric.time_stamp]
        self.total_time += [metric.total_time]
        self.pace       += [metric.pace]
        self.calories   += [metric.calories]
        self.distance   += [metric.distance]
        self.speed      += [metric.speed]

    def time_to_utc(self):
        self.time_stamp = list(map(ts_to_date, self.time_stamp))
