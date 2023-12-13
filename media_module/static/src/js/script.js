odoo.define('media_module.select_media', function (require) {
'use strict';

var publicWidget = require('web.public.widget');

publicWidget.registry.SelectMedia = publicWidget.Widget.extend({
    selector: '.js_media_div',
    events : {
        'change select' : "_chnage_selection"
    },
    _chnage_selection(event){
        // Here this queryselectror gives value in nodeList
        // We use queryselectorall beacuase of selecting multiple images and videos
        const imageItems = $('.js_media_image');
        const videoItems = $('.js_media_video');

        if (event.target.value === 'Image') {
            imageItems.removeClass('d-none')
            videoItems.addClass('d-none')
            // imageItems.[i].style.display = 'none';
        }else if (event.target.value === 'Video') {
            videoItems.removeClass('d-none')
            imageItems.addClass('d-none')
        }else{
            videoItems.addClass('d-none')
            imageItems.addClass('d-none')
        }
    }
});
});

// $(document).ready(function (){
//     $("#media_type").on("change",function(){
//         var selectedValue = $(this).val();
//         if(selectedValue === "Image") {
//             $("img").show();
//             $("video").hide();
//         }
//         else if(selectedValue === "Video"){
//             $("img").hide();
//             $("video").show();
//         }
//     });
// });