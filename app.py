# Application
import datetime
import calendar
class MeetingScheduler:
    def __init__(self, working_hours=(9, 17), holidays=None):
        self.working_hours = working_hours
        self.holidays = holidays if holidays else []
        self.schedule = {}
    def is_working_day(self, date):
        return date.weekday() < 5 and date not in self.holidays
    def is_time_slot_available(self, user, start_time, end_time):
        if user not in self.schedule:
            return True
        for meeting in self.schedule[user]:
            if (start_time < meeting[1] and end_time > meeting[0]):
                return False
        return True
    def schedule_meeting(self, user, date, start_hour, end_hour):
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        start_time = datetime.datetime.combine(date, datetime.time(start_hour))
        end_time = datetime.datetime.combine(date, datetime.time(end_hour))
        if not self.is_working_day(date):
            return f"{date} is not a working day."
        if not self.is_time_slot_available(user, start_time, end_time):
            return "Time slot is not available."
        if user not in self.schedule:
            self.schedule[user] = []
        self.schedule[user].append((start_time, end_time))
        return f"Meeting scheduled for {user} on {date} from {start_hour}:00 to {end_hour}:00."
    def check_available_slots(self, user, date):
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        if not self.is_working_day(date):
            return f"{date} is not a working day."
        available_slots = []
        start_of_day = datetime.datetime.combine(date, datetime.time(self.working_hours[0]))
        end_of_day = datetime.datetime.combine(date, datetime.time(self.working_hours[1]))
        if user in self.schedule:
            booked_slots = self.schedule[user]
            booked_slots.sort()  # Sort by start time
            last_end_time = start_of_day
            for meeting in booked_slots:
                if last_end_time < meeting[0]:
                    available_slots.append((last_end_time, meeting[0]))
                last_end_time = max(last_end_time, meeting[1])
            if last_end_time < end_of_day:
                available_slots.append((last_end_time, end_of_day))
        else:
            available_slots.append((start_of_day, end_of_day))
        return available_slots
    def view_scheduled_meetings(self, user):
        if user not in self.schedule or not self.schedule[user]:
            return "No scheduled meetings."
        return self.schedule[user]
if __name__ == "__main__":
    holidays = [datetime.date(2025, 1, 1), datetime.date(2025, 12, 25)]  # New Year's Day and Christmas
    scheduler = MeetingScheduler(holidays=holidays)
    print(scheduler.schedule_meeting("Migule", "2025-03-18", 10, 11))
    print(scheduler.schedule_meeting("Migule", "2025-04-18", 11, 12))  # Should succeed
    print(scheduler.schedule_meeting("Migule", "2025-05-18", 10, 11))  # Should fail (overlap)
    available_slots = scheduler.check_available_slots("Migule", "2025-05-18")
    print("Available slots for Migule on 2025-05-18:", available_slots)
    meetings = scheduler.view_scheduled_meetings("Migule")
    print("Scheduled meetings for Migule:", meetings)
