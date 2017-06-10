# -*- coding:utf-8 -*-
import time


class Timer(object):
    def __enter__(self):
        self.__start = time.time()

    def __exit__(self, type, value, traceback):
        # Error handling here
        self.__finish = time.time()

    @property
    def duration_in_seconds(self):
        return self.__finish - self.__start

    @property
    def duration_in_ms(self):
        return (self.__finish - self.__start) * 1000


timer = Timer()
