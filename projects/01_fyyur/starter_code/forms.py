from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, RadioField
from wtforms.validators import DataRequired, AnyOf, URL


state_choices = [
    ('AL', 'AL'),
    ('AK', 'AK'),
    ('AZ', 'AZ'),
    ('AR', 'AR'),
    ('CA', 'CA'),
    ('CO', 'CO'),
    ('CT', 'CT'),
    ('DE', 'DE'),
    ('DC', 'DC'),
    ('FL', 'FL'),
    ('GA', 'GA'),
    ('HI', 'HI'),
    ('ID', 'ID'),
    ('IL', 'IL'),
    ('IN', 'IN'),
    ('IA', 'IA'),
    ('KS', 'KS'),
    ('KY', 'KY'),
    ('LA', 'LA'),
    ('ME', 'ME'),
    ('MT', 'MT'),
    ('NE', 'NE'),
    ('NV', 'NV'),
    ('NH', 'NH'),
    ('NJ', 'NJ'),
    ('NM', 'NM'),
    ('NY', 'NY'),
    ('NC', 'NC'),
    ('ND', 'ND'),
    ('OH', 'OH'),
    ('OK', 'OK'),
    ('OR', 'OR'),
    ('MD', 'MD'),
    ('MA', 'MA'),
    ('MI', 'MI'),
    ('MN', 'MN'),
    ('MS', 'MS'),
    ('MO', 'MO'),
    ('PA', 'PA'),
    ('RI', 'RI'),
    ('SC', 'SC'),
    ('SD', 'SD'),
    ('TN', 'TN'),
    ('TX', 'TX'),
    ('UT', 'UT'),
    ('VT', 'VT'),
    ('VA', 'VA'),
    ('WA', 'WA'),
    ('WV', 'WV'),
    ('WI', 'WI'),
    ('WY', 'WY'),
]

genres_choices = [
    ('Alternative', 'Alternative'),
    ('Blues', 'Blues'),
    ('Classical', 'Classical'),
    ('Country', 'Country'),
    ('Electronic', 'Electronic'),
    ('Folk', 'Folk'),
    ('Funk', 'Funk'),
    ('Hip-Hop', 'Hip-Hop'),
    ('Heavy Metal', 'Heavy Metal'),
    ('Instrumental', 'Instrumental'),
    ('Jazz', 'Jazz'),
    ('Musical Theatre', 'Musical Theatre'),
    ('Pop', 'Pop'),
    ('Punk', 'Punk'),
    ('R&B', 'R&B'),
    ('Reggae', 'Reggae'),
    ('Rock n Roll', 'Rock n Roll'),
    ('Soul', 'Soul'),
    ('Other', 'Other'),
]

class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=state_choices
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=genres_choices
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    #Added
    image_link = StringField(
        'image_link'
    )
    seeking_talent = RadioField(
        'Radio',
        # [validators.Required()],
        validators=[DataRequired()],
        choices=[(True, 'True'), (False, 'False')], default=False
    ) 
    seeking_description = StringField(
        'seeking_description'
    )
    website = StringField(
        'website'
    )

    # Enum restriction
    def validate(self):
        """Define a custom validate method in Form:"""
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        if not set(self.genres.data).issubset(dict(genres_choices).keys()):
            self.genres.errors.append('Invalid genre.')
            return False
        if self.state.data not in dict(state_choices).keys():
            self.state.errors.append('Invalid state.')
            return False
        # if pass validation
        return True

class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=state_choices
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone', validators=[DataRequired()]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=genres_choices
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
    )


    #Added
    image_link = StringField(
        'image_link'
    )
    seeking_venue = RadioField(
        'Radio',
        validators=[DataRequired()],
        choices=[(True, 'True'), (False, 'False')], default=False
    ) 
    seeking_description = StringField(
        'seeking_description'
    )
    website = StringField(
        # TODO implement enum restriction
        'website'
    )
    availability_start_time = DateTimeField(
        'availability_start_time',
        default= datetime.today()
    )
    availability_end_time = DateTimeField(
        'availability_end_time',
        default= datetime.today()
    )

    # Enum restriction
    def validate(self):
        """Define a custom validate method in your Form:"""
        rv = FlaskForm.validate(self)
        if not rv:
            return False
        if not set(self.genres.data).issubset(dict(genres_choices).keys()):
            self.genres.errors.append('Invalid genre.')
            return False
        if self.state.data not in dict(state_choices).keys():
            self.state.errors.append('Invalid state.')
            return False
        # if pass validation
        return True

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
