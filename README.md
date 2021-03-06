*NIX command line and GUI tool for retrieving OMDb movie/TV information
============================================================

### Prerequisites:

You need to obtain your personal **API key** from the [OMDb API
website][omdbapi] in order to be able to use the tool. Once you have it, you
can either pass it via `--apikey` argument, or if you don't wish to pass it
every time, you can set it as an environment variable `OMDB_API_KEY`.

### Usage:

First set up an alias for the command:

    alias omdbtool="python /path/to/omdbtool.py"

Or for the gui:

    alias omdbtool="python /path/to/omdbtool-gui.py"

Note: in order to use the gui you will need to install [Gooey][gooey]

    pip install Gooey

### Some interesting usage examples:

Show all info about the movie 'Cars'

    omdbtool -t Cars

Show all info about the series 'Firefly'

    omdbtool -t firefly --type series

Show all info about season 1 episode 1 of 'Firefly'

    omdbtool -t firefly --season 1 --episode 1

Show all info about the series 'Firefly', in JSON format

    omdbtool -t firefly -r JSON

Show all info about latest 'True Grit' movie

    omdbtool -t "True Grit"

Show all info about 1969 version of 'True Grit'

    omdbtool -t "True Grit" -y 1969

Print movie's rating only

    omdbtool -t Cars | sed -n '/^imdbrating/{n;p;}'

Download movie's poster

    omdbtool -t Cars | wget `sed -n '/^poster/{n;p;}'`


### Additional useful features:

Include full plot summary (not available for some movies)

    omdbtool -t "True Grit" --plot full

Include additional data from Rotten Tomatoes

    omdbtool -t "True Grit" --tomatoes

Show info by IMDb id

    omdbtool -i tt0103064


### Example to get ratings for all movies in current directory

(it will use directory and file names as movie titles)

Save following code to file `get_ratings.sh` (make sure to update the path in line 3):

    ls -1 |
    while read title; do
      res=`python /path/to/omdbtool.py -t "$title"`
      rating=`echo "$res" | sed -n '/^imdbrating/{n;p;}'`
      restitle=`echo "$res" | sed -n '/^title/{n;p;}' | sed s/*//g`
      year=`echo "$res" | sed -n '/^year/{n;p;}'`
      echo "$title  *  $restitle  *  $year  *  $rating"
    done

then execute the saved command to fetch all the ratings: `./get_ratings.sh > ratings.txt`
(it'll take a while to retrieve all the data). Then you can open the
`ratings.txt` file to see the movie ratings, or you can sort the movies by
ratings to pick the best one to watch: `< ratings.txt sort -t* -k4 -r`.

_(This used to be more useful when the API worked with inexact movie titles)_


## Notes ##

 - works with Python 3 and Python 2.7 or earlier with argparse package installed
 - **thanks to the creator of this [great site called OMDBAPI][omdbapi]**


## License ##

This tool is licensed under [GNU Lesser GPL][lgpl] license.


[omdbapi]: http://www.omdbapi.com
[lgpl]: http://www.gnu.org/licenses/lgpl.html
[gooey]: https://github.com/chriskiehl/Gooey
