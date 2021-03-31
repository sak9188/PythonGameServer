# -*- coding: UTF-8 -*-

import time


class GameTime(object):

    def __init__(self, time_resolution=0.001):
        # 与当前时间的差值
        self.offset_time = 0.0
        # self.time_stamp = time.time()
        self.stop_time = None
        # 服务器最小时间精度
        if time_resolution > 0.1:
            time_resolution = 0.1
        self.time_span = time_resolution
        # 时间同步流逝比率
        self.time_rate = 1
        # 时间加速比率
        # TODO

    def __call__(self):
        "返回时间戳"
        return time.time() - self.offset_time
    
    def __enter__(self):
        self.stop()

    def __exit__(self):
        self.start()

    def stop(self):
        "暂停时间"
        self.stop_time = time.time()
        pass

    def start(self):
        now = time.time()
        new_offset = now - self.stop_time
        self.offset_time += new_offset
        self.update_time_rate()

    def update_time_rate(self):
        # 设置服务器时间流逝速率，根据差时来确定流逝速率
        if self.offset_time > 3600:
            # 如果慢了一个小时的话， 每次更新时间大约是 102.4s（1ms精度）
            self.time_rate = 102400
        elif self.offset_time > 600:
            # 如果在1小时到10分钟以内的话， 每次更新时间大约是 25.6s（1ms精度）
            self.time_rate = 25600
        elif self.offset_time > 60:
            # 如果在10分钟到1分钟以内的话，每次更新时间大约是 2.56s（1ms精度）
            self.time_rate = 2560
        elif self.offset_time > 1:
            #如果在1分钟到1s钟以内的话，   每次更新时间大约是 0.064s（1ms精度）
            self.time_rate = 64
        elif self.offset_time > 0.1:
            # 如果在1s到100ms钟以内的话， 每次更新时间大约是 0.032s（1ms精度）
            self.time_rate = 32
        elif self.offset_time > 0.01:
            # 如果在100ms到10ms钟以内的话， 每次更新时间大约是 0.008s（1ms精度）
            self.time_rate = 8
        else:
            # 如果在10ms以内的话， 每次更新时间大约是最小精度（1ms精度）
            self.time_rate = 1

    def sync_real_time(self):
        "同步真实世界的时间，并且返回给服务器当前时间"
        if self.offset_time > 0:
            time_span = self.time_rate * self.time_span
            self.offset_time -= time_span
            self.update_time_rate()
        return self.__call__()

        