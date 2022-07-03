$ = jQuery;
$(document).ready(function () {

    /* header scroll functionality */
    let $scrolled = 150;

    if ($('#program-nav').length) {
        var programNav = $('#program-nav')
        var programNavTop = Math.floor(programNav.offset().top - 74);
        $(document).scroll(function () {
            if ($(document).width() < 992){
                if (programNav.hasClass('program-scrolled')){
                    programNav.removeClass('program-scrolled');
                }
                return;
            }
            var currentScrollPos = $(document).scrollTop();
            if (!programNav.hasClass('program-scrolled') && currentScrollPos > programNavTop){
                programNav.addClass('program-scrolled');
                programNav.css('top', 74 );
                $('header').addClass('hidden');
                $('.programmpunkte-wrapper').css('padding-top', programNav.outerHeight());
            } else if (programNav.hasClass('program-scrolled') && $(document).scrollTop() <= programNavTop){
                programNav.removeClass('program-scrolled');
                programNav.css('top', 'unset');
                $('header').removeClass('hidden');
                $('.programmpunkte-wrapper').css('padding-top', 'unset')
            }
        });
    }

    if($('.toggler').length){
        $('.toggler').click(function(){
            var id = this.dataset.id
            if (ellipsis = document.getElementById('ellipsis-' + id)){
                ellipsis.classList.toggle('d-none');
                document.getElementById('full-text-' +id).classList.toggle('d-none');
            }
           
            var map = document.getElementById('map-' + id);
            map.classList.toggle('open');
            map.src = map.dataset.src;
            this.blur();
        })
    }

    if ($(document).scrollTop() > $scrolled) $('header').addClass('scrolled');
    $(document).scroll(function () {
        if (!$('header').hasClass('scrolled') && $(document).scrollTop() > $scrolled) {
            $('header').addClass('scrolled');
        } else if ($('header').hasClass('scrolled') && $(document).scrollTop() <= $scrolled) {
            $('header').removeClass('scrolled');
        }
    });



    /* close navbar when click somewhere else */
    $('body').click(function (e) {
        if ($('header .navbar-collapse').hasClass('show') && !$('header .menu-item > a').is(e.target)) {
            $('header .navbar-collapse').collapse('hide');
        }
    });

    /* body class "navbar-open" functionality */
    $('header .navbar-collapse').on('hidden.bs.collapse', function () {
        $('body').removeClass('navbar-open');
    }).on('show.bs.collapse', function () {
        $('body').addClass('navbar-open');
    });

    /* info-box-with-tabs functionality */
    if ($(".info-box-with-tabs").length > 0) {
        $('div[class^="tab-number"]:not(.active)').css('display', 'none');
        $('.tab-link').click(function (e) {
            e.preventDefault();
            $('.tab-link').removeClass('active');
            $(this).addClass('active');
            $('div[class^="tab-number"]').removeClass("active");
            let tabNumber = $(this).data("tabNumber");
            $('.tab-number-' + tabNumber).addClass('active').fadeIn('slow');

            if ($(window).width() < 992) {
                $([document.documentElement, document.body]).animate({
                    scrollTop: $('.tab-content').offset().top - 100
                }, 300);
            }

            //$('.tab-number-' + tabNumber)[0].scrollIntoView(true);
            $('div[class^="tab-number"]:not(.active)').css('display', 'none');
        });
    }

    /* hero-swiper initialization */
    $(".hero-swiper .owl-carousel").owlCarousel({
        items: 1,
        loop: false, // 3j
        nav: true,
        navContainerClass: 'owl-nav d-flex justify-content-end align-items-center container',
        navElement: 'a',
        navClass: ['owl-prev d-flex mr-md-5 mr-3', 'owl-next d-flex ml-md-5 ml-3'],
        navText: ['<img src="/wp-content/themes/karlsruhe-digital/images/Pfeil_Links.png">', '<img src="/wp-content/themes/karlsruhe-digital/images/Pfeil_Rechts.png">'],
        dots: false,
        margin: 0,
        autoplay: false, // 3j
        autoplayTimeout: 5000000, // 3j
        checkVisible: false,
        onInitialized: addItemNumberToNavigation,
        onChanged: changeItemNumber
    });

    /* blog-swiper initialization */
    $(".blog-swiper .owl-carousel").owlCarousel({
        items: 1,
        loop: true,
        nav: true,
        slideBy: 'page',
        navContainerClass: 'owl-nav d-flex justify-content-center align-items-center',
        navElement: 'a',
        navClass: ['owl-prev d-flex mr-4', 'owl-next d-flex ml-4'],
        navText: ['<img src="/wp-content/themes/karlsruhe-digital/images/Pfeil_Links.png">', '<img src="/wp-content/themes/karlsruhe-digital/images/Pfeil_Rechts.png">'],
        dots: false,
        margin: 0,
        responsive: {
            1200: {
                items: 3
            },
            767: {
                items: 2
            }
        },
        onInitialized: addItemNumberToNavigation,
        onChanged: changeItemNumber
    });

    /* theses-swiper initialization */
    $(".theses-swiper .owl-carousel").owlCarousel({
        items: 1,
        loop: true,
        nav: true,
        slideBy: 'page',
        navContainerClass: 'owl-nav d-flex justify-content-center align-items-center',
        navElement: 'a',
        navClass: ['owl-prev d-flex mr-4', 'owl-next d-flex ml-4'],
        navText: ['<img src="/wp-content/themes/karlsruhe-digital/images/Pfeil_Links.png">', '<img src="/wp-content/themes/karlsruhe-digital/images/Pfeil_Rechts.png">'],
        dots: false,
        margin: 0,
        responsive: {
            1200: {
                items: 3
            },
            767: {
                items: 2
            }
        },
        onInitialized: addItemNumberToNavigation,
        onChanged: changeItemNumber
    });

    /* testimonial-swiper initialization */
    $(".testimonial-swiper .owl-carousel").owlCarousel({
        items: 1,
        loop: true,
        nav: true,
        navContainerClass: 'owl-nav d-flex justify-content-center align-items-center',
        navElement: 'a',
        navClass: ['owl-prev d-flex mr-4', 'owl-next d-flex ml-4'],
        navText: ['<img src="/wp-content/themes/karlsruhe-digital/images/Pfeil_Links.png">', '<img src="/wp-content/themes/karlsruhe-digital/images/Pfeil_Rechts.png">'],
        dots: false,
        margin: 25,
        onInitialized: addItemNumberToNavigation,
        onChanged: changeItemNumber
    });

    function addItemNumberToNavigation(e) {
        var idEl = '#' + e.target.id;
        var html = '';
        var openSpanEl = '<span class="swiper-item-number">';
        var endSpanEl = '</span>';
        var itemNumber = '01';
        var countNumber = '';

        if (idEl == '#hero-swiper') {
            itemNumber = '1';
            countNumber = '<span class="color-white">/' + e.item.count + endSpanEl;
        }

        html += openSpanEl + itemNumber + endSpanEl + countNumber;

        $(idEl + ' .owl-prev').after(html);
    }

    function changeItemNumber(e) {
        var idEl = '#' + e.target.id;
        var item = e.item.index - 1;
        var count = e.item.count;

        if (idEl == '#blog-swiper' || idEl == '#theses-swiper') {
            item = e.page.index + 1;
        } else {
            if (item == 0) {
                item = count;
            } else if (item == -1) {
                item = 1;
            } else if (item > count) {
                item -= count;
            }
        }

        if (idEl != '#hero-swiper' && item < 10) {
            item = '0' + item;
        }

        $(idEl + ' .swiper-item-number').text(item);
    }

});