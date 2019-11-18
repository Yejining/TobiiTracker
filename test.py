import tobii_research as tr
import pandas as pd
import time
import os
import numpy as np
import math
from datetime import datetime
import matplotlib.pyplot as plt


class GazeData:
    def __init__(self):
        self.left_gaze_point_in_user_coordinate_system = []
        self.right_gaze_point_in_user_coordinate_system = []
        self.left_gaze_point_on_display_area = []
        self.right_gaze_point_on_display_area = []
        self.left_gaze_origin_in_user_coordinate_system = []
        self.right_gaze_origin_in_user_coordinate_system = []
        self.left_gaze_origin_in_trackbox_coordinate_system = []
        self.right_gaze_origin_in_trackbox_coordinate_system = []
        self.left_gaze_point_validity = []
        self.right_gaze_point_validity = []
        self.left_gaze_origin_validity = []
        self.right_gaze_origin_validity = []
        self.device_time_stamp = []
        self.movement_type = []
        self.count = 0

    def gaze_data_callback(self, gaze_data):
        self.left_gaze_point_in_user_coordinate_system.append(gaze_data['left_gaze_point_in_user_coordinate_system'])
        self.right_gaze_point_in_user_coordinate_system.append(gaze_data['right_gaze_point_in_user_coordinate_system'])
        self.left_gaze_point_on_display_area.append(gaze_data['left_gaze_point_on_display_area'])
        self.right_gaze_point_on_display_area.append(gaze_data['right_gaze_point_on_display_area'])
        self.left_gaze_origin_in_user_coordinate_system.append(gaze_data['left_gaze_origin_in_user_coordinate_system'])
        self.right_gaze_origin_in_user_coordinate_system.append(gaze_data['right_gaze_origin_in_user_coordinate_system'])
        self.left_gaze_origin_in_trackbox_coordinate_system.append(gaze_data['left_gaze_origin_in_trackbox_coordinate_system'])
        self.right_gaze_origin_in_trackbox_coordinate_system.append(gaze_data['right_gaze_origin_in_trackbox_coordinate_system'])
        self.left_gaze_point_validity.append(gaze_data['left_gaze_point_validity'])
        self.right_gaze_point_validity.append(gaze_data['right_gaze_point_validity'])
        self.left_gaze_origin_validity.append(gaze_data['left_gaze_origin_validity'])
        self.right_gaze_origin_validity.append(gaze_data['right_gaze_origin_validity'])
        self.device_time_stamp.append(gaze_data['device_time_stamp'])
        self.movement_type.append(0)
        self.count += 1

    # 사용 안 함
    def csv_format(self):
        result = []
        for left, right, stamp in zip(self.left_gaze_point, self.right_gaze_point, self.device_time_stamp):
            data = []
            data.append(left[0])
            data.append(left[1])
            data.append(right[0])
            data.append(right[1])
            data.append(stamp)
            result.append(data)
        return result

    # 사용 안 함
    def header(self):
        header = []
        header.append('left_gaze_point')
        header.append('right_gaze_point')
        header.append('time_stamp')


class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def subtract(self, point):
        return Point3D(self.x - point.x, self.y - point.y, self.z - point.z)


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
    dictionary = {
        'left_gaze_point_in_user_coordinate_system' : data.left_gaze_point_in_user_coordinate_system,
        'right_gaze_point_in_user_coordinate_system' : data.right_gaze_point_in_user_coordinate_system,
        'left_gaze_point_on_display_area' : data.left_gaze_point_on_display_area,
        'right_gaze_point_on_display_area': data.right_gaze_point_on_display_area,
        'left_gaze_origin_in_user_coordinate_system': data.left_gaze_origin_in_user_coordinate_system,
        'right_gaze_origin_in_user_coordinate_system': data.right_gaze_origin_in_user_coordinate_system,
        'left_gaze_origin_in_trackbox_coordinate_system': data.left_gaze_origin_in_trackbox_coordinate_system,
        'right_gaze_origin_in_trackbox_coordinate_system': data.right_gaze_origin_in_trackbox_coordinate_system,
        'left_gaze_point_validity': data.left_gaze_point_validity,
        'right_gaze_point_validity': data.right_gaze_point_validity,
        'left_gaze_origin_validity': data.left_gaze_origin_validity,
        'right_gaze_origin_validity': data.right_gaze_origin_validity,
        'device_time_stamp' : data.device_time_stamp
    }
    dataframe = pd.DataFrame(dictionary)
    dataframe.to_csv(path)


def subtract_time(time_stamp, start, end):
    return (time_stamp[end] - time_stamp[start]) % 10000000


# left만 구함
def get_velocity_between_two_points(current_data, next_data):
    current_point = Point3D(current_data[0], current_data[1], current_data[2])
    next_point = Point3D(next_data[0], next_data[1], next_data[2])

    subtracted = current_point.subtract(next_point)
    return np.sqrt(np.power(subtracted.x, 2) + np.power(subtracted.y, 2) + np.power(subtracted.z, 2))


def get_length_of_vector(vector):
    return np.sqrt(np.power(vector.x, 2) + np.power(vector.y, 2) + np.power(vector.z, 2))


def normalize_vector(sample_position, single_eye_coordinate):
    sample = Point3D(sample_position[0], sample_position[1], sample_position[2])
    point = Point3D(single_eye_coordinate[0], single_eye_coordinate[1], single_eye_coordinate[2])
    vector = Point3D(sample.x - point.x, sample.y - point.y, sample.z - point.z)

    length = get_length_of_vector(vector)
    return Point3D(vector.x/length, vector.y/length, vector.z/length)


def dot_product(left, right):
    return (left.x * right.x) + (left.y * right.y) + (left.z * right.z)


def get_angle(start_vector, end_vector):
    cosine = dot_product(start_vector, end_vector) / (get_length_of_vector(start_vector) * get_length_of_vector(end_vector))
    cosine = min(1, max(-1, cosine))
    return math.acos(cosine)


def get_angular_distance(gaze_data, sample, start, end):
    sample_position = gaze_data.left_gaze_origin_in_user_coordinate_system[sample]
    start_point = gaze_data.left_gaze_point_in_user_coordinate_system[start]
    end_point = gaze_data.left_gaze_point_in_user_coordinate_system[end]
    start_vector = normalize_vector(sample_position, start_point)
    end_vector = normalize_vector(sample_position, end_point)
    if math.isnan(start_vector.x) or math.isnan(end_vector.x): return 0
    angle_radian = get_angle(start_vector, end_vector)
    # print("start vector" + str(start_vector.x), str(start_vector.y), str(start_vector.z), end=' ')
    # print("end vector" + str(end_vector.x), str(end_vector.y), str(end_vector.z), end=' ')
    # print("sample" + str(sample), end=' ')
    # print("start" + str(start), end=' ')
    # print("end" + str(end), end=' ')
    # print("radian:" + str(angle_radian), end=' ')
    angle_degree = math.degrees(angle_radian)
    # print("degree:" + str(angle_degree))
    return angle_degree


def get_fixation_and_saccade(gaze_data):
    fixation = []
    saccade = []
    for i in range(gaze_data.count):
        if gaze_data.movement_type[i] == 1:
            fixation.append(i)
        elif gaze_data.movement_type[i] == 2:
            saccade.append(i)
    return fixation, saccade


def final_result(gaze_data, fixation):
    result = []
    centroid = []
    centroid_time = []

    # for i in range(len(fixation)):


def scatter_plot(gaze_data, fixation, saccade):
    fixation_coordinate = [gaze_data.left_gaze_point_in_user_coordinate_system[index] for index in fixation]
    saccade_coordinate = [gaze_data.left_gaze_point_in_user_coordinate_system[index] for index in saccade]
    plt.scatter([sac[0] for sac in saccade_coordinate], [sac[1] for sac in saccade_coordinate], color='black', alpha=0.5)
    plt.scatter([fix[0] for fix in fixation_coordinate], [fix[1] for fix in fixation_coordinate], color='red', alpha=0.5)
    # plt.scatter([p[0] for p in saccadepoints], [p[1] for p in saccadepoints], color='black', alpha=0.5)
    # plt.scatter([p[0] for p in fixpoints], [p[1] for p in fixpoints], color='red', alpha=0.5)
    # RADIUS = 10
    #
    # #     pyplot.plot(data[:,[0]], data[:,[1]])
    # pp = [p[0] for p in centers[1]]
    # for point in pp:
    #     plt.scatter(point[0], point[1], color='yellow')
    #     center = plt.Circle((point[0], point[1]), RADIUS, fill=False, color='blue')
    #     plt.gcf().gca().add_artist(center)
    plt.title("Fixtation detected")
    plt.xlabel("X axis")
    plt.ylabel("Y axis")
    plt.show()



def main():
    gaze_data = collect_gaze_data(get_eye_tracker(), 5)
    save_data(gaze_data)

    # for i in range(gaze_data.count - 1):
    #     current_data = gaze_data.left_gaze_origin_in_user_coordinate_system[i]
    #     next_data = gaze_data.right_gaze_origin_in_user_coordinate_system[i + 1]
    #
    #     velocity = get_velocity_between_two_points(current_data, next_data)

    buffer = []
    amplitude = []
    i = 0
    eye_velocities = []
    median = 0
    while True:
        if i + 1 < gaze_data.count:
            buffer.append(i)
            amplitude.append(get_angular_distance(gaze_data, buffer[len(buffer) - 2], buffer[len(buffer) - 2], buffer[len(buffer) - 1]))
            median = math.floor(len(buffer) / 2)
            i += 1
        window = (subtract_time(gaze_data.device_time_stamp, buffer[0], buffer[len(buffer) - 1])) / 1000000
        if window < 1 and i + 1 >= gaze_data.count: break
        if window > 1:
            velocity = sum(amplitude) / window
            eye_velocities.append(velocity, buffer[median])
            # print(sum(amplitude), end=' ')
            # print(window, end=' ')
            # print(velocity)
            if velocity < 30:
                gaze_data.movement_type[buffer[0]] = 1  # fixation
                # print(buffer[0])
            else:
                gaze_data.movement_type[buffer[0]] = 2  # saccade
            amplitude.pop(0)
            buffer.pop(0)

    fixation, saccade = get_fixation_and_saccade(gaze_data)
    scatter_plot(gaze_data, fixation, saccade)





if __name__ == "__main__":
    main()
