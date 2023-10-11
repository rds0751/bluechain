; (function ($) {
    "use strict";

    $(document).ready(function () {

        /**-----------------------------
         *  Navbar fix
         * ---------------------------*/
        $(document).on('click', '.navbar-area .navbar-nav li.menu-item-has-children>a', function (e) {
            e.preventDefault();
        })
       
        /*-------------------------------------
            menu
        -------------------------------------*/
        $('.navbar-area .menu').on('click', function() {
            $(this).toggleClass('open');
            $('.navbar-area .navbar-collapse').toggleClass('sopen');
        });
    
        // mobile menu
        if ($(window).width() < 992) {
            $(".in-mobile").clone().appendTo(".sidebar-inner");
            $(".in-mobile ul li.menu-item-has-children").append('<i class="fas fa-chevron-right"></i>');
            $('<i class="fas fa-chevron-right"></i>').insertAfter("");

            $(".menu-item-has-children a").on('click', function(e) {
                // e.preventDefault();

                $(this).siblings('.sub-menu').animate({
                    height: "toggle"
                }, 300);
            });
        }

        var menutoggle = $('.menu-toggle');
        var mainmenu = $('.navbar-nav');
        
        menutoggle.on('click', function() {
            if (menutoggle.hasClass('is-active')) {
                mainmenu.removeClass('menu-open');
            } else {
                mainmenu.addClass('menu-open');
            }
        });
    
        

        /* -----------------------------------------------------
            Variables
        ----------------------------------------------------- */
        var leftArrow = '<i class="fa fa-angle-left"></i>';
        var rightArrow = '<i class="fa fa-angle-right"></i>';

        /* -------------------------------------------------------------
            fact counter
        ------------------------------------------------------------- */
        $('.counter').counterUp({
            delay: 15,
            time: 2000,
        });

        /* -------------------------------------------------------------
            swiper-slider
        ------------------------------------------------------------- */            
        var swiper = new Swiper('.swiper-container', {
            mode:'horizontal',
            loop: true,
            speed: 950,
            effect: 'coverflow',
            grabCursor: true,
            centeredSlides: true,
            slidesPerView: 'auto',
            nextButton: '.arrow-right',
            prevButton: '.arrow-left',
            coverflowEffect: {
                rotate: 0,
                stretch: 180,
                depth: 180,
                smodifier: 1,
                slideShadows : false,
            },
            pagination: {
                el: '.swiper-pagination',
            },
                // Navigation arrows
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            breakpoints: {
                500: {
                    coverflowEffect: {
                        rotate: 0,
                        stretch: 140,
                        depth: 140,
                        smodifier: 1,
                        slideShadows : false,
                    }
                },
                600: {
                    coverflowEffect: {
                        rotate: 0,
                        stretch: 160,
                        depth: 160,
                        smodifier: 1,
                        slideShadows : false,
                    }
                },
                800: {
                    coverflowEffect: {
                        rotate: 0,
                        stretch: 160,
                        depth: 160,
                        smodifier: 1,
                        slideShadows : false,
                    }
                },
                1100: {
                    coverflowEffect: {
                        rotate: 0,
                        stretch: 220,
                        depth: 220,
                        smodifier: 1,
                        slideShadows : false,
                    }
                }
            }
        });


        /*------------------------------------------------
            testimonial-slider
        ------------------------------------------------*/
        $('.testimonial-slider').owlCarousel({
            loop:true,
            margin:10,
            nav:false,
            dots: true,
            center:true,
            smartSpeed: 1000,
            responsive:{
                0:{
                    items:1
                },
                600:{
                    items:2
                },
                1000:{
                    items:3
                }
            }
        })

        /*------------------------------------------------
            accordion
        ------------------------------------------------*/
        $('.collapse').collapse()



        /*--------------------------------------------
            Search Popup
        ---------------------------------------------*/
        var bodyOvrelay =  $('#body-overlay');
        var searchPopup = $('#search-popup');

        $(document).on('click','#body-overlay',function(e){
            e.preventDefault();
        bodyOvrelay.removeClass('active');
            searchPopup.removeClass('active');
        });
        $(document).on('click','.search',function(e){
            e.preventDefault();
            searchPopup.addClass('active');
        bodyOvrelay.addClass('active');
        });

        /*------------------------------------------------
            Magnific JS
        ------------------------------------------------*/
        $('.play-btn').magnificPopup({
            type: 'iframe',
            removalDelay: 260,
            mainClass: 'mfp-zoom-in',
        });
        $.extend(true, $.magnificPopup.defaults, {
            iframe: {
                patterns: {
                    youtube: {
                        index: 'youtube.com/',
                        id: 'v=',
                        src: 'https://www.youtube.com/embed/Wimkqo8gDZ0'
                    }
                }
            }
        });


        /*------------------
           back to top
        ------------------*/
        $(document).on('click', '.back-to-top', function () {
            $("html,body").animate({
                scrollTop: 0
            }, 2000);
        });

    });

    $(window).on("scroll", function() {
        /*---------------------------------------
        sticky menu activation && Sticky Icon Bar
        -----------------------------------------*/
        var mainMenuTop = $(".navbar-area");
        if ($(window).scrollTop() >= 1) {
            mainMenuTop.addClass('navbar-area-fixed');
        }
        else {
            mainMenuTop.removeClass('navbar-area-fixed');
        }
        
        var ScrollTop = $('.back-to-top');
        if ($(window).scrollTop() > 1000) {
            ScrollTop.fadeIn(1000);
        } else {
            ScrollTop.fadeOut(1000);
        }
    });


    $(window).on('load', function () {

        /*-----------------
            preloader
        ------------------*/
        var preLoder = $("#preloader");
        preLoder.fadeOut(0);

        /*-----------------
            back to top
        ------------------*/
        var backtoTop = $('.back-to-top')
        backtoTop.fadeOut();

        /*---------------------
            Cancel Preloader
        ----------------------*/
        $(document).on('click', '.cancel-preloader a', function (e) {
            e.preventDefault();
            $("#preloader").fadeOut(2000);
        });

    });


    /*---------------------
        Google Map
    ----------------------*/
    if($('#map-canvas').length > 0){
      function popup_listing_map(){
         var map;        
          var myCenter=new google.maps.LatLng(53, -1.33);
          var marker=new google.maps.Marker({
              position:myCenter
          });
          function initialize() {
              var mapProp = {
                center:myCenter,
                zoom: 14,
                draggable: false,
                scrollwheel: false,
                mapTypeId:google.maps.MapTypeId.ROADMAP
              };

              map=new google.maps.Map(document.getElementById("map-canvas"),mapProp);

               //Map Marker
              var marker = new google.maps.Marker({
                  position:myCenter,
                  map: map,
              });

              google.maps.event.addListener(marker, 'click', function() {
                
              infowindow.setContent(contentString);
              infowindow.open(map, marker);

              }); 
          };

          google.maps.event.addDomListener(window, 'load', initialize);

          google.maps.event.addDomListener(window, "resize", resizingMap());

          $('#popupmodal').on('show.bs.modal', function() {
             //Must wait until the render of the modal appear, thats why we use the resizeMap and NOT resizingMap!! ;-)
             resizeMap();
          })

          function resizeMap() {
             if(typeof map =="undefined") return;
             setTimeout( function(){resizingMap();} , 400);
          }

          function resizingMap() {
             if(typeof map =="undefined") return;
             var center = map.getCenter();
             google.maps.event.trigger(map, "resize");
             map.setCenter(center); 
          } 
      }
      popup_listing_map();

    }



})(jQuery);


// Seed data to populate the donut pie chart
var seedData = [{
    "label": "20%",
    "value": 20,
    "link": "#"
}, {
    "label": "10%",
    "value": 10,
    "link": "#"
    },
    {
        "label": "15%",
        "value": 15,
        "link": "#"
    },

    {
    "label": "11%",
    "value": 11,
    "link": "#"
}, {
    "label": "5%",
    "value": 5,
    "link": "#"
    }, {
        "label": "5%",
        "value": 5,
        "link": "#"
    },
    {
        "label": "14%",
        "value": 14,
        "link": "#"
    },

    {
        "label": "10%",
        "value": 10,
        "link": "#"
    },

    {
        "label": "5%",
        "value": 5,
        "link": "#"
    },
    {
    "label": "5%",
    "value": 5,
    "link": "#"
}];

// Define size & radius of donut pie chart
var width = 330,
    height = 330,
    radius = Math.min(width, height) / 2;

// Define arc colours
var colour = d3.scaleOrdinal(d3.schemeCategory20);

// Define arc ranges
var arcText = d3.scaleOrdinal()
    .range([0, width]);

// Determine size of arcs
var arc = d3.arc()
    .innerRadius(radius - 130)
    .outerRadius(radius - 10);

// Create the donut pie chart layout
var pie = d3.pie()
    .value(function (d) { return d["value"]; })
    .sort(null);

// Append SVG attributes and append g to the SVG
var svg = d3.select("#donut-chart")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(" + radius + "," + radius + ")");

// Define inner circle
svg.append("circle")
    .attr("cx", 0)
    .attr("cy", 0)
    .attr("r", 100)
    .attr("fill", "#fff");

// Calculate SVG paths and fill in the colours
var g = svg.selectAll(".arc")
    .data(pie(seedData))
    .enter().append("g")
    .attr("class", "arc")

    // Make each arc clickable 
    .on("click", function (d, i) {
        window.location = seedData[i].link;
    });

// Append the path to each g
g.append("path")
    .attr("d", arc)
    .attr("fill", function (d, i) {
        return colour(i);
    });

// Append text labels to each arc
g.append("text")
    .attr("transform", function (d) {
        return "translate(" + arc.centroid(d) + ")";
    })
    .attr("dy", ".35em")
    .style("text-anchor", "middle")
    .attr("fill", "#fff")
    .text(function (d, i) { return seedData[i].label; })

g.selectAll(".arc text").call(wrap, arcText.range([0, width]));

// Append text to the inner circle
svg.append("text")
    .attr("dy", "-0.5em")
    .style("text-anchor", "middle")
    .attr("class", "inner-circle")
    .attr("fill", "#36454f")
    .text(function (d) { return 'DollarVridhix'; });

svg.append("text")
    .attr("dy", "1.0em")
    .style("text-anchor", "middle")
    .attr("class", "inner-circle")
    .attr("fill", "#36454f")
    .text(function (d) { return 'TOKEN'; });

// Wrap function to handle labels with longer text
function wrap(text, width) {
    text.each(function () {
        var text = d3.select(this),
            words = text.text().split(/\s+/).reverse(),
            word,
            line = [],
            lineNumber = 0,
            lineHeight = 1.1, // ems
            y = text.attr("y"),
            dy = parseFloat(text.attr("dy")),
            tspan = text.text(null).append("tspan").attr("x", 0).attr("y", y).attr("dy", dy + "em");
        console.log("tspan: " + tspan);
        while (word = words.pop()) {
            line.push(word);
            tspan.text(line.join(" "));
            if (tspan.node().getComputedTextLength() > 90) {
                line.pop();
                tspan.text(line.join(" "));
                line = [word];
                tspan = text.append("tspan").attr("x", 0).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
            }
        }
    });
}