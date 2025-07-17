from app.commons.enums import ScheduleMethod


def get_schedule_method(method: str):
    if method is not None:
        return ScheduleMethod(method)
    return None
