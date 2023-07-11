'use strict'
$(window).on('load', function () {
    $('.footer').addClass('text-white');

    /* swiper slider */
    var swiperonboarding = new Swiper(".onboarding-swiper", {
        noSwiping: true,
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
        },
        navigation: {
            nextEl: '.btn-next',
            prevEl: '.btn-prev',
        },
    });
    swiperonboarding.on('reachEnd', function () {
        /* reach at last slide show finish*/
        swiperonboarding.on('slideChange', function () {
            $('.btn-next').prop('disabled', false).removeClass('swiper-button-disabled').on('click', function () {
                $(this).prop('disabled', false).html('<div class="spinner-border text-white spinner-border-sm" role="status"><span class= "visually-hidden"> Loading...</span></div>');
                setTimeout(function () {
                    window.location.replace("onboarding-summary.html");
                }, 1500)
            });
        });
    });

    /* upload pic*/
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                var userimg;
                userimg = 'url("' + e.target.result + '")';
                $('#userphotoonboarding').parent().css('background-image', userimg);
                setCookie('AdminUXuserimg', userimg, 1);
                sessionStorage.setItem('AdminUXuserimg1', userimg);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#userphotoonboarding").change(function () {
        readURL(this);
    });

    /* user name value  */
    $('#usernamevalue').on('keyup focusout', function () {
        setCookie('AdminUXusername', $(this).val(), 1);
    });

    /* upload logo */
    $("#companylogolightinput").change(function () {
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#companylogolight').attr('src', e.target.result);
                $('.header .navbar-brand img').attr('src', e.target.result);
                sessionStorage.setItem('AdminUXlogopath', e.target.result);
            }
            reader.readAsDataURL(this.files[0]);
        }
    });

    /* domain select */
    $('#domain-select').find('.select-box').each(function () {
        $(this).on('click', function () {
            $('#domain-select .select-box').removeClass('selected')
            $(this).addClass('selected');
            setCookie('AdminUXbusiness', $(this).attr('data-title'), 1);
        });
    });

    /* theme select */
    $('#theme-select').find('.select-box').each(function () {
        $(this).on('click', function () {
            $('#theme-select .select-box').removeClass('selected')
            $(this).addClass('selected');

        });
    });

    /* loader */
    if ($('#timer').length > 0) {
        $('#timer').innerHTML = '0' + ':' + '20';

        startTimer();
        function startTimer() {
            var presentTime = $('#timer').html();
            var timeArray = presentTime.split(/[:]+/);
            var m = timeArray[0];
            var s = checkSecond((timeArray[1] - 1));
            if (s == 59) {
                m = m - 1
            }
            if (m < 0) {
                return
            }
            $('#timer').html(m + ":" + s);
            setTimeout(startTimer, 1000);

            /* redirect page on timer ends */
            if (m === '0' && s === '00') {
                redirectpage()
            }
        }
        function checkSecond(sec) {
            if (sec < 10 && sec >= 0) {
                sec = "0" + sec
            }; // add zero in front of numbers < 10
            if (sec < 0) {
                sec = "59"
            };
            return sec;
        }
    }

    /* redirect page */
    function redirectpage() {
        if (getCookie('AdminUXbusiness') === '' || getCookie('AdminUXbusiness') === 'undefined' || getCookie('AdminUXbusiness') === 'null') {
            window.location.replace('home.html');
        } else {
            window.location.replace(getCookie('AdminUXbusiness') + '-dashboard.html');
        }
    }

    if (getCookie('AdminUXbusiness') != '' || getCookie('AdminUXbusiness') != 'undefined') {
        $('#redirecttolink').attr('href', '' + getCookie('AdminUXbusiness') + '-dashboard.html');
    } else {
        $('#redirecttolink').attr('href', 'home.html');
    }

    /* summary set image **/
    if (sessionStorage.getItem('AdminUXuserimg1') != '') {
        $('#userimage').parent().css('background-image', sessionStorage.getItem('AdminUXuserimg1'));
        $('#userphotoonboarding').parent().css('background-image', sessionStorage.getItem('AdminUXuserimg1'));
    }
    if (getCookie('AdminUXusername') != '') {
        $('#usernamedisplay').html(getCookie('AdminUXusername'));
        console.log(getCookie('AdminUXusername'))
    }

});
