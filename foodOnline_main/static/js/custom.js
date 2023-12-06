// let autocomplete;

// function initAutoComplete(){
// autocomplete = new google.maps.places.Autocomplete(
//     document.getElementById('id_address'), 
//     {
//     types: ['geocode', 'establishment'],
//         //default in this app is "IN" - add your country code
//     componentRestrictions:{'country':['in']},
//     })
// // function to specify what should happen when the prediction
// autocomplete.addListener('place_changed', onPlaceChanged);
// }

// function onPlaceChanged() {
//     var place = autocomplete.getPlace();
//     // user did not select the prediction. Reset the input field or alert()
//     if (!place.geometry) {
//         document.getElementById('id_address').placeholder = "Start typing...";
//     }
//     else{
//         // console.log('place name=>', place.name)
//     }
//     // get the address components and assign them to the fields 
//     //console.log(place)

//     var geocoder = new google.maps.Geocoder()
//     var address = document.getElementById('id_address').value 

//     geocoder.geocode({'address': address}, function(results, status){

//         if(status == google.maps.GeocoderStatus.OK){
//             var latitude = results[0].geometry.location.lat();
//             var longitude = results[0].geometry.location.lng();

//             //console.log('lat=>', latitude);
//             //console.log('lng=>', longitude);

//             $('#id_latitude').val(latitude);
//             $('#id_longitude').val(longitude);

//             $('#id_address').val(address);

//         }
//     });
// }
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// let autocomplete;

// function initAutoComplete() {
//     autocomplete = new MapQuest.autoComplete();
    
//     autocomplete.bindTo('id_address');

//     autocomplete.on('done', function(data) {
//         // Handle autocomplete results here if needed
//     });

//     // function to specify what should happen when the prediction is selected
//     autocomplete.on('select', function(data) {
//         onPlaceChanged(data.result);
//     });
// }

// function onPlaceChanged(place) {
//     // get the address components and assign them to the fields
//     var geocoder = new MapQuest.geocoding();
//     var address = place.displayString;

//     geocoder.geocode({
//         location: {
//             street: address
//         }
//     }, function(response) {
//         if (response.info.statuscode === 0) {
//             var location = response.results[0].locations[0].latLng;

//             // Update latitude and longitude fields
//             $('#id_latitude').val(location.lat);
//             $('#id_longitude').val(location.lng);

//             // Update address field
//             $('#id_address').val(address);
//         }
//     });
// }

// // Initialize the MapQuest Autocomplete
// window.onload = function () {
//     L.mapquest.key = 'ZF9FL4wX94kRuMo0xGMilQYlmjdMDGR9';
//     initAutoComplete();
// };
////////////////////////////////////////////////////////////////////////////////////////////////



// window.onload = function() {
//     placeSearch({
//       container: document.querySelector('#id_address'),
//       useDeviceLocation: true,
//       collection: [
//         'poi',
//         'airport',
//         'address',
//         'adminArea',
//       ]
//     })}

// ....................................................
// // Replace 'YOUR_API_KEY' with your actual MapQuest API key
// const apiKey = '{{MAPQUEST_API_KEY}}';

// // Function to get the latitude and longitude of a location using the MapQuest Geocoding API
// function getCoordinates(location) {
// const url = `https://www.mapquestapi.com/geocoding/v1/address?key=${apiKey}&location=${encodeURIComponent(location)}`;

// // Make a GET request to the MapQuest API
// fetch(url)
//     .then(response => response.json())
//     .then(data => {
//     // Extract latitude and longitude from the response
//     const firstResult = data.results[0].locations[0];
//     const latLng = {
//         lat: firstResult.latLng.lat,
//         lng: firstResult.latLng.lng
//     };

//     // Log the coordinates to the console
//     console.log('Coordinates:', latLng);
//     })
//     .catch(error => {
//     console.error('Error:', error);
//     });
// }

// // Example: Get coordinates for a location (replace with your desired location)
// const locationToGeocode = 'New York, NY';
// getCoordinates(locationToGeocode);

// ...................................................
// static/geocode.js
// $(document).ready(function () {
//     $('#geocodeForm').submit(function (e) {
//         e.preventDefault();

//         const location = $('#locationInput').val();
//         geocode(location);
//     });

//     function geocode(location) {
//         $.ajax({
//             url: '/geocode/',  // Django URL for handling the geocoding request
//             method: 'POST',
//             data: { location: location },
//             success: function (data) {
//                 $('#result').html(`Latitude: ${data.latitude}, Longitude: ${data.longitude}`);
//             },
//             error: function () {
//                 $('#result').html('Error geocoding the location.');
//             }
//         });
//     }
// });
// ....................................................
// var map = L.map('map').setView([29.843771, 31.119118], 13);

// var tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
//     maxZoom: 19,
//     attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
// }).addTo(map);

// const marker = L.marker([29.843771, 31.119118]).addTo(map)
//     .bindPopup('<b>Hello world!</b><br />I am a popup.').openPopup();

// const polygon = L.polygon([
//     [51.509, -0.08],
//     [51.503, -0.06],
//     [51.51, -0.047]
// ]).addTo(map).bindPopup('I am a polygon.');


// const popup = L.popup()
//     .setLatLng([51.513, -0.09])
//     .setContent('I am a standalone popup.')
//     .openOn(map);

// function onMapClick(e) {
//     popup
//         .setLatLng(e.latlng)
//         .setContent(`You clicked the map at ${e.latlng.toString()}`)
//         .openOn(map);
// }

// map.on('click', onMapClick);

//-------------------------------------------------------------------------------------------------------------

$(document).ready(function(){
    // Add to cart
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();
        
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        
        $.ajax({
            type: 'GET',
            url: url,
            
            success: function(response){
                console.log(response)
                if(response.status == 'login_required'){
                    // console.log('raise the error message')
                    swal(response.message, "", "info").then(function(){
                        window.location = "/accounts/login";
                    })
                }else if(response.status == 'Failed'){
                    swal(response.message,"", "error");
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);
                
                    // subtotal , tax and grand total
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total'],
                    )
                    
                }
            }
        })
    })

    // place the cart item quantity on load
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#'+the_id).html(qty)

    })

    // decrease cart
    $('.decrease_cart').on('click', function(e){
        e.preventDefault();
        
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');
        
        $.ajax({
            type: 'GET',
            url: url,
            
            success: function(response){
                console.log(response)
                if(response.status == 'login_required'){
                    swal(response.message, "", "info").then(function(){
                        window.location = "/accounts/login";
                    })
                }else if(response.status == 'Failed'){
                    swal(response.message,"", "error");
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);

                    // subtotal , tax and grand total
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total'],
                    );

                    if(window.location.pathname == '/cart/'){
                        removeCartItem(response.qty, cart_id);
                        checkEmptyCart();
                    }
                }

                
            }
        })
    })

    // Delete Item from cart
    $('.delete_from_cart').on('click', function(e){
        e.preventDefault();
        
        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        
        $.ajax({
            type: 'GET',
            url: url,
            
            success: function(response){
                console.log(response)
                if(response.status == 'Failed'){
                    swal(response.message,"", "error");
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    swal(response.status, response.message, 'success')

                    // subtotal , tax and grand total
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total'],
                    )

                    removeCartItem(0, cart_id);
                    checkEmptyCart();
                }

            }
        })
    })

    // delete the cart elmement if the qty is 0 --refresh auto
    function removeCartItem(cartItemQty, cart_id){
        
           if(cartItemQty <= 0){
            // remove the cart item element
            document.getElementById("cart-item-"+cart_id).remove()
            } 
        
        
    }

    function checkEmptyCart(){
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if(cart_counter == 0){
            document.getElementById("empty-cart").style.display = "block";
        }
    }

    // apply cart amounts
    function applyCartAmounts(subtotal, tax, grand_total){
        if(window.location.pathname == '/cart/'){
        $("#subtotal").html(subtotal);
        $("#tax").html(tax);
        $("#total").html(grand_total);
        }
    }

    //Add Opening Hour
    $('.add_hour').on('click', function(e){
        e.preventDefault();
        var day = document.getElementById('id_day').value
        var from_hour = document.getElementById('id_from_hour').value
        var to_hour = document.getElementById('id_to_hour').value
        var is_closed = document.getElementById('id_is_closed').checked
        var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
        var url = document.getElementById('add_hour_url').value
        
        console.log(day, from_hour, to_hour, is_closed, csrf_token)

        if(is_closed){
            is_closed = 'True'
            condition = "day != ''"
        }else{
            is_closed = 'False'
            condition = "day != '' && from_hour != '' && to_hour != ''"
        }
        if(eval(condition)){
            $.ajax({
                type:'POST',
                url: url,
                data:{
                    'day': day,
                    'from_hour': from_hour,
                    'to_hour': to_hour,
                    'is_closed': is_closed,
                    'csrfmiddlewaretoken': csrf_token
                },
                success: function(response){
                    if(response.status == 'success'){
                        if(response.is_closed == 'Closed'){
                            html = '<tr id="hour-'+response.id+'"><td><b>'+response.day+'</b></td><td>Closed</td><td><a href="#" class="remove_hour" data-url="/accounts/vendor/opening-hours/remove/'+response.id+'/">Remove</a></td></tr>';
                        }else{
                            html = '<tr id="hour-'+response.id+'"><td><b>'+response.day+'</b></td><td>'+response.from_hour+' - '+response.to_hour+'</td><td><a href="#" class="remove_hour" data-url="/accounts/vendor/opening-hours/remove/'+response.id+'/">Remove</a></td></tr>';
                        }
                        $('.opening_hours').append(html)
                        document.getElementById("opening_hours").reset();
                    }else{
                        swal(response.message, '', "error")
                    }
                }
            })
        }else{
            swal('Please Fill All Fields','','info');
        }
    })

    //Delete Opening Hour
    $(document).on('click', '.remove_hour', function(e){
        e.preventDefault();
        url = $(this).attr('data-url');

        $.ajax({
            type:"GET",
            url : url ,
            success:function(response){
                if (response.status=='success'){
                    document.getElementById('hour-'+response.id).remove()
                }
            }
        })
    })

    
    //document ready closed 
});