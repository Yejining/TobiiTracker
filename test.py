import tobii_research as tr
import pandas as pd
import time
import os
from datetime import datetime


class GazeData:
    def __init__(self):
        self.display_area = []
        self.gaze_data = []

    def gaze_data_callback(self, gaze_data):
        self.gaze_data.append(gaze_data)


def get_eye_tracker():
    found_trackers = tr.find_all_eyetrackers()
    return found_trackers[0]


def get_display_area(eye_tracker):
    display_area = eye_tracker.get_display_area()


def collect_gaze_data(eye_tracker, duration):
    data = GazeData()
    eye_tracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, data.gaze_data_callback, as_dictionary=True)
    time.sleep(duration)
    eye_tracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, data.gaze_data_callback)
    return data


def save_data(data):
    path = os.path.dirname(os.path.realpath(__file__))
    path += "\\data\\" + datetime.today().strftime('%y%m%d%H%M%S') + ".csv"
    dataframe = pd.DataFrame(data.gaze_data)
    dataframe.to_csv(path, header=False, index=False)


def main():
    data = collect_gaze_data(get_eye_tracker(), 10)
    save_data(data)


if __name__ == "__main__":
    main()
