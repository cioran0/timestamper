# keyword message.content is calc, precede with botcommand ! altered from $
import asyncio
import discord
from discord.ext import commands
import time

TOKEN = 'INSERT YOUR OWN TOKEN HERE OR IT WONT WORK BLANK FOR SECURITY'
bot = commands.Bot(command_prefix='!')
game = discord.Game('with your time')
tz = 'LOCALTIME'
err1 = 'ERROR That is not a number. Enter numbers please'
err2 = 'ERROR Value is too short. Please remember the leading zero on single digit months'
err3 = 'ERROR Value is too long. Year is 2 digits, not four'
err4 = 'ERROR Use slash marks in between dates'
err5 = 'ERROR Dates must be valid'
err6 = 'ERROR Values cannot be in the past'

@bot.event
async def on_ready():
	print('Logged in as:')
	print(bot.user.name)
	print(bot.user.id)
	print('--------')
	await bot.change_presence(status=discord.Status.online, activity=game)

#check # days for month is correct incl leap year
def is_valid_m(years, month, day):
	day_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	years = years + 2000
	if years < 2024: 
		years = years - 2000 #passed a reference and not a value
		return False
	if(
		years % 4 == 0 and 
   		(years % 100 != 0 or years % 400 == 0)
   	):
		day_month[2] = 29
	if(
		( 
		(month >=1 and month <= 12) and 
		(day >=1 and day <= day_month[month])
		)
	):
			years = years - 2000 #passed a reference and not a value
			return True
	else:
			years = years - 2000 #passed a reference and not a value
			return False
#check length mm-dd-yy so 2/24/24 is wrong and so is 02/24/2024, must be mm/dd/yy
def isitDate(v):
	lval = len(v)
	if(lval < 14):
		return [False,err2]
	elif(lval > 14):
		return [False, err3]
	else:
		return [True, 'None']
# avoid string problems incl empty strings in input checking by explicitly casting string slices to int
# check not letters somehow with isdigit
# TF returns false and returns with all 0's if anyone is false
def strAssign(val):
	s1 = val[0:2]
	print(s1.isdigit())
	if(s1.isdigit()):
		s1 = int(s1)
		TF = True
	else:
		TF = False
		return[0,0,0,0,0,TF]
	s2 = val[3:5]
	if(s2.isdigit()):
		s2 = int(s2)
		TF = False
	else:
		TF = False
		return[0,0,0,0,0,TF]
	s3 = val[6:8]
	if(s3.isdigit()):
		s3 = int(s3)
		TF = True
	else:
		TF = False
		return[0,0,0,0,0,TF]
	s4 = val[9:11]
	if(s4.isdigit()):
		s4 = int(s4)
		TF = True
	else:
		TF = False
		return[0,0,0,0,0,TF]
	s5 = val[12:14]
	if(s5.isdigit()):
		s5 = int(s5)
		TF = True
	else:
		TF = False
		return[0,0,0,0,0,TF]
	return[s1,s2,s3,s4,s5,TF]

def notBot(m):
	if m.author == bot.user:
		return False
	else:
		return True

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return
	await bot.process_commands(message)

#main
@bot.command(aliases=['calc']) #alias = !calc, change as needed
async def calculate(ctx, message=None, validDate=False):
	#calculate current times
	epo = time.time()
	cur1 = time.strftime("%a, %d %b %Y %H:%M", time.localtime(epo))
	gmt =  time.strftime("%a, %d %b %Y %H:%M", 
					 time.gmtime(epo))
	await ctx.send (f'Current time is: \n \t {cur1} {tz} \n \t {gmt} UTC')
	await ctx.send('Type \"quit\" at any time to quit the calculator.')
	while not validDate: #re-enter as long as things are false e.g. date's wrong
		await ctx.send('Enter a future value for the date to convert to timestamp in 24h local time mm-dd-yy e.g 12/25/24 14:00')
		try:
			value = await bot.wait_for('message', timeout=60) #times out after a minute
			if value.content == 'quit':
				await ctx.send('Quitting calculator program.')
				return
			dateErr = isitDate(value.content)
			print("DateErr", dateErr) #diag
			if(dateErr[0] == False):
				validDate = False
				await ctx.send(dateErr[1])
			else: #date is proper length acc to dateErr isitdate return
				value = (value.content)
				try:
					s = strAssign(value)
				except:
					await ctx.send(err1)
				if s[5] == True: #check if Letters
					if not is_valid_m(s[2],s[0],s[1]): #check date makes sense 30/31 day leap year etc				
						await ctx.send(err5)
						validDate = False
					else:
						try:
							strip = time.strptime(value, "%m/%d/%y %H:%M") # diag 2
							validDate = True
							mkv = round(time.mktime(strip)) #rounded epoch time
							await ctx.send(f'Timestamp is  `<t:{mkv}>` which shows as <t:{mkv}> ')
						except:
							await ctx.send('That is not valid. Please enter a valid future date in mm/dd/yy hh:mm format')
				else:
					await ctx.send(err1) #not a number
					validDate = False
		except asyncio.TimeoutError:
			await ctx.send('You took too long! Program terminated.')
			return
	await ctx.send('Thanks for using Ciorans timestamper. Goodbye')
	





bot.run(TOKEN)
