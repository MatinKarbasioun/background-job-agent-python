from datetime import timedelta, datetime
import pytz

from src.application.app_setting import AppSetting
from src.domain.time import ScheduleTime


class JobDateTimeService:

    def __init__(self, start_time, end_time, timezone: str = "UTC", time_format: str = "%H:%M"):
        config = AppSetting.APP_SETTINGS['scheduling_conf']
        self.__start_time = config['daily_start_time']
        self.__end_time = config['marketEndTime']
        self.__timezone = config['timeZone']
        self.__time_format = config['time_format']
        self.__time_zone = pytz.timezone(self.__timezone)
        self.__time = datetime.now(tz=self.__time_zone).strftime(self.__time_format)

    def get_time(self) -> ScheduleTime:
        market_time = ScheduleTime(starTime=self.__start_time,
                                 endTime=self.__end_time,
                                 timeZone=self.__timezone)
        return market_time

    def _update_time(self):
        self.__time = datetime.now(tz=self.__time_zone).strftime(self.__time_format)

    def get_remaining_time_to_job_end(self) -> timedelta:
        return datetime.strptime(self.__end_time, self.__time_format) - datetime.strptime(self.__time, self.__time_format)

    def get_relative_remaining_time_to_job_end(self, time: str) -> timedelta:
        return datetime.strptime(self.__end_time, self.__time_format) - datetime.strptime(time, self.__time_format)

    def is_remain_time_to_end_of_job_time(self, time: str) -> bool:
        self._update_time()
        return self.__time < time

    def is_running_time(self) -> bool:
        self._update_time()
        return self.__start_time <= self.__time <= self.__end_time

    def is_started_time(self) -> bool:
        self._update_time()
        return self.__start_time < self.__time

    def is_ended_time(self) -> bool:
        self._update_time()
        return self.__end_time < self.__time