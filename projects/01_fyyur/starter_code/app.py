#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (
  Flask, 
  render_template, 
  request, Response, 
  flash, 
  redirect, 
  url_for, 
  jsonify, abort
  )
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
from flask_migrate import Migrate
# import datetime
from datetime import datetime
import ast
from sqlalchemy import and_, or_, not_
from models import db, Venue, Artist, Show 
import distutils
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)


# TODO: connect to a local postgresql database
# db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  recent_artists = Artist.query.order_by(Artist.id.desc()).limit(10).all()[::-1]
  recent_venues = Venue.query.order_by(Venue.id.desc()).limit(10).all()[::-1]
  # print(recent_venues)
  return render_template('pages/home.html', artists=recent_artists, venues=recent_venues)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []

  area = []
  venues = Venue.query.all()
  # print(venues[0].shows[0].start_time)

  places = Venue.query.distinct(Venue.city, Venue.state).all()

  for place in places:
      area.append({
          'city': place.city,
          'state': place.state,
          'venues': [{
              'id': venue.id,
              'name': venue.name,
          } for venue in venues if
              venue.city == place.city and venue.state == place.state]
      })

  return render_template('pages/venues.html', areas=area);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term')
  venues = Venue.query.filter(or_(Venue.name.ilike('%' + search_term + '%'), Venue.state.ilike('%' + search_term + '%'), Venue.city.ilike('%' + search_term + '%'))).all() # l
  # print(venues)

  data = []
  currentDate = datetime.now()  
  for venue in venues:
        num_upcoming_shows = []
        if len(venue.shows) > 0:
              num_upcoming_shows = [str(show.start_time) for show in venue.shows if currentDate < show.start_time]
        data.append({
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": len(num_upcoming_shows),
        })

  response={
    "count": len(venues),
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  past_shows = db.session.query(Artist, Show).join(Show).join(Venue).filter(
        Show.venue_id == venue_id,
        Show.artist_id == Artist.id,
        Show.start_time < datetime.now()
    ).all()

  upcoming_shows = db.session.query(Artist, Show).join(Show).join(Venue).filter(
        Show.venue_id == venue_id,
        Show.artist_id == Artist.id,
        Show.start_time > datetime.now()
    ).all()

  venue = Venue.query.get(venue_id)
  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": [{
            'artist_id': artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
        } for artist, show in past_shows],
    "upcoming_shows": [{
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        } for artist, show in upcoming_shows],
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  form = VenueForm(request.form, meta={'csrf': False})
  if form.validate():
        try:
          venue = Venue()
          form.populate_obj(venue)
          venue.seeking_talent = form.seeking_talent.data == 'True'

          db.session.add(venue)
          db.session.commit()
        # TODO: modify data to be the data object returned from db insertion
          flash('Venue ' + venue.name + ' was successfully listed!')
        except ValueError as e:
          print(e)
          db.session.rollback()
        finally:
          db.session.close()
  else:
        
        message = []
        for field, err in form.errors.items():
              message.append(field + ' ' + '|'.join(err))
        flash('Errors ' + str(message))
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.with_entities(Artist.id, Artist.name).order_by(db.asc(Artist.name)).all()

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search_term = request.form.get('search_term')
  artists = Artist.query.filter(or_(Artist.name.ilike('%' + search_term + '%'), Artist.city.ilike('%' + search_term + '%'), Artist.state.ilike('%' + search_term + '%'))).all()

  data = []
  currentDate = datetime.now()  
  for artist in artists:
        num_upcoming_shows = []
        if len(artist.shows) > 0:
              num_upcoming_shows = [str(show.start_time) for show in artist.shows if currentDate < show.start_time]
        data.append({
          "id": artist.id,
          "name": artist.name,
          "num_upcoming_shows": len(num_upcoming_shows),
        })

  response={
    "count": len(artists),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id

  past_shows = db.session.query(Artist, Show).join(Show).join(Venue).filter(
        Show.venue_id == Venue.id,
        Show.artist_id == artist_id,
        Show.start_time < datetime.now()
    ).all()

  upcoming_shows = db.session.query(Artist, Show).join(Show).join(Venue).filter(
        Show.venue_id == Venue.id,
        Show.artist_id == artist_id,
        Show.start_time > datetime.now()
    ).all()

  artist = Artist.query.get(artist_id)

  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": [{
            'venue_id': venue.id,
            'venue_name': venue.name,
            'venue_image_link': venue.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        } for venue, show in past_shows],
    "upcoming_shows": [{
            'venue_id': venue.id,
            'venue_name': venue.name,
            'venue_image_link': venue.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        } for venue, show in upcoming_shows],
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  artist.availability_start_time = datetime.now() if artist.availability_start_time is None else artist.availability_start_time
  artist.availability_end_time = datetime.now() if artist.availability_end_time is None else artist.availability_end_time
  form = ArtistForm(obj=artist)
  
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm(request.form, meta={'csrf': False})
  if form.validate():
        try:
          artist = Artist.query.get(artist_id)
          form.populate_obj(artist)
          artist.seeking_venue = form.seeking_venue.data == 'True'

          db.session.add(artist)
          db.session.commit()
        # TODO: modify data to be the data object returned from db insertion
          flash('Artist ' + artist.name + ' was successfully Edited!')
        except ValueError as e:
          print(e)
          db.session.rollback()
        finally:
          db.session.close()
  else:
        
        message = []
        for field, err in form.errors.items():
              message.append(field + ' ' + '|'.join(err))
        flash('Errors ' + str(message))
  return render_template('pages/home.html')

  

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)

  form = VenueForm(obj=venue)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
      
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm(request.form, meta={'csrf': False})
  if form.validate():
        try:
          venue = Venue.query.get(venue_id)
          form.populate_obj(venue)
          # print(type(form.seeking_talent.data == 'True'))
          venue.seeking_talent = form.seeking_talent.data == 'True'
          db.session.commit()
        # TODO: modify data to be the data object returned from db insertion
          flash('Venue ' + venue.name + ' was successfully Edited!')
        except ValueError as e:
          print(e)
          db.session.rollback()
        finally:
          db.session.close()
  else:
        
        message = []
        for field, err in form.errors.items():
              message.append(field + ' ' + '|'.join(err))
        flash('Errors ' + str(message))
  return render_template('pages/home.html')

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form, meta={'csrf': False})
  if form.validate():
        try:
          artist = Artist()
          form.populate_obj(artist)
          artist.seeking_venue = form.seeking_venue.data == 'True'

          db.session.add(artist)
          db.session.commit()
        # TODO: modify data to be the data object returned from db insertion
          flash('Artist ' + artist.name + ' was successfully listed!')
        except ValueError as e:
          print(e)
          db.session.rollback()
        finally:
          db.session.close()
  else:
        
        message = []
        for field, err in form.errors.items():
              message.append(field + ' ' + '|'.join(err))
        flash('Errors ' + str(message))
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows = Show.query.all()
  data = []
  for show in shows:
        data.append({
          "venue_id": show.shows_venue.id,
          "venue_name": show.shows_venue.name,
          "artist_id": show.shows_artist.id,
          "artist_name": show.shows_artist.name,
          "artist_image_link": show.shows_artist.image_link,
          "start_time": str(show.start_time)
        })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  msg = ''

  form = ShowForm(request.form, meta={'csrf': False})
  if form.validate():
        try:
          show = Show()
          form.populate_obj(show)
          
          event_time = show.start_time

          artist = Artist.query.get(show.artist_id)
          
          if artist.availability_start_time and artist.availability_end_time:
                if artist.availability_start_time <= event_time <= artist.availability_end_time:
                      db.session.add(show)
                      db.session.commit()
                else:
                      error = True
                      
                      msg = 'NOT CREATED. Artist not available at this time.'
          else:
                db.session.add(show)
                db.session.commit()
        except ValueError as e:
          print(e)
          error = True
          db.session.rollback()
        finally:
          db.session.close()
        if error:
              msg = msg if msg != '' else 'An error occurred. Show could not be listed.'
              flash(msg)
        else:
          flash('Show was successfully listed!')

        # on successful db insert, flash success
        # flash('Show was successfully listed!')
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
