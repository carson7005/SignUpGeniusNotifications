# SignUpGeniusNotifications
A connection between SignupGenius and Canvas LMS to send updates to a certain course. 

## Config Template
```json
{
  "canvas_token": "str; Canvas LMS Token here",
  "default_canvas_course": "int; The Canvas Course ID for the announcements to be sent",
  "signup_genius_token": "str; SignUpGenius Token here",
  "daily_time": "str; Time time for the daily updates, in the format '%H:%M' (ex. 07:00, 13:30)",
  "hourly_minute": "str; Minute marker for the hourly updates, in the format ':%M' (ex. :05, :15)",
  "request_retries": "int; The amount of retry attempts for the SG API calls",
  "contacts": "[[str]]; The contacts for the notification string, formatted [['NAME', 'EMAIL'], ...]"
}
```
