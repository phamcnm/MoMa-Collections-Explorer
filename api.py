'''
	webapp.py
	api design link: https://docs.google.com/document/d/1C5ehLX8iEC4V5L81kdd9yBH9Xf6DoRMkKh0SB84Zd3s/edit?usp=sharing
'''
import sys
import flask
import json
import config
import psycopg2
api = flask.Blueprint('api', __name__)

def get_connection():
	'''
	Returns a connection to the database described in the
	config module. May raise an exception as described in the
	documentation for psycopg2.connect.
	'''
	return psycopg2.connect(database=config.database,
							user=config.user,
							password=config.password)

def send_query(query):
	try:
		connection = get_connection()
		cursor = connection.cursor()
		cursor.execute(query)
	except Exception as e:
		print(e, file=sys.stderr)
		exit()
	return cursor

def get_wildcard(string):
	string = "%" + string + "%"
	return string

def create_end_of_search_query(query, conditions):
	if len(conditions) > 0:
		query += " WHERE "
		for i in range(len(conditions)):
			query += conditions[i]
			if i < len(conditions)-1:
				query += " AND "
	return query

def get_string_by_id(field, value):
	if value == None:
		return None
	if field[-1] == "y":
		table = field[:-1] + "ies"
	else:
		table = field + "s"
	id_field = field + "_id"
	query = f"SELECT {field} FROM {table} WHERE {id_field} = {value}"
	cursor = send_query(query).fetchone()[0]
	return cursor

def get_id_by_string(field, value, full_match=True):
	if full_match:
		query = "SELECT %s FROM %s WHERE %s = %s"
	else:
		query = "SELECT %s FROM %s WHERE %s LIKE %s"
	if field[-1] == "y":
		table = field[:-1] + "ies"
	else:
		table = field + "s"
	id_field = field + "_id"
	cursor = send_query(query).fetchone()[0]
	return cursor

def get_artist_id_from_artwork_id(artwork_id):
	query = f"SELECT artists.artist_id FROM artists, artworks, artworks_artists WHERE artworks.artwork_id = artworks_artists.artwork_id AND artists.artist_id = artworks_artists.artist_id AND artworks.artwork_id = {artwork_id}"
	try:
		cursor = send_query(query).fetchone()[0]
	except: # artwork has no recorded artist
		return None
	return cursor

def get_artist_name_from_artwork_id(artwork_id):
	query = f"SELECT artists.artist_name FROM artists, artworks, artworks_artists WHERE artworks.artwork_id = artworks_artists.artwork_id AND artists.artist_id = artworks_artists.artist_id AND artworks.artwork_id = {artwork_id}"
	try:
		cursor = send_query(query).fetchone()[0]
	except: # artwork has no recorded artist
		return None
	return cursor

def get_sort_artists(sort_id):
	sort_by = ["artist_name", "birth_year", "death_year", "nationality"]
	return sort_by[sort_id]

def get_sort_artworks(sort_id):
	sort_by = ["artwork_title", "artwork_year"]
	return sort_by[sort_id]

@api.route('/test/')
def get_testlist():
	query = '''SELECT * FROM artworks LIMIT 10'''
	cursor = send_query(query)
	artworks_testlist = []
	for row in cursor:
		artwork = {'artwork_title':row[1], 'year_created':row[2], 'height':row[4], 'width':row[5]}
		artworks_testlist.append(artwork)
	return json.dumps(artworks_testlist)


@api.route('/artists')
# ?artist_name={name}&min_year={min_year}&max_year={max_year}&gender={gender}&nationality={nationality}
# sort={artist_name|birth_year|death_year|gender|nationality}&display[]=[true|false]
def get_artists_list():
	'''
	Parameters:
		artist_name={name} (optional, default none): (text) search string for the artist's full name
		min_year={year} (optional, default none): (integer) lower boundary for artist's birth year
		max_year={year} (optional, default none): (integer) upper boundary for artist's death year
		gender={gender} (optional, default none): (text) the artist's gender
		nationality={nationality} (optional, default none): (text) the artist's nationality
	RESPONSE: A JSON list of dictionaries, each of which represents an artist, filtered by several parameters. Each dictionary has the following fields:
		artist_id -- (integer) unique identifier for artist
		artist_name -- (text) the artist’s full name
		birth_year -- (integer) the year the artist was born
		death_year -- (integer) the year the artist was gone
		gender -- (text) the artist’s gender
		nationality -- (text) the artist’s nationality
	'''
	artist_name = flask.request.args.get('artist_name', default='',type=str)
	min_year = flask.request.args.get('min_year', default='', type=int)
	max_year = flask.request.args.get('max_year', default='', type=int)
	gender = flask.request.args.get('gender', default='', type=int)
	nationality = flask.request.args.get('nationality', default='', type=int)
	sort_id = flask.request.args.get('sort_by', default=0, type=int)
	limit = flask.request.args.get('limit', default=10, type=int)

	query = "SELECT * FROM artists"

	artist_name_wildcarded = get_wildcard(artist_name)

	conditions = []
	if (artist_name):
		conditions.append(f"artist_name LIKE '{artist_name_wildcarded}'")
	if (min_year):
		conditions.append(f"death_year > {min_year}")
	if (max_year):
		conditions.append(f"birth_year < {max_year}")
	if (gender):
		conditions.append(f"gender = {gender}")
	if (nationality):
		conditions.append(f"nationality = {nationality}")

	if len(conditions) > 0:
		query = create_end_of_search_query(query, conditions)

	sort_by = get_sort_artists(sort_id)
	query += f" ORDER BY {sort_by} LIMIT {limit}"

	cursor = send_query(query)

	artists_list = []
	for row in cursor:
		artist_dict = {}
		artist_dict['artist_id'] = row[0]
		artist_dict['artist_name'] = row[1]
		artist_dict['nationality'] = get_string_by_id("nationality", row[2])
		artist_dict['gender'] = get_string_by_id("gender", row[3])
		artist_dict['birth_year'] = row[4]
		artist_dict['death_year'] = row[5]
		artists_list.append(artist_dict)

	return json.dumps(artists_list)

@api.route('/artworks')
# ?sort={artwork_name|artist_name|year_created|artist_birth|artist_death|classification|department|year_acquired}&display[]=[true|false]
def get_artworks_list():
	'''
	Parameters:
		artwork_title={title} (optional, default none): (text) search string for the artwork title
		min_year={year} (optional, default none): (integer) lower boundary for year created
		max_year={year} (optional, default none): (integer) upper boundary for year created
		medium={medium} (optional, default none): (text) search string for the artwork medium
		min_height={height} (optional, default none): (integer) lower boundary for artwork height
		max_height={height} (optional, default none): (integer) upper boundary for artwork height
		min_width={height} (optional, default none): (integer) lower boundary for artwork width
		max_width={height} (optional, default none): (integer) upper boundary for artwork width
		min_year_acquired={year} (optional, default none): (integer) lower boundary for the year acquired
		max_year_acquired={year} (optional, default none): (integer) upper boundary for the year acquired
		classification={classification} (optional, default none): (integer) the classification of the artworks
		department={department} (optional, default none): (integer) the department of the artworks
		sort_id={id} (default 0): (integer) the id of sorting by artwork_name
		limit={limit} (default 10): (integer) how many rows to show
	RESPONSE: A JSON list of dictionaries, each of which represents an artwork. This list only contains artworks that are filtered by specified parameters from above. Each dictionary has the following fields, which are the fields that will be displayed by default:
		artwork_title -- (text) the artwork’s title
		artist_name -- (text) the artist’s full name
		year_created -- (integer) the year the artwork was created

	'''
	artwork_title = flask.request.args.get('artwork_title', default='',type=str)
	min_year = flask.request.args.get('min_year', default='', type=int)
	max_year = flask.request.args.get('max_year', default='', type=int)
	medium = flask.request.args.get('medium', default='', type=str)
	min_height = flask.request.args.get('min_height', default='', type=float)
	max_height = flask.request.args.get('max_height', default='', type=float)
	min_width = flask.request.args.get('min_width', default='', type=float)
	max_width = flask.request.args.get('max_width', default='', type=float)
	min_year_acquired = flask.request.args.get('min_year_acquired', default='', type=int)
	max_year_acquired = flask.request.args.get('max_year_acquired', default='', type=int)
	classification = flask.request.args.get('classification', default='', type=int)
	department = flask.request.args.get('department', default='', type=int)
	sort_id = flask.request.args.get('sort_by', default=0, type=int)
	limit = flask.request.args.get('limit', default=10, type=int)

	artwork_title_wildcarded = get_wildcard(artwork_title)
	medium_wildcarded = get_wildcard(medium)

	query = "SELECT artwork_id, artwork_title, height, width, classification, department, date_acquired FROM artworks"

	conditions = []
	if (artwork_title):
		conditions.append(f"artwork_title LIKE '{artwork_title_wildcarded}'")
	if (min_year):
		conditions.append(f"artwork_year > {min_year}")
	if (max_year):
		conditions.append(f"artwork_year < {max_year}")
	if (medium):
		conditions.append(f"medium LIKE {medium_wildcarded}")
	if (min_height):
		conditions.append(f"height > {min_height}")
	if (max_height):
		conditions.append(f"height < {max_height}")
	if (min_width):
		conditions.append(f"width > {min_width}")
	if (max_width):
		conditions.append(f"width < {max_width}")
	if (min_year_acquired):
		conditions.append(f"year_acquired > {min_year_acquired}")
	if (max_year_acquired):
		conditions.append(f"year_acquired < {max_year_acquired}")
	if (classification):
		conditions.append(f"classification = {classification}")
	if (department):
		conditions.append(f"department = {department}")

	if len(conditions) > 0:
		query = create_end_of_search_query(query, conditions)

	sort_by = get_sort_artworks(sort_id)
	query += f" ORDER BY {sort_by} LIMIT {limit}"

	cursor = send_query(query)

	artworks_list = []
	for row in cursor:
		artwork_dict = {}
		artwork_dict['artwork_id'] = row[0]
		artwork_dict['artwork_title'] = row[1]
		artwork_dict['artist_name'] = get_artist_name_from_artwork_id(row[0])
		artwork_dict['height'] = row[2]
		artwork_dict['width'] = row[3]
		artwork_dict['classification'] = get_string_by_id("classification", row[4])
		artwork_dict['classification'] = get_string_by_id("department", row[5])
		artwork_dict['date_acquired'] = str(row[6])
		artworks_list.append(artwork_dict)

	return json.dumps(artworks_list)


@api.route('/artists/<artist_id>')
def get_artist(artist_id):

    '''
    RESPONSE: a JSON dictionary representing a single artist, with the following fields:
        artist_name -- (text) the artist’s full name
        birth_year -- (integer) the year the artist was born
        death_year -- (integer) the year the artist was gone
        gender -- (text) the artist's gender
        nationality -- (text) the artist’s nationality
        artworks -- (dictionaries) the list of all the artworks created by this artist. Each of these nested dictionaries will contain the following fields:
        artwork_id -- (integer) unique identifier for the artwork
        artwork_title -- (text) the artwork’s title
        year -- (integer) the year the artwork was created
    '''

    "SELECT artworks.artwork_id, artworks.artwork_title, artists.artist_name, artworks.artwork_year FROM artworks, artists, artworks_artists WHERE artworks.artwork_id = artworks_artists.artwork_id AND artists.artist_id = artworks_artists.artist_id"

    query = f"SELECT * FROM artists WHERE artist_id = {artist_id}"
    cursor = send_query(query).fetchone()
    artist_dict = {}
    artist_dict['artist_name'] = cursor[1]
    artist_dict['nationality'] = get_string_by_id("nationality", cursor[2])
    artist_dict['gender'] = get_string_by_id("gender", cursor[3])
    artist_dict['birth_year'] = cursor[4]
    artist_dict['death_year'] = cursor[5]

    return json.dumps(artist_dict)

@api.route('/artists/artworksby/<artist_id>')
def get_artworks_by_artist(artist_id):

    query = f"SELECT artworks.artwork_id, artworks.artwork_title, artworks.artwork_year FROM artworks, artists, artworks_artists WHERE artists.artist_id = {artist_id}"
    cursor = send_query(query)

    artworks_list = []
    for row in cursor:
        artwork_dict = {}
        artwork_dict['artwork_id'] = row[0]
        artwork_dict['artwork_title'] = row[1]
        artwork_dict['artist_name'] = get_artist_name_from_artwork_id(row[0])
        artwork_dict['year_created'] = row[2]
        artworks_list.append(artwork_dict)

    return json.dumps(artworks_list)



@api.route('/artworks/<artwork_id>')
def get_artwork(artwork_id):
    '''
    RESPONSE: A JSON dictionary representing a single artwork, with the following fields:
        artwork_title -- (text) the artwork’s title
        artist_id -- (integer) unique identifier for the artist
        artist_name -- (text) the artist’s full name
        year_created -- (integer) the year the artwork was created
        medium -- (text) the medium(s) of the artwork
        dimensions -- (text) the dimensions of the artwork, for displaying
        height -- (float) the height of the artwork in cm
        width -- (float) the width of the artwork in cm
        credit_line -- (text) crediting who gave the artwork to the MoMA
        classification -- (text) the artwork’s classification
        department -- (text) the artwork’s department
        year_acquired -- (integer) the year, or the estimated year range the artwork was acquired
        lookup_id -- (int) ID of the artwork, to link to its entry in MoMA’s website (add to end of URL)
    '''

    query = f"SELECT * FROM artworks WHERE artwork_id = {artwork_id}"
    cursor = send_query(query).fetchone()

    artwork_dict = {}
    artwork_dict['artwork_id'] = cursor[0]
    artwork_dict['artwork_title'] = cursor[1]
    artwork_dict['artist_id'] = get_artist_id_from_artwork_id(cursor[0])
    artwork_dict['artist_name'] = get_artist_name_from_artwork_id(cursor[0])
    artwork_dict['artwork_year'] = cursor[2]
    artwork_dict['medium'] = cursor[3]
    artwork_dict['height'] = cursor[4]
    artwork_dict['width'] = cursor[5]
    artwork_dict['dimensions'] = cursor[6]
    artwork_dict['classification'] = cursor[7]
    artwork_dict['department'] = cursor[8]
    artwork_dict['date_acquired'] = str(cursor[9])
    artwork_dict['credit_line'] = cursor[10]
    artwork_dict['area'] = float(artwork_dict['height']) * float(artwork_dict['width'])

    return json.dumps(artwork_dict)



@api.route('/visualize/artist_gender/<nationality_id>')
def visualize_artist_gender(nationality_id):
    '''
    Returns a list containing two lists:
        male_artists: the number of male artists born in each 10 years
        female_artists: the number of female artists born in each 10 years
    '''

    years = [1730, 1740, 1750, 1760, 1770, 1780, 1790, 1800, 1810, 1820, 1830, 1840, 1850, 1860, 1870, 1880, 1890, 1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]

    female_artists = []
    male_artists = []
    for year in years:
        female_artists.append(0)
        male_artists.append(0)

    prev_year = 1720
    for cur_year in years:
        query = f"SELECT gender FROM artists WHERE nationality = {nationality_id} AND birth_year < {cur_year} and birth_year > {prev_year}"
        cursor = send_query(query)

        for row in cursor:
            if row[0] == 1: #female
                female_artists[years.index(cur_year)] += 1
            if row[0] == 2: #male
                male_artists[years.index(cur_year)] += 1
            prev_year = cur_year

    visualize_data = []
    visualize_data.append(female_artists)
    visualize_data.append(male_artists)

    return json.dumps(visualize_data)