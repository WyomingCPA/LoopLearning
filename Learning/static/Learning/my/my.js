﻿$(document).ready(function () {
    $("a[id^='opener']").click(function () {
        var elem = $(this).text();
        var number = elem.split('-')
        var dialog = '#dialog-' + number[1]

        $(dialog).dialog({
            modal: true,
            width: 600,
            height: 500,
        });

        return false;      
    });

    tinymce.init({
        selector: "textarea",  // change this value according to your HTML
        plugins: "codesample",
        toolbar: "codesample"
    });

});