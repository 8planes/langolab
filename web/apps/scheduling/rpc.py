from scheduling import models, tasks
from datetime import date, datetime, timedelta

def save_schedule(request, utc_schedule, utc_year, utc_month, utc_day, num_hours):
    start_datetime = datetime(utc_year, utc_month, utc_day)
    end_datetime = start_datetime + timedelta(hours=num_hours)
    models.UserScheduleRange.objects.filter(
        user=request.user,
        start_time__lte=end_datetime,
        end_time__gte=start_datetime).delete()

    tasks.update_schedules.delay(
        request.user.id, date(utc_year, utc_month, utc_day), num_hours)

def fetch_schedule(request, native_languages, foreign_languages, utc_year, utc_month, utc_day, num_hours):
    pass
