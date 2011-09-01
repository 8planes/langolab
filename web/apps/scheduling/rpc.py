from scheduling import models, tasks
from datetime import date, datetime, timedelta

def save_schedule(request, utc_schedule, utc_year, utc_month, utc_day, num_hours):
    start_datetime = datetime(utc_year, utc_month, utc_day)
    end_datetime = start_datetime + timedelta(hours=num_hours)
    models.UserScheduleRange.objects.filter(
        user=request.user,
        start_time__lte=end_datetime,
        end_time__gte=start_datetime).delete()
    for range in utc_schedule:
        start = range['start']
        end = range['end']
        start_time = datetime(start[0], start[1], start[2], start[3])
        end_time = datetime(end[0], end[1], end[2], end[3])
        models.UserScheduleRange(
            user=request.user,
            start_time=start_time,
            end_time=end_time).save()
    tasks.update_schedules.delay(
        request.user.id, datetime(utc_year, utc_month, utc_day), 
        num_hours)

def fetch_schedule(request, native_languages, foreign_languages, utc_year, utc_month, utc_day, num_hours):
    start_date = datetime(utc_year, utc_month, utc_day)
    end_date = start_date + timedelta(hours=num_hours - 1)
    start_hour = models.LanguagePairUserCount.hour_for_date(start_date)
    end_hour = models.LanguagePairUserCount.hour_for_date(end_date)
    hour_dicts = []
    for native_language in native_languages:
        for foreign_language in foreign_languages:
            schedules_qs = models.LanguagePairUserCount.objects.filter(
                hour__gte=start_hour,
                hour__lte=end_hour,
                native_language=native_language,
                foreign_language=foreign_language).all()
            hour_dicts.append(
                dict([(str(s.hour), s.user_count) for s in schedules_qs]))
    schedule = [0] * (end_hour - start_hour + 1)
    for hour in range(start_hour, end_hour + 1):
        str_hour = str(hour)
        for hour_dict in hour_dicts:
            if str_hour in hour_dict:
                schedule[hour - start_hour] += hour_dict[str_hour]
    return schedule
