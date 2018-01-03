jQuery(document).ready(function () {
    jQuery('[data-toggle="tooltip"]').tooltip();
    jQuery('#opener').click(function () {
        jQuery("#dialog").dialog();
    });
});