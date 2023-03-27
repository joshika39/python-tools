def time_to_decimal(time: tuple[int, int, int]):
	return time[0] + (time[1] / 60) + (time[2] / 3600)


def get_time():
	time = input("Time: ").split(" ")
	return int(time[0]), int(time[1]), int(time[2])


print(round(time_to_decimal(get_time()), 2))
