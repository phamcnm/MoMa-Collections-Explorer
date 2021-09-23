/*
 * chart-from-api.js
 *
 * Uses the Chartist library: https://gionkunz.github.io/chartist-js/
 * Copyright © 2019 Gion Kunz
 * Free to use under either the WTFPL license or the MIT license.
 *
 */

window.onload = initialize;

function initialize() {
    // initializeNationalitySelector();
}

function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}

// function initializeNationalitySelector() {
//     var nationalitySelector = document.getElementById('visualize-nationalities-select');
//     nationalitySelector.onchange = onNationalitySelectorChanged;
//     // load 'american' by default
//     nationalitySelector.value = 4;
//     createGenderChart(4);
// }
//
// function onNationalitySelectorChanged() {
//     var nationalitySelector = document.getElementById('visualize-nationalities-select');
//     if (nationalitySelector) {
//         var nationality_id = nationalitySelector.value;
//         createGenderChart(nationality_id);
//     }
// }

var nationality_id = 4

function createGenderChart(nationality_id) {
    var url = getAPIBaseURL() + '/visualize/artist_gender/' + nationality_id;

    fetch(url, {method: 'get'})
    .then((response) => response.json())

    .then(function(visualize_artist_gender) {
        // for (var k = 0; k < visualize_artist_gender.length; k++) {
        //     var gender = genders[k];
        var female_artists = visualize_artist_gender[0];
        var male_artists = visualize_artist_gender[1];

        var data = {
            labels: ['1730', '1740', '1750', '1760', '1770', '1780', '1790', '1800', '1810', '1820', '1830', '1840', '1850', '1860', '1870', '1880', '1890', '1900', '1910', '1920', '1930', '1940', '1950', '1960', '1970', '1980', '1990', '2000', '2010', '2020'],

            series: [
                { data: female_artists }
                { data: male_artists }
                // { data: ['1730', '1740', '1750', '1760', '1770', '1780', '1790', '1800', '1810', '1820', '1830', '1840', '1850', '1860', '1870', '1880', '1890', '1900', '1910', '1920', '1930', '1940', '1950', '1960', '1970', '1980', '1990', '2000', '2010', '2020'] }
            ];
        }

        var options = { seriesBarDistance: 25,
                        axisX: { labelInterpolationFnc:
                        function(value, index) {
                                    return index % 5 === 0 ? value :
                                    null;
                                }
                            },
                        };

        var chart = new Chartist.Line('#visualize-gender-chart', data, options);

    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}
