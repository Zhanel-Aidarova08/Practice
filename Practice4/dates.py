# Date and time operations
# 1.Write a Python program to subtract five days from current date.
from datetime import datetime, timedelta

current_date = datetime.now()
new_date = current_date - timedelta(days=5)

print(new_date)

# Output example:
# 2026-02-14 21:35:10.123456
# (Дата будет зависеть от текущего времени)




# 2.Write a Python program to print yesterday, today, tomorrow.
from datetime import datetime, timedelta

today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)

# Output example:
# Yesterday: 2026-02-18 21:40:00.123456
# Today: 2026-02-19 21:40:00.123456
# Tomorrow: 2026-02-20 21:40:00.123456




# 3.Write a Python program to drop microseconds from datetime.
from datetime import datetime

now = datetime.now()
without_microseconds = now.replace(microsecond=0)

print(without_microseconds)

# Output example:
# 2026-02-19 21:45:30




# 4.Write a Python program to calculate two date difference in seconds.
from datetime import datetime

date1 = datetime(2026, 2, 19, 12, 0, 0)
date2 = datetime(2026, 2, 19, 12, 1, 30)

difference = date2 - date1
print(difference.total_seconds())

# Output:
# 90.0
