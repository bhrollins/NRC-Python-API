#!/usr/bin/env python3

import src.nike_plus_api as api
import matplotlib.pyplot as plt

from typing import List
from src.run_metrics import RunMetrics

def add_figure(time=None, data=None, label='', ylabel=''):
    plt.figure()
    plt.plot(time, data, label=label)
    plt.ylabel(ylabel)
    plt.xlabel('date (UTC)')
    plt.legend(loc='upper right')


def get_summaries(uuids: List):
    summaries = RunMetrics()
    for uuid in uuids:
        run = api.NikeApiAllMetricsReq()
        run.get(uuid)

        run_parser = api.NikeApiAllMetricsParser(run)
        run_parser.parse()

        summaries.append(run_parser.metrics)

    return summaries


def main():
    activities = api.NikeApiActivitiesAfterTimeReq()
    activities.get(0)

    parser = api.NikeApiAfterTimeParser(activities)
    parser.parse_uuids()

    run_summaries = get_summaries(parser.activity_uuids)
    run_summaries.time_to_utc()

    add_figure(time=run_summaries.time_stamp, data=run_summaries.distance, label='distance', ylabel='miles')
    add_figure(time=run_summaries.time_stamp, data=run_summaries.pace, label='pace', ylabel='minutes/mile')
    add_figure(time=run_summaries.time_stamp, data=run_summaries.calories, label='calories', ylabel='kcal')
    add_figure(time=run_summaries.time_stamp, data=run_summaries.speed, label='speed', ylabel='miles/hour')
    add_figure(time=run_summaries.time_stamp, data=run_summaries.total_time, label='duration', ylabel='minutes')

    plt.show()

if __name__ == '__main__':
    main()
