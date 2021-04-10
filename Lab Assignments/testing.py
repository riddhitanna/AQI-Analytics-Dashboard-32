''' input: enter the number of test cases you want to test and then for each test case,
input the date to be tested for each test case
assumptions: feb has 28 days
			 leap years are not considered

'''
print('NOTE: The date format followed is: DD/MM/YYYY. ')
n = int(input('Enter number of test cases : '))

#test_days = [31, 2, 5, 6, 32, 40, 11, 13, 25, 1]
#test_months = [12, 9, 8, 6, 5, 20, 23, 4, 1, 1]
#test_years = [1995, 1996, 2005, 2016, 1990, 2004, 2003, 2001, 2015 ,1900]


for i in range(n):
	print('Test case {} '.format(i+1))
	day = int(input('Enter the day: '))
	month = int(input('Enter the month: '))
	year = int(input('Enter the year: '))
	#day = test_days[i]
	#month = test_months[i]
	#year = test_years[i]
	if day<1 or day>31 or month<1 or month>12 or year<1900 or year>2015:
		print('Invalid')

	elif (month in [2, 4, 6, 9, 11] and day == 31):
		print('Invalid')

	elif (month == 2 and day > 28):
		print('Invalid')

	else:

		if day == 1:

			if month == 1:

				if year == 1900: # 01/01/1900
					print('Invalid')

				else:
					day = 31 
					month = 12
					year = year - 1
					print('{}/{}/{}'.format(day,month,year))


			elif month == 3:
				month = 2
				day = 28
				print('{}/{}/{}'.format(day,month,year))


			elif month in [5, 7, 10, 12]:
				month = month - 1
				day = 30
				print('{}/{}/{}'.format(day,month,year))

			else:
				day = 31
				month = month - 1
				print('{}/{}/{}'.format(day,month,year))

		else:
			day = day - 1
			print('{}/{}/{}'.format(day,month,year))

