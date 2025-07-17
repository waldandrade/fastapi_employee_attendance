from enum import Enum


class ScheduleMethod(Enum):
    SIX_HOURS_WITHOUT_BREAK = 'six_hours_without_break'
    EIGHT_HOURS_WITH_BREAK = 'eight_hours_with_break'


class AttendanceStatus(Enum):
    ENTERING = 'entering'
    PAUSE_STARTING = 'pausing'
    PAUSE_ENDING = 'backing'
    EXITING = 'exiting'
