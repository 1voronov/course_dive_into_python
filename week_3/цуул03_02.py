import os
import csv


class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)
    
    car_type = None

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)
        self.car_type = 'car'


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        try:
            b_length, b_width, b_height = body_whl.split('x')
            self.body_width = float(b_width)
            self.body_height = float(b_height)
            self.body_length = float(b_length)
        except ValueError:
            self.body_width = 0.0
            self.body_height = 0.0
            self.body_length = 0.0
        self.car_type = 'truck'
        
    def get_body_volume(self):
        return self.body_width * self.body_height * self.body_length


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra
        self.car_type = 'spec_machine'


def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')
        next(reader)
        for row in reader:
            if row[0] not in ['car', 'truck', 'spec_machine'] \
                or row[1] == '' \
                or os.path.splitext(row[3])[1] == '' \
                or '.' in os.path.splitext(row[3])[0] \
                or row[5] == '':
                continue
            elif row[0] == 'car':
                if row[2] == '':
                    continue
                else:
                    car_list.append(Car(row[1], row[3], row[5], \
                                        row[2]))
            elif row[0] == 'truck':
                car_list.append(Truck(row[1], row[3], row[5], \
                                      row[4]))
            elif row[0] == 'spec_machine':
                if row[6] == '':
                    continue
                else: 
                    car_list.append(SpecMachine(row[1], row[3], row[5], \
                                                row[6]))
    return car_list
