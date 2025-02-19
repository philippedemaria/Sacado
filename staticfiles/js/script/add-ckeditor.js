define(['jquery',  'bootstrap', 'ckeditor'], function ($) {
    $(document).ready(function () {


    console.log(" add-ckeditor chargé ");


    if ( $("#id_title").length > 0 ) {

        CKEDITOR.replace('id_title', {
            height: '200px',
            toolbar:    
                [  
                    { name: 'clipboard', groups: [ 'clipboard', 'undo' ], items: [ 'Source', '-','Copy', 'Paste', 'PasteText' ] },
                    { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ], items: [ 'NumberedList', 'BulletedList', '-',   'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock' ] }, 
                    { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ], items: [ 'Bold', 'Italic', 'Underline',  ] },
                ] ,
        });

        if ( $("#text_to_set").length > 0 )
        { text_to_set = $("#text_to_set").val() ; 
        CKEDITOR.instances['id_title'].setData(text_to_set) ; 
        }
    
    }



    if ( $("#id_filltheblanks").length > 0 ) {

        CKEDITOR.replace('id_filltheblanks', {
            height: '200px',
            toolbar:    
                [  
                    { name: 'clipboard', groups: [ 'clipboard', 'undo' ], items: [ 'Source', '-', 'Copy', 'Paste', 'PasteText' ] },
                    { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ], items: [ 'NumberedList', 'BulletedList', '-',   'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock' ] }, 
                    { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ], items: [ 'Bold', 'Italic', 'Underline','-','Table','-', 'HorizontalRule'] },

                ] ,
        });
    }



    $("#loading").hide(500); 

  // Affiche dans la modal la liste des élèves du groupe sélectionné
    $('#id_levels').on('change', function (event) {
        let id_level = $(this).val();
        let id_subject = $("#id_subject").val();
        let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
        $("#loading").html("<i class='fa fa-spinner fa-pulse fa-fw'></i>");
        $("#loading").show(); 
        $.ajax(
            {
                type: "POST",
                dataType: "json",
                traditional: true,
                data: {
                    'id_level': id_level,
                    'id_subject': id_subject,                        
                    csrfmiddlewaretoken: csrf_token
                },
                url : "../../qcm/ajax/chargethemes_parcours",
                success: function (data) {

                    themes = data["themes"];
                    $('select[name=themes]').empty("");
                    if (themes.length >0)

                    { for (let i = 0; i < themes.length; i++) {
                                

                                console.log(themes[i]);
                                let themes_id = themes[i][0];
                                let themes_name =  themes[i][1]  ;
                                let option = $("<option>", {
                                    'value': Number(themes_id),
                                    'html': themes_name
                                });
                                $('select[name=themes]').append(option);
                            }
                    }
                    else
                    {
                        let option = $("<option>", {
                            'value': 0,
                            'html': "Aucun contenu disponible"
                        });
                        $('select[name=themes]').append(option);
                    }
                    $("#loading").hide(500); 
                }
            }
        )
    });


    $('input[name=waitings]').on('click', function (event) {

            let waitings = $(this).val();
            let id_subject = $("#id_subject").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            $("#loading").html("<i class='fa fa-spinner fa-pulse fa-fw'></i>");
            $("#loading").show(); 

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'waitings': waitings,                     
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : "../../tool/ajax_chargeknowledges",
                    success: function (data) {

                        knowledges = data["knowledges"];
                        for (let i = 0; i < knowledges.length; i++) {
                                
                                let knowledges_id = knowledges[i][0];
                                
                                $('hidden_knowledges').hide(500);
                                $('knowledge'+knowledges_id).show(500);
                            }
                      
                        $("#loading").hide(500); 
                    }
                }
            )
    });


    // Fonction de sélection du Vrai faux
    function checked_vf(){ 
            if( $("#check1").hasClass("checked")  )  
                {   
                    // Gestion du check
                    $('#check1').removeClass("checked");
                    $('#check2').addClass("checked");
                    // affiche du fa
                    $('#check1').css("display","none");
                    $('#noCheck1').css("display","block");
                    $('#check2').css("display","block");
                    $('#noCheck2').css("display","none");
                    $("#id_is_correct").prop("checked", false); 
                } 
            else 
                {   
                    // Gestion du check
                    $('#check1').addClass("checked");
                    $('#check2').removeClass("checked");
                    // affiche du fa
                    $('#check2').css("display","none");
                    $('#noCheck2').css("display","block");
                    $('#check1').css("display","block");
                    $('#noCheck1').css("display","none");
                    $("#id_is_correct").prop("checked", true); 
                }             
        }

        $('body').on('click', '#vf_zone1' , function (event) {  
            checked_vf() ;
        }); 
        $('body').on('click', '#vf_zone2' , function (event) {  
            checked_vf() ;
        }); 

 


        $("#id_calculator").prop("checked", false);   
        $("#id_is_publish").prop("checked", true); 


        $('body').on('click', '#checking_zone0' , function (event) {  
            checked_and_checked(0) ;
        });
        $('body').on('click', '#checking_zone1' , function (event) {  
            checked_and_checked(1) ;
        });
        $('body').on('click', '#checking_zone2' , function (event) {  
            checked_and_checked(2) ;
        });
        $('body').on('click', '#checking_zone3' , function (event) {  
            checked_and_checked(3) ;
        });


        function checked_and_checked(nb){ 
                qtype = $("#qtype").val() ;

                if( $("#check"+nb).hasClass("checked")  )  
                    {   
                        $('#check'+nb).removeClass("checked");
                        $('#check'+nb).css("display","none");
                        $('#noCheck'+nb).css("display","block");
                        $("#id_choices-"+nb+"-is_correct").prop("checked", false);                         

                    } 
                else 
                    {   
                        $('#check'+nb).addClass("checked");
                        $('#check'+nb).css("display","block");
                        $('#noCheck'+nb).css("display","none");
                        $("#id_choices-"+nb+"-is_correct").prop("checked", true);                     
                    }
 
                if (qtype==4 && $(".checked").length > 1 ) { 
                    alert("Vous avez choisi un QCS dans lequel une seule réponse est autorisée. Optez pour le QCM alors.") ; 
                    $('#check'+nb).removeClass("checked");
                    $('#check'+nb).css("display","none");
                    $('#noCheck'+nb).css("display","block");
                    $("#id_choices-"+nb+"-is_correct").prop("checked", false);                         
                    return false;
                }
            }
 


 
       // Trie des diapositives
        $('#questions_sortable_list').sortable({
            start: function( event, ui ) { 
                   $(ui.item).css("box-shadow", "2px 1px 2px gray").css("background-color", "#271942").css("color", "#FFF"); 
               },
            stop: function (event, ui) {

                var valeurs = "";
                         
                $(".sorted_question_id").each(function() {
                    let this_question_id = $(this).val();
                    valeurs = valeurs + this_question_id +"-";
                });


                $(ui.item).css("box-shadow", "0px 0px 0px transparent").css("background-color", "#dbcdf7").css("color", "#271942"); 

                $.ajax({
                        data:   { 'valeurs': valeurs ,   } ,   
                        type: "POST",
                        dataType: "json",
                        url: "../../question_sorter" 
                    }); 
                }
            });



        $('body').on('change', '.choose_imageanswer' , function (event) {
            var tab =  $(this).attr('id').split("-");
            previewFile(tab[1],"bgcolorRed") ;
         });


        $('body').on('change', '.choose_imageanswerbis' , function (event) {
            var tab =  $(this).attr('id').split("-");
            previewFilebis(tab[1],"bgcolorRed") ;
         });    


        $('body').on('click', '.delete_img' , function (event) {
            var tab =  $(this).attr('id').split("img");
            noPreviewFile(tab[1],"bgcolorRed") ;
         });


        $('body').on('click', '.delete_imgbis' , function (event) {
            var tab =  $(this).attr('id').split("bis");
            noPreviewFilebis(tab[1],"bgcolorRed") ;
         });    



        $('body').on('change', '.choose_imageanswersub' , function (event) {
            var tab =  $(this).parent().find("i:first").attr('id').split("sub");           
            previewFileSub(tab[1],"bgcolorRed") ;
         });    


        $('body').on('click', '.delete_subimg' , function (event) {
            var tab =  $(this).attr('id').split("img");
            nopreviewFileSub(tab[1],"bgcolorRed") ;
         });


        function previewFile(nb,classe) {

            const preview = $('#preview'+nb);
            const file = $('#id_choices-'+nb+'-imageanswer')[0].files[0];
            const reader = new FileReader();


            $("#preview"+nb).val("") ;  
            $("#answer"+nb+"_div").addClass(classe) ;
            $("#id_choices-"+nb+"-answer").addClass("preview") ;
            $("#preview"+nb).removeClass("preview") ; 
            $("#delete_img"+nb).removeClass("preview") ; 

            reader.addEventListener("load", function (e) {
                                                var image = e.target.result ; 
                                                $("#preview"+nb).attr("src", image );
                                            }) ;

            if (file) { 
              reader.readAsDataURL(file);
            }            

          }


        function noPreviewFile(nb,classe) {

                $("#preview"+nb).attr("src", "" );
                $("#answer"+nb+"_div").removeClass(classe) ;
                $("#id_choices-"+nb+"-answer").removeClass("preview") ;
                $("#preview"+nb).addClass("preview") ; 
                $("#delete_img"+nb).addClass("preview") ;      
          }

        function previewFilebis(nb,classe) {

            const preview = $('#preview_bis'+nb);
            const file = $('#id_choices-'+nb+'-imageanswerbis')[0].files[0];
            const reader = new FileReader();


            $("#preview_bis"+nb).val("") ;  
            $("#answerbis"+nb+"_div").addClass(classe) ;
            $("#id_choices-"+nb+"-answerbis").addClass("preview") ;
            $("#preview_bis"+nb).removeClass("preview") ; 
            $("#delete_imgbis"+nb).removeClass("preview") ; 

            reader.addEventListener("load", function (e) {
                                                var image = e.target.result ; 
                                                $("#preview_bis"+nb).attr("src", image );
                                            }) ;

            if (file) { 
              reader.readAsDataURL(file);
            }            

          }


        function noPreviewFilebis(nb,classe) {

                $("#preview_bis"+nb).attr("src", "" );
                $("#answerbis"+nb+"_div").removeClass(classe) ;
                $("#id_choices-"+nb+"-answerbis").removeClass("preview") ;
                $("#preview_bis"+nb).addClass("preview") ; 
                $("#delete_imgbis"+nb).addClass("preview") ;      
          }



        function previewFileSub(nb,classe) {



            subtab = nb.split("-") ; 

            const preview = $('#previewsub'+nb);
            const file = $('#subformsetZone'+subtab[0]+' #id_subchoices-'+subtab[1]+'-imageanswer')[0].files[0];
            const reader = new FileReader();


            $("#previewsub"+nb).val("") ;  
            $('#subformsetZone'+subtab[0]+' #id_subchoices-'+subtab[1]+'-answer').addClass("preview") ;
            $("#previewsub"+nb).removeClass("preview") ; 
            $("#delete_subimg"+nb).removeClass("preview") ; 

            reader.addEventListener("load", function (e) {
                                                var image = e.target.result ; 
                                                $("#previewsub"+nb).attr("src", image );
                                            }) ;

            if (file) { 
              reader.readAsDataURL(file);
            }            

          }


        function nopreviewFileSub(nb,classe) {

            subtab = nb.split("-") ;

            $("#previewsub"+nb).attr("src", "" );
            $('#subformsetZone'+subtab[0]+' #id_subchoices-'+subtab[1]+'-answer').removeClass("preview") ;
            $("#previewsub"+nb).addClass("preview") ; 
            $("#delete_subimg"+nb).addClass("preview") ;      
          }


 
        $("#support_image").on('click', function (event) {

            get_the_target("#support_image","#drop_zone_image","#video_div","#audio_div")

        })



        $("#support_video").on('click', function (event) { 

            get_the_target("#support_video","#video_div","#drop_zone_image","#audio_div")

        })



        $("#support_audio").on('click', function (event) { 

            get_the_target("#support_audio","#audio_div","#drop_zone_image","#video_div")

        })


        $("#support_audio_image").on('click', function (event) { 

            get_the_target_2("#support_audio_image","#drop_zone_image","#audio_div","#video_div")

        })

 
        function get_the_target(target,cible,f1,f2){

            $(f1).removeClass("allowed_display");
            $(f2).removeClass("allowed_display");
            $(f1).addClass("not_allowed_display");
            $(f2).addClass("not_allowed_display");

            if ($(cible).hasClass("not_allowed_display")) 
            {
                $(cible).removeClass("not_allowed_display");
                $(cible).addClass("allowed_display");
            } else {
                $(cible).removeClass("allowed_display");                
                $(cible).addClass("not_allowed_display");
            }
        }

        function get_the_target_2(target,cible,f1,f2){

            $(f1).removeClass("allowed_display");
            $(f2).removeClass("allowed_display");
            $(f1).addClass("not_allowed_display");
            $(f2).addClass("not_allowed_display");

            if ($(cible).hasClass("not_allowed_display")) 
            {
                $(cible).removeClass("not_allowed_display");
                $(cible).addClass("allowed_display");
                $(f1).removeClass("not_allowed_display");
                $(f1).addClass("allowed_display");
            } else {
                $(cible).removeClass("allowed_display");                
                $(cible).addClass("not_allowed_display");
                $(f1).removeClass("not_allowed_display");
                $(f1).addClass("allowed_display");
            }
        }



        function asnwerfontsize(choice) {

            let fs ;
            if ( choice.length > 50) { fs = 1.2 ;}
            else if ( choice.length > 17) { fs = 1.7 ;}
            else if ( choice.length > 10) { fs = 2.5 ;}
            else { fs = 3 ;}

            return fs;
        }


        // Chargement d'une image dans la réponse possible.
        $('body').on('click', '.automatic_insertion' , function (event) {  
 
            var feed_back = $(this).attr('id');
            $("#div_"+feed_back).toggle(500);

         });

 

        $('body').on('click', '#show_randomize_zone' , function (event) { 
            $('#pseudorandomize_zone').hide(500);
            $('#randomize_zone').toggle(500);
         });

        $('body').on('click', '#show_pseudorandomize_zone' , function (event) { 
            $('#randomize_zone').hide(500);
            $('#pseudorandomize_zone').toggle(500);
         });



        $(document).on('click', '.add_more', function (event) { 

                var total_form = $('#id_choices-TOTAL_FORMS') ;
                var totalForms = parseInt(total_form.val())  ;

                var thisClone = $('#rowToClone');
                rowToClone = thisClone.html() ;

                console.log(totalForms) ; 

                $('#formsetZone').append(rowToClone);

                $('#duplicate').attr("id","duplicate"+totalForms) 
                //$('#cloningZone').attr("id","cloningZone"+totalForms) 

                $('#duplicate'+totalForms).find('.delete_button').html('<a href="javascript:void(0)" class="btn btn-danger remove_more" ><i class="fa fa-trash"></i></a>'); 
                $('#duplicate'+totalForms).find("input[type='checkbox']").bootstrapToggle();

                $("#duplicate"+totalForms+" input").each(function(){ 
                    $(this).attr('id',$(this).attr('id').replace('__prefix__',totalForms));
                    $(this).attr('name',$(this).attr('name').replace('__prefix__',totalForms));
                });

                $("#duplicate"+totalForms+" textarea").each(function(){ 
                    $(this).attr('id',$(this).attr('id').replace('__prefix__',totalForms));
                    $(this).attr('name',$(this).attr('name').replace('__prefix__',totalForms));
                });

 
                // $('#duplicate'+totalForms+" .onclic").attr('data-counter', totalForms);
                // $('#duplicate'+totalForms+" .onclic").addClass('onclic'+totalForms);

                // $('#duplicate'+totalForms+" .show_onclic").addClass('show_onclic'+totalForms);
                // $('#duplicate'+totalForms+" #show_variable").attr('id','show_variable'+totalForms);
                // $('#duplicate'+totalForms+" #show_numeric").attr('id','show_numeric'+totalForms);
                // $('#duplicate'+totalForms+" #show_textuel").attr('id','show_textuel'+totalForms);
                // $('#duplicate'+totalForms+" #show_image").attr('id','show_image'+totalForms);
                // $('#id_images-TOTAL').attr('id','id_images-TOTAL'+totalForms);
                // $('#id_images-TOTAL'+totalForms).val(totalForms);

                total_form.val(totalForms+1);

            });



        $(document).on('click', '.remove_more', function () {
            var total_form = $('#id_choices-TOTAL_FORMS') ;
            var totalForms = parseInt(total_form.val())-1  ;

            $('#duplicate'+totalForms).remove();
            total_form.val(totalForms)
        });


 

        // $(document).on('click', '.add_more_image', function (event) {


        //     var total_form     = $('#id_variableqs-TOTAL_FORMS') ;
        //     var totalForms     = parseInt(total_form.val())-1  ;
        //     var variable       = $("#id_variableqs-"+totalForms+"-name").val();
        //     var selector_image = $('#id_images-TOTAL'+totalForms) ;
        //     var number_image   = parseInt(selector_image.val());
        //     var thisClone      = $('#imageToClone') ;
        //     var imageToClone   = thisClone.html() ;

        //     if (variable=="") { alert("Nommer la variable"); return false;}

        //     $('#cloningZone'+totalForms).append(imageToClone);
        //     $('#duplicateImage').attr("id","duplicateImage"+number_image) 
        //     $('#duplicateImage'+number_image+" input").each(function(){ 
        //         $(this).attr('id',$(this).attr('id').replace('__var__',variable));
        //         $(this).attr('id',$(this).attr('id').replace('__nbr__',number_image));
        //         $(this).attr('name',$(this).attr('name').replace('__var__',variable));
        //         $(this).attr('name',$(this).attr('name').replace('__nbr__',number_image));
        //     });


        //     selector_image.val(number_image + 1);

        //     });



        // $(document).on('click', '.remove_more_image', function () {
        //     $(this).parent().parent().remove();
        // });



 


        // $(document).on('click', '.onclic', function () {
        //     var type = $(this).data('type');
        //     var counter = $(this).data('counter');

        //     $('#show_variable'+counter).show();
        //     $('.show_onclic'+counter).hide();
        //     $('#show_'+type+counter).show();


        //     $('#duplicate'+counter+" .onclic").removeClass('btn-sacado_active').addClass('btn-secondary');
        //     $(this).addClass('btn-sacado_active');
        // });

 

        $(document).on('click', '.add_more_question', function (event) { 

                var total_form = $('#id_variableqs-TOTAL_FORMS') ;
                var totalForms = parseInt(total_form.val())  ;

                var thisClone = $('#rowToClone_question');
                rowToClone = thisClone.html() ;

                console.log(totalForms) ; 

                $('#formsetZone_question').append(rowToClone);

                $('#duplicate_question').attr("id","duplicate_question"+totalForms) 
                //$('#cloningZone').attr("id","cloningZone"+totalForms) 

                $('#duplicate_question'+totalForms).find('.delete_button_question').html('<a href="javascript:void(0)" class="btn btn-danger remove_more_question" ><i class="fa fa-trash"></i></a>'); 
                $('#duplicate_question'+totalForms).find("input[type='checkbox']").bootstrapToggle();

                $("#duplicate_question"+totalForms+" input").each(function(){ 
                    $(this).attr('id',$(this).attr('id').replace('__prefix__',totalForms));
                    $(this).attr('name',$(this).attr('name').replace('__prefix__',totalForms));
                });
 
                // $('#duplicate'+totalForms+" .onclic").attr('data-counter', totalForms);
                // $('#duplicate'+totalForms+" .onclic").addClass('onclic'+totalForms);

                // $('#duplicate'+totalForms+" .show_onclic").addClass('show_onclic'+totalForms);
                // $('#duplicate'+totalForms+" #show_variable").attr('id','show_variable'+totalForms);
                // $('#duplicate'+totalForms+" #show_numeric").attr('id','show_numeric'+totalForms);
                // $('#duplicate'+totalForms+" #show_textuel").attr('id','show_textuel'+totalForms);
                // $('#duplicate'+totalForms+" #show_image").attr('id','show_image'+totalForms);
                // $('#id_images-TOTAL').attr('id','id_images-TOTAL'+totalForms);
                // $('#id_images-TOTAL'+totalForms).val(totalForms);

                total_form.val(totalForms+1);

            });


        $(document).on('click', '.remove_more_question', function () {
            var total_form = $('#id_variableqs-TOTAL_FORMS') ;
            var totalForms = parseInt(total_form.val())-1  ;

            $('#duplicate_question'+totalForms).remove();
            total_form.val(totalForms)
        });





    });
});