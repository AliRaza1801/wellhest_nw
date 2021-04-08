var map_results = null

function render(results){
  var listBox = document.querySelector('.location-list')
  map_results = results
  listBox.innerHTML = map_results.map(result => `<button type="button" onclick="placeDetails(event)" class="btn btn-light" id=${result.place_id} >${result.name}: ${result.formatted_address}</button>`).join('');
}

function selectLocation(result){
  // Fill data
  document.querySelector('#lat').value = result.geometry.location.lat
  document.querySelector('#lng').value = result.geometry.location.lng
  document.querySelector('#place_id').value = result.place_id
  document.querySelector('#add').value = result.formatted_address
  var locale_obj = result.address_components.find(addr => addr.types.includes('sublocality_level_1'))
  if (locale_obj){
    document.querySelector('#locale').value = locale_obj.long_name
  }
  var city_obj = result.address_components.find(addr => addr.types.includes('administrative_area_level_2'))
  if (city_obj){
    document.querySelector('#city').value = city_obj.long_name
  }
  var pin_obj = result.address_components.find(addr => addr.types.includes('postal_code'))
  if (pin_obj){
    document.querySelector('#pin').value = pin_obj.long_name
  }
  // Clear Search
  var listBox = document.querySelector('.location-list')
  map_results = []
  listBox.innerHTML = ''
}