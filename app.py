# Application
from datetime import datetime, timedelta
import calendar
class MeetingScheduler:
    def __init__(self):
        self.working_hours_start = 9
        self.working_hours_end = 17
        self.public_holidays = {
            "01-01": "New Year's Day",
            "12-25": "Christmas",
            "07-04": "Independence Day"
        }
        self.users_meetings = {}
    def is_working_day(self, date: datetime):
        """Check if the given date is a working day (not a weekend or holiday)."""
        day_of_week = date.weekday() 
        if day_of_week >= 5: 
            return False
        date_str = date.strftime("%m-%d")
        if date_str in self.public_holidays:
            return False
        return True
    def schedule_meeting(self, user: str, meeting_date: datetime, duration_minutes: int):
        """Schedule a meeting for a user."""
        if not self.is_working_day(meeting_date):
            print(f"Cannot schedule meeting on {meeting_date.strftime('%Y-%m-%d')}, it's not a working day.")
            return False
        if not (self.working_hours_start <= meeting_date.hour < self.working_hours_end):
            print(f"Meeting time must be within working hours ({self.working_hours_start}:00 to {self.working_hours_end}:00).")
            return False
        if user not in self.users_meetings:
            self.users_meetings[user] = []
        for existing_meeting in self.users_meetings[user]:
            existing_start, existing_end = existing_meeting
            if not (meeting_date + timedelta(minutes=duration_minutes) <= existing_start or meeting_date >= existing_end):
                print(f"Meeting time overlaps with an existing meeting from {existing_start} to {existing_end}.")
                return False
        meeting_end = meeting_date + timedelta(minutes=duration_minutes)
        self.users_meetings[user].append((meeting_date, meeting_end))
        self.users_meetings[user] = sorted(self.users_meetings[user])  # Sort by meeting start time
        print(f"Meeting scheduled for {user} on {meeting_date.strftime('%Y-%m-%d %H:%M:%S')} for {duration_minutes} minutes.")
        return True
    def check_available_slots(self, user: str, date: datetime):
        """Show available time slots for the given date."""
        available_slots = []
        if user not in self.users_meetings:
            self.users_meetings[user] = []
        for hour in range(self.working_hours_start, self.working_hours_end):
            for minute in [0, 30]:
                meeting_start = datetime(date.year, date.month, date.day, hour, minute)
                meeting_end = meeting_start + timedelta(minutes=30)  # Default duration is 30 minutes
                if self.is_working_day(meeting_start) and all(
                    not (meeting_start < end and meeting_end > start)
                    for start, end in self.users_meetings[user]
                ):
                    available_slots.append(meeting_start.strftime("%H:%M"))
        if available_slots:
            print(f"Available slots for {user} on {date.strftime('%Y-%m-%d')}: {', '.join(available_slots)}")
        else:
            print(f"No available slots for {user} on {date.strftime('%Y-%m-%d')}.")
    def view_scheduled_meetings(self, user: str):
        """Display scheduled meetings for a user."""
        if user not in self.users_meetings:
            print(f"No meetings scheduled for {user}.")
            return 
        print(f"Scheduled meetings for {user}:")
        for start, end in self.users_meetings[user]:
            print(f"- From {start.strftime('%Y-%m-%d %H:%M:%S')} to {end.strftime('%Y-%m-%d %H:%M:%S')}")
scheduler = MeetingScheduler()
scheduler.schedule_meeting("Migule", datetime(2025, 3, 16, 10, 0), 60)
scheduler.schedule_meeting("Migule", datetime(2025, 2, 17, 11, 0), 30)  
scheduler.check_available_slots("Migule", datetime(2025, 3, 16))
scheduler.view_scheduled_meetings("Migule")
