# -*- coding: utf-8 -*-

"""
Description du pogramme: à faire.
"""

import os

from flask import Blueprint
from flask import current_app as app
from flask import request, render_template

from .utils import *
from .auth  import auth

root_path = os.path.dirname(os.path.abspath(__file__))
kerguelen = Blueprint('kerguelen', __name__, url_prefix='/kerguelen')

@kerguelen.route('/', methods = ['GET'])
@auth.login_required
def home():

    # calcul du remplissage de la carte SD
    sd_percent = os.statvfs(os.path.dirname(os.path.abspath(__file__)))
    sd_percent = int(100-float(sd_percent.f_bavail)/float(sd_percent.f_blocks)*100)
    if ( sd_percent < 80 ):
        sd_color = "green"
    else:
        sd_color = "deep-orange"

    return render_template(
        "home.html",
        home_menu  = True,
        sd_percent = sd_percent,
        sd_color   = sd_color,
        version    = app.config['VERSION']
    )

@kerguelen.route('/camera', methods = ['GET'])
@auth.login_required
def camera():
    messages = list()

    photo_param = request.args.get('photo')
    if photo_param == 'new':
      if not take_a_picture(app.config):
        messages.append('Impossible de prendre la photo, problème avec la caméra.')

    purge_param = request.args.get('purge')
    images = get_images(os.path.join(root_path, 'static'))
    if purge_param == 'all':
      purge(list(images.values()))
      images = get_images(os.path.join(root_path, 'static'))
    elif purge_param == 'old':
      purge(list(images.values())[10:])
      images = get_images(os.path.join(root_path, 'static'))
    else:
      pass

    # get the last picture:
    if ( len(images) > 0 ):
      for image in images.values():
        last_image = image
        break
    else:
      last_image = None

    # affichage de la page sur la base du modele
    return render_template(
        'camera.html',
        camera_menu = True,
        image = last_image,
        num_images = len(images),
        version    = app.config['VERSION'],
        messages = messages
    )

@kerguelen.route('/historique', methods = ['GET'])
@auth.login_required
def historique():
  images = get_images(os.path.join(root_path, 'static'))
  for image in images.values():
    current_image=image
    break

  action = request.args.get('action')
  if ( action == 'view' ):
    current_image = request.args.get('image')
  elif ( action == 'del' ):
    current_image = request.args.get('image')
    purge(list([current_image]))
    images = get_images(os.path.join(root_path, 'static'))
    for image in images.values():
      current_image=image
      break
  else:
    pass

  return render_template(
    'historique.html',
    historique_menu = True,
    images = images,
    current_image = current_image,
    version    = app.config['VERSION']
  )

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
#   END OF FILE
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -