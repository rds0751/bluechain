'use strict'
$(document).ready(function () {

    var html = $('html');
    var body = $('body');

    /* create cookie */
    function setCookie(cname, cvalue, exdays) {
        const d = new Date();
        d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
        let expires = "expires=" + d.toUTCString();
        document.cookie = cname + "=" + cvalue + ";" + expires + ";  path=/; SameSite=None; Secure";
    }

    function getCookie(cname) {
        let name = cname + "=";
        let ca = document.cookie.split(';');
        for (let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }


    /* layout modes dark-light */
    if (getCookie("AdminUXlayoutmode") === 'dark-mode') {
        $('#btn-layout-modes-dark').prop('checked', true);
        html.addClass('dark-mode');
    } else {
        $('#btn-layout-modes-dark').prop('checked', false);
        html.removeClass('dark-mode');
    }

    $('#btn-layout-modes-dark').on('click', function () {
        if ($(this).is(':checked')) {
            setCookie('AdminUXlayoutmode', 'dark-mode', 1);
            html.attr('class', getCookie("AdminUXlayoutmode"));
        } else {
            setCookie('AdminUXlayoutmode', 'dark-mode', 1);
            html.attr('class', getCookie("AdminUXlayoutmode"));
        }
    });


    /* Right to left to right directions  */
    if (getCookie('AdminUXdirectionmode') === 'rtl') {
        $('#btn-layout-RTL').prop('checked', true);
        html.addClass('rtl');
        html.attr('dir', 'ltr');

    } else {
        $('#btn-layout-RTL').prop('checked', false);
        html.attr('dir', '');
        html.removeClass('rtl');
    }

    $('#btn-layout-RTL').on('click', function () {
        if ($(this).is(':checked')) {
            setCookie('AdminUXdirectionmode', 'rtl', 1);
            html.attr('dir', 'rtl');
            html.addClass('rtl');

        } else {
            setCookie('AdminUXdirectionmode', 'ltr', 1);
            html.attr('dir', '');
            html.removeClass('rtl');
        }
    });



    /* color style  */
    var curentstyle = body.attr('data-theme');
    if ($.type(getCookie("AdminUXtheme")) != 'undefined' && getCookie("AdminUXtheme") != '') {

        body.addClass(getCookie("AdminUXtheme"));
        body.attr('data-theme', getCookie("AdminUXtheme"));
        curentstyle = getCookie("AdminUXtheme");

        $('#theme-select .select-box').each(function () {
            if ($(this).attr('data-title') === getCookie("AdminUXtheme")) {
                $(this).addClass("active");
            }
        });
        $('.personalise-color-list li').each(function () {
            if ($(this).attr('data-title') === getCookie("AdminUXtheme")) {
                $(this).addClass("active");
            }
        });
    }

    $('.personalise-color-list li').on('click', function () {
        body.removeClass(body.attr('data-theme'));

        $('.personalise-color-list li').removeClass('active');
        var setstyle = $(this).attr('data-title');

        if ($(this).hasClass('active') != true && setstyle != '') {
            $(this).addClass('active');
            body.addClass(setstyle).attr('data-theme', setstyle);
            setCookie('AdminUXtheme', setstyle, 1);
            curentstyle = setstyle;
        }

        if ($('.personalise-preview').length > 0) {

        }
    });

    $('#theme-select').find('.select-box').each(function () {

        $(this).on('click', function () {
            $('#theme-select').find('.select-box').removeClass('active');

            if ($(this).hasClass('active') != true && setstyle != '') {
                var curentstyle = body.attr('data-theme');
                var setstyle = $(this).attr('data-title');

                $(this).addClass('active');
                body.removeClass(curentstyle).addClass(setstyle).attr('data-theme', setstyle);
                setCookie('AdminUXtheme', setstyle, 1);
                curentstyle = setstyle;
            }
        });
    });

    /* sidebar type */
    if ($.type(getCookie("AdminUXsidebarfilled")) != 'undefined' && getCookie("AdminUXsidebarfilled") != '') {
        body.addClass(getCookie("AdminUXsidebarfilled"));

        $('.personalise-preview-sidebar').each(function () {
            $(this).removeClass("active");
            if ($(this).attr('data-title') === getCookie("AdminUXsidebarfilled")) {
                $(this).addClass("active");
            }
        });
    }
    $('.personalise-preview-sidebar').on('click', function () {
        var setSidebarfill = $(this).attr('data-title');

        $('.personalise-preview-sidebar').removeClass('active');
        $(this).addClass("active");

        if (setSidebarfill != "") {
            body.removeClass(getCookie("AdminUXsidebarfilled")).addClass(setSidebarfill);
            setCookie('AdminUXsidebarfilled', setSidebarfill, 1);
        } else {
            body.removeClass(getCookie("AdminUXsidebarfilled"));
            removeCookie('AdminUXsidebarfilled');
        }
    });



    /* sidebar style */
    var currentstyle = body.attr('data-sidebarstyle');
    if ($.type(getCookie("AdminUXsidebarStyle")) != 'undefined' && getCookie("AdminUXsidebarStyle") != '') {
        body.removeClass(currentstyle).addClass(getCookie("AdminUXsidebarStyle")).attr('data-sidebarstyle', getCookie("AdminUXsidebarStyle"));

        $('.sidebarstyle').each(function () {
            $(this).removeClass("active");
            if ($(this).attr('data-title') === getCookie("AdminUXsidebarStyle")) {
                $(this).addClass("active");
            }
        });
    }
    $('.sidebarstyle').on('click', function () {
        var setSidebarStyle = $(this).attr('data-title');
        body.attr('data-sidebarstyle', setSidebarStyle);

        $('.sidebarstyle').removeClass('active');
        $(this).addClass("active");

        if (setSidebarStyle != "") {
            body.removeClass(getCookie("AdminUXsidebarStyle")).addClass(setSidebarStyle);
            setCookie('AdminUXsidebarStyle', setSidebarStyle, 1);
        } else {
            body.removeClass(getCookie("AdminUXsidebarStyle"));
            removeCookie('AdminUXsidebarStyle');
        }
    });


    /* header logo, photo and user name */
    if ("AdminUXlogopath" in sessionStorage) {
        $('.header .navbar-brand img').attr('src', sessionStorage.getItem('AdminUXlogopath'));
    }
    if ("AdminUXuserimg1" in sessionStorage) {
        $('#userprofiledd img, #userphotoonboarding3, .ususerphotoonboarding').parent().css('background-image', sessionStorage.getItem('AdminUXuserimg1'));
    }
    if (getCookie('AdminUXusername') != '') {
        $('#userprofiledd .username').html(getCookie('AdminUXusername'));
    }

});