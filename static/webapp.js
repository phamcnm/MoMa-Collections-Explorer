/*
 * webapp.js
 */

window.onload = initialize;

function initialize() {
    // search artworks
    var element = document.getElementById('search-artworks-button');
    if (element) {
        element.onclick = onSearchArtworksButton;
    }
    // clear artworks search
    var element = document.getElementById('clear-artworks-button');
    if (element) {
        element.onclick = onClearArtworksButton;
    }
    // open advanced search artworks options
    var element = document.getElementById('advanced-artworks-button');
    if (element) {
        element.onclick = openAdvancedOptionsArtworks;
    }
    // search artists
    var element = document.getElementById('search-artists-button');
    if (element) {
        element.onclick = onSearchArtistsButton;
    }
    // clear artists search
    var element = document.getElementById('clear-artists-button');
    if (element) {
        element.onclick = onClearArtistsButton;
    }
    // open advanced search artists options
    var element = document.getElementById('advanced-artists-button');
    if (element) {
        element.onclick = openAdvancedOptionsArtists;
    }
    // clear results
    var element = document.getElementById('clear-results-button');
    if (element) {
        element.onclick = onClearResultsButton;
    }

}

function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}

function openAdvancedOptionsArtworks() {
    if (document.getElementById('advanced-options-artworks').style.display === 'block') {
        document.getElementById('advanced-options-artworks').style.display = 'none'
        document.getElementById('advanced-artworks').innerText = "Open advanced options"
    } else {
        document.getElementById('advanced-options-artworks').style.display = 'block'
        document.getElementById('advanced-artworks').innerText = "Close advanced options"
    }
}

function openAdvancedOptionsArtists() {
    if (document.getElementById('advanced-options-artists').style.display === 'block') {
        document.getElementById('advanced-options-artists').style.display = 'none'
        document.getElementById('advanced-artists').innerText = "Open advanced options"
    } else {
        document.getElementById('advanced-options-artists').style.display = 'block'
        document.getElementById('advanced-artists').innerText = "Close advanced options"
    }
}

function onSearchArtworksButton() {

    // get the optional parameters
    var parameters = ""
    var artwork_title = document.getElementById('artwork-title')
    if (artwork_title) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "artwork_title=" + artwork_title.value;
    }
    var min_year = document.getElementById('artwork-minyear')
    if (min_year) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "min_year=" + min_year.value;
    }
    var max_year = document.getElementById('artist-maxyear')
    if (max_year) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "max_year=" + max_year.value;
    }
    var min_height = document.getElementById('minheight')
    if (min_height) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "min_height=" + min_height.value;
    }
    var max_height = document.getElementById('maxheight')
    if (max_height) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "max_height=" + max_height.value;
    }
    var min_width = document.getElementById('minwidth')
    if (min_width) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "min_width=" + min_width.value;
    }
    var max_width = document.getElementById('maxwidth')
    if (max_width) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "max_width=" + max_width.value;
    }
    var classification = document.getElementById('classification')
    if (classification) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "classification=" + classification.value;
    }
    var sort_by = document.getElementById('sort-artworks')
    if (sort_by) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "sort_by=" + sort_by.value;
    }
    var limit = document.getElementById('limit-artworks')
    if (limit) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "limit=" + limit.value;
    }
    if (parameters) {
        parameters = "?" + parameters;
    }

    var url = getAPIBaseURL() + "/artworks" + parameters;

    fetch(url, {method: 'get'})
    .then((response) => response.json())
    .then(function(artworks) {

        document.getElementById('num-results').innerHTML = artworks.length + " results returned:";


        // Print out the results
        var list_body = ''
        for (var k = 0; k < artworks.length; k++) {
            var artwork = artworks[k];
            list_body += '<li>' + artwork['artwork_title'] + " --- "
            if (document.getElementById('display-artist').checked) {
                list_body += artwork["artist_name"] + " "
            }
            if (document.getElementById('display-dimensions').checked) {
                list_body += "(" + artwork["width"] + "x" + artwork["height"] + ")"
            }
            if (document.getElementById('display-year-acquired').checked) {
                list_body += artwork["date_acquired"] + " "
            }
            if (document.getElementById('display-classification').checked) {
                list_body += artwork["classification"] + " "
            }
            list_body +=  '</li>\n';
        }
        if (list_body) {
            document.getElementById('clear-results-button').style.display = "block"
        }
        // Display it in the html
        var testListElement = document.getElementById('results');
        if (testListElement) {
            testListElement.innerHTML = list_body;
        }
    })
    .catch(function(error) {
        console.log(error);
    });
}

function onClearArtworksButton() {
    document.getElementById('artwork-title').value = ''
    document.getElementById('artwork-minyear').value = ''
    document.getElementById('artist-maxyear').value = ''
    document.getElementById('minheight').value = ''
    document.getElementById('maxheight').value = ''
    document.getElementById('minwidth').value = ''
    document.getElementById('maxwidth').value = ''
    document.getElementById('classification').value = ''
}

function onSearchArtistsButton() {

    // get the optional parameters
    var parameters = ""
    var artist_name = document.getElementById('artist-name')
    if (artist_name) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "artist_name=" + artist_name.value;
    }
    var artist_minyear = document.getElementById('artist-minyear')
    if (artist_minyear) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "artist_minyear=" + artist_minyear.value;
    }
    var artist_maxyear = document.getElementById('artist-maxyear')
    if (artist_maxyear) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "artist_maxyear=" + artist_maxyear.value;
    }
    var gender = document.getElementById('gender')
    if (gender) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "gender=" + gender.value;
    }
    var nationality = document.getElementById('nationality')
    if (nationality) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "nationality=" + nationality.value;
    }
    var sort_by = document.getElementById('sort-artists')
    if (sort_by) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "sort_by=" + sort_by.value;
    }
    var limit = document.getElementById('limit-artists')
    if (limit) {
        if (parameters) {
            parameters += "&"
        }
        parameters += "limit=" + limit.value;
    }
    if (parameters) {
        parameters = "?" + parameters;
    }

    var url = getAPIBaseURL() + "/artists" + parameters;

    fetch(url, {method: 'get'})
    .then((response) => response.json())
    .then(function(artists) {

        document.getElementById('num-results').innerHTML = artists.length + " results returned:";

        // Print out the results
        var list_body = '';
        for (var k = 0; k < artists.length; k++) {
            var artist = artists[k];
            list_body += '<li>' + artist['artist_name'] + " "
            if (document.getElementById('display-birth-year').checked) {
                list_body += artist['birth_year']
            }
            if (document.getElementById('display-birth-year').checked || document.getElementById('display-death-year').checked) {
                list_body += "-"
            }
            if (document.getElementById('display-death-year').checked) {
                list_body += artist['death_year']
            }
            if (document.getElementById('display-birth-year').checked || document.getElementById('display-death-year').checked) {
                list_body += " "
            }
            if (document.getElementById('display-gender').checked) {
                list_body += artist['gender'] + " "
            }
            if (document.getElementById('display-nationality').checked) {
                list_body += artist['nationality']
            }
            list_body += "</li>\n";
        }
        // Display it in the html
        if (list_body) {
            document.getElementById('clear-results-button').style.display = "block"
        }
        var testListElement = document.getElementById('results');
        if (testListElement) {
            testListElement.innerHTML = list_body;
        }
    })
    .catch(function(error) {
        console.log(error);
    });
}

function onClearArtistsButton() {
    document.getElementById('artist-name').value = ''
    document.getElementById('artist-minyear').value = ''
    document.getElementById('artist-maxyear').value = ''
    document.getElementById('gender').value = ''
    document.getElementById('nationality').value = ''
}

function onClearResultsButton() {
    document.getElementById('results').innerHTML = ''
    document.getElementById('num-results').innerHTML = ''
    document.getElementById('clear-results-button').style.display = "none"
}
