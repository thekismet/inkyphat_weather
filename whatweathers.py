#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import glob
from inky import InkyWHAT
from PIL import Image, ImageFont, ImageDraw
import datetime
import time
from datetime import date, timedelta
from darksky import forecast
import textwrap
from font_source_serif_pro import SourceSerifProSemibold
from font_source_sans_pro import SourceSansProSemibold

# set the colour of the phat: black, red or yellow
inky_display = InkyWHAT('yellow')

# set lat/long for location
LOCATION = 37.5683,126.9778 #put your longitude and latittude here in decimal degrees
UNITS = 'auto' #specify the units you want your results in here, see the Dark Sky API docs page for details

# set Darksky API Key
APIKEY= 'xxxxxxxxxx' # put your Dark Sky API key here. Get one at https://darksky.net/dev

# Get data from DarkSky
with forecast (APIKEY, *LOCATION, units=UNITS) as location:
    # today
    currentTemp = location['currently']['temperature']
    upcoming_conditions = location['hourly']['summary']
    relativeHumidity = location['currently']['humidity']
    highTemp = location['daily']['data'][0]['temperatureHigh']
    lowTemp = location['daily']['data'][0]['temperatureLow']
    iconDesc = location['currently']['icon']

    # tomorrow
    summary2 = location['daily']['data'][1]['summary']
    iconDesc2 = location['daily']['data'][1]['icon']
    highTemp2 = location['daily']['data'][1]['temperatureHigh']
    lowTemp2 = location['daily']['data'][1]['temperatureLow']

# format today's variables, current temp and high and low temps for the day
#in both Celcius and Fahrenheit for old-timers and Americans
temp = '{0:.0f}'.format(currentTemp) + 'C'
currentTempF = round((1.8 * currentTemp) + 32)
tempF = str(currentTempF) + 'F'
tempsToday = 'High ' + '{0:.0f}'.format(highTemp) + ' Low ' + '{0:.0f}'.format(lowTemp)

# format tomorrow's variables
tempsDay2 = 'High ' + '{0:.0f}'.format(highTemp2) + ' Low ' + '{0:.0f}'.format(lowTemp2)

# Create a new blank image, img, of type P
# that is the width and height of the Inky pHAT display,
# then create a drawing canvas, draw, to which we can draw text and graphics
img = Image.new('P', (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

# import the fonts and set sizes
bbig_font = ImageFont.truetype(SourceSerifProSemibold, 24)
big_font = ImageFont.truetype(SourceSansProSemibold, 24)
medium_font = ImageFont.truetype(SourceSansProSemibold, 18)

# define weekday text
weekday = date.today()
day_Name = date.strftime(weekday, '%A')
day_month_year = time.strftime('%H:%M %B %-d %Y')

weekday2 = datetime.date.today() + datetime.timedelta(days=1)
day2 = date.strftime(weekday2, '%A')

# format the summary texts for today and tomorrow
currentCondFormatted = textwrap.fill(upcoming_conditions, 25)
summary2Formatted = textwrap.fill(summary2, 25)

# draw some lines to box out tomorrow's forecast
# draw.line((118, 50, 118, 104),2, 4)
# draw.line((118, 50, 212, 50),2, 4)

# draw today's name on top left side
draw.text((15, 15), day_Name, inky_display.BLACK, big_font)

# draw today's date on left side below today's name
dayDate = day_month_year
draw.text((15, 45), dayDate, inky_display.BLACK, big_font)

#draw current temperature to right of day name and date
draw.text((280, 15), temp, inky_display.BLACK, big_font)
#draw.text((105, 34), tempF, inky_display.BLACK, font)

# draw today's high and low temps to center on left side below date
w, h = medium_font.getsize(tempsToday)
x_temps = (inky_display.WIDTH / 4) - (w / 2)
draw.text((15, 80), tempsToday, inky_display.BLACK, medium_font)

# draw the current summary and conditions on the left side of the screen
draw.text((15, 100), currentCondFormatted, inky_display.BLACK, medium_font)

# draw tomorrow's forecast in lower right box
draw.text((225, 110), day2, inky_display.BLACK, medium_font)
draw.text((225, 130), tempsDay2, inky_display.BLACK, medium_font)
draw.text((225, 150), summary2Formatted, inky_display.BLACK, medium_font)

# prepare to draw the icon on the upper right side of the screen
# Dictionary to store the icons
icons = {}

# build the dictionary 'icons'
for icon in glob.glob('/home/pi/inkyweather/weather-icons/icon-*.png'):
    # format the file name down to the text we need
    # example: 'icon-fog.png' becomes 'fog'
    # and gets put in the libary
    icon_name = icon.split('icon-')[1].replace('.png', '')
    icon_image = Image.open(icon)
    icons[icon_name] = icon_image

# Draw the current weather icon top in top right
if iconDesc is not None:
    img.paste(icons[iconDesc], (320, 15))
else:
    draw.text((320, 15), '?', inky_display.YELLOW, big_font)


# set up the image to push it
inky_display.set_image(img)
inky_display.set_border(inky_display.YELLOW)

inky_display.h_flip = True
inky_display.v_flip = True

# push it all to the screen
inky_display.show()


