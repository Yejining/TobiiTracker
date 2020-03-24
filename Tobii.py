import tobii_research as tr


class Tobii:
    def __init__(self):
        self.tobii = tr.find_all_eyetrackers()[0]
        self.data = GazeData()

    def run(self):
        self.tobii.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.data.gaze_data_callback, as_dictionary=True)

    def end(self):
        self.tobii.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.data.gaze_data_callback)


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
