define(['jquery','bootstrap_popover', 'bootstrap' ], function ($) {
    $(document).ready(function () {
        console.log("chargement JS inside_data_tab.js OK");





        $('.dataTables_length').append("  <a href='#' data-toggle='modal' data-target='#export_marks'  class='btn btn-default pull-right'><i class='bi bi-file-arrow-down'></i> Exporter les scores</a>  ") ;



    });
});