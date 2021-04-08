var morningTimes =  ["09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM"]
var afternoonTimes = ["12:00 PM", "12:30 PM", "01:00 PM", "01:30 PM", "02:00 PM", "02:30 PM", "03:00 PM", "03:30 PM",]
var eveningTimes = ["04:00 PM", "04:30 PM", "05:00 PM", "05:30 PM", "06:00 PM", "06:30 PM", "07:00 PM", "07:30 PM", "08:00 PM", "08:30 PM", "09:00 PM", "09:30 PM", "10:00 PM",]

function selectTime(e) {
    $('.SelectTime ul li').removeClass('selected');
    $(e.target).addClass('selected');
    document.querySelector('.checkout').querySelector('input[name="time"]').value = e.target.textContent
//    try {
//
//    }catch(err) {
//        alert("Please select a Booking first")
//        $('.SelectTime ul li').removeClass('selected');
//    }
}

function selectShift(e){
    $('.ApponintmentShifts ul li').removeClass('selectedShift');
    $(e.target).addClass('selectedShift');
    $('.morning').hide()
    $('.afternoon').hide()
    $('.evening').hide()
    $(`.${e.target.textContent.toLowerCase()}`).show()
}

function dateSelect(formattedDate, date, inst){
    document.querySelector('.checkout').querySelector('input[name="date"]').value = formattedDate
//    try{
//
//    }catch(err) {
//        if (formattedDate){
//            alert("Please select a Booking first")
//        }
//        datePicker.data().datepicker.clear()
//    }
}

function submitCheckout(e){
    e.preventDefault()
    var time = e.target.querySelector('input[name="time"]').value
    var date = e.target.querySelector('input[name="date"]').value
    if (time && date){
        e.target.submit()
    } else {
        alert('Please Select Date and Time')
    }
}

//function selectBooking(e){
//    //Change Booking Selection
//    $('.selectBooking').removeClass('selected');
//    target = e.currentTarget || e.target
//    $(target).addClass('selected');
//
//    //Update Datepicker Date
//    date = target.querySelector('input[name="date"]').value
//    if (date){
//        datePicker.data().datepicker.selectDate(new Date(date))
//    } else {
//        datePicker.data().datepicker.clear()
//    }
//    //Update Timepicker Time
//    time = target.querySelector('input[name="time"]').value
//    $('.SelectTime ul li').removeClass('selected');
//    $('.ApponintmentShifts ul li').removeClass('selectedShift');
//    $('.morning').hide()
//    $('.afternoon').hide()
//    $('.evening').hide()
//    if (time){
//        if (morningTimes.includes(time)){
//            $('#morningShift').addClass('selectedShift');
//            $('.morning').show()
//        }
//        if (afternoonTimes.includes(time)){
//            $('#afternoonShift').addClass('selectedShift');
//            $('.afternoon').show()
//        }
//        if (eveningTimes.includes(time)){
//            $('#eveningShift').addClass('selectedShift');
//            $('.evening').show()
//        }
//        $(`li:contains(${time})`).addClass('selected');
//    } else {
//        $('#morningShift').addClass('selectedShift');
//        $('.morning').show()
//    }
//}

//function submitCheckout(e){
//    e.preventDefault()
//    data = []
//    error = false
//    for (booking of document.getElementsByClassName('selectBooking')){
//        id = booking.querySelector('input[name="id"]').value
//        time = booking.querySelector('input[name="time"]').value
//        date = booking.querySelector('input[name="date"]').value
//        if (time && date){
//            data.push({
//                id: id,
//                time: time,
//                date: date
//            })
//        } else {
//            error = 'Please Select Date and Time'
//            $(booking).click()
//            break
//        }
//    }
//    if (!error){
//        $.ajax({
//          type: "POST",
//          contentType: "application/json",
//          url: e.currentTarget.action,
//          data: JSON.stringify(data),
//          dataType: "json",
//          success: function(data){
//            console.log(data)
//            window.location = data.redirect_url;
//          },
//        });
//    } else {
//        alert(error)
//    }
//}