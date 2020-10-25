# -*- coding: utf-8 -*-

import os
import requests
import json

from datetime import datetime
from time import sleep
from base64 import b64decode
try:
    from picamera import PiCamera, Color
except:
    pass

root_path = os.path.dirname(os.path.abspath(__file__))

def get_weather(config):
  api_key     = config['WEATHER_API_KEY']
  latitude    = config['WEATHER_LATITUDE']
  longitude   = config['WEATHER_LONGITUDE']
  weather_url = config['WEATHER_URL']

  url = weather_url+"?lat="+latitude+"&lon="+longitude+"&appid="+api_key+"&lang=fr&units=metric&mode=json"

  r = requests.get(url)
  data = json.loads(r.text)

  weather_str = "{} (nuage: {}%) - Temp: {} - Vent: {} km/h ({}) - {} bars".format(
    data['weather'][0]['description'],
    data['clouds']['all'],
    data["main"]["temp"],
    float(data['wind']['speed'])*3600/1000,
    data['wind']['deg'],
    data["main"]["pressure"]
  )
  return weather_str


def now():
    d0 = datetime.now()
    d1 = d0.strftime("%Y%m%d-%H%M%S")
    d2 = d0.strftime("Le %d/%m/%Y %H:%M:%S")

    return d1, d2

def get_images(root):
  images = dict()
  for r, d, f in os.walk(root):
      for image in f:
          if image.endswith('.jpg'):
              images[os.path.basename(image)] = os.path.join('/static', image)
  sorted_images = { key: val for key, val  in sorted(images.items(), key=lambda elem: elem[0], reverse = True) }
  return sorted_images

def purge(images):
  for image in images:
    os.remove(os.path.join(root_path, image[1:]))

def take_a_picture(app):
  mode       = app.config['PHOTO_MODE']
  delay      = app.config['PHOTO_DELAY']
  width      = app.config['PHOTO_WIDTH']
  height     = app.config['PHOTO_HEIGHT']
  text_size  = app.config['PHOTO_TEXT_SIZE']
  background = app.config['PHOTO_BACKGROUND']
  quality    = app.config['PHOTO_QUALITY']

  instant, label = now()
  filename = os.path.join(os.path.dirname(__file__), 'static/'+instant+'.jpg')

  try:
      camera = PiCamera()
      camera.resolution = (width, height)
      camera.awb_mode = mode
      camera.start_preview()
      sleep(float(delay))
      weather = get_weather(app.config)
      camera.annotate_text = label + "\n" + weather
      camera.annotate_text_size = text_size
      camera.annotate_background = Color(background)
      camera.capture(filename, format = 'jpeg', quality = quality)

  except Exception as e:
      app.logger.error(e)
      return False

  finally:
      if 'camera' in locals():
        camera.close()
        return True
      else:
        return False