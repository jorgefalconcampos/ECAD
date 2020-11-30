$(window).on('load',function(){
    $('#noCategoModal').modal('show');
    $('[data-toggle="tooltip"]').tooltip(); 
    // alert(window.location.origin); //http://localhost:9000

    $('[id^="cmt_counter"]').each(function() {
        var post_id = $(this).attr('id').replace(/[^\d]+/, ''); //getting only the numeric part
        post_details[post_id] = parseInt($(this).html());  //adding to a JSON object the post_id with the number of comments inside that post
    });

    var active = sessionStorage.getItem('active');

    switch (active) {
        case "sel_item_nav_settings":
            $("#settings_account").click();
        break;
        case "sel_item_nav_password":
            $("#settings_password").click();
        break;   
        default: $("#settings_profile").click(); break;
      }
});


$("#settings_account").on('click', function(){
    sessionStorage.setItem('active', "sel_item_nav_settings");
});

$("#settings_password").on('click', function(){
    sessionStorage.setItem('active', "sel_item_nav_password");
});

$("#settings_profile").on('click', function(){
    sessionStorage.setItem('active', "sel_item_nav_profile");
});

var post_details = {}

// START TOAST MESSAGES SECTION //
var success_title = 'Cambios guardados con éxito', success_text = 'Los cambios fueron guardados. ', success_reloading = ' Recargando...';

function success(title, text, param, rowID, modal_ID){
    if($("#toastForm").hasClass("border-danger")){$("#toastForm").removeClass('border-danger'); $("#toastForm").addClass('border-success'); }
    if($("#msg_header").hasClass("bg-danger")){$("#msg_header").removeClass('bg-danger'); $("#msg_header").addClass('bg-success'); }
    $("#toastForm").addClass('border-success'); 
    $("#msg_header").addClass('bg-success'); 
    $("#msg_icon").attr('class', 'fas fa-check mr-1'); 
    $("#msg_title").text(title); 
    $("#msg_txt").text(text); 
    $("#toastForm").toast('show');

    // 0: updates personal info in settings, reloads the page
    // 1: deletes a post inside the post detail, then redirect to dashboard
    // 2: deletes a post inside the dashboard/all posts page, keeps in url but removes the element
    // 3: archives a post and ... (?)
    switch (param) {
        case 0: window.setTimeout( function() { $('#postActionsModal').modal('hide'); window.location.reload(true); }, 750);  break;
        case 1: 
            if (sender === 'detail'){
                window.setTimeout( function() { window.location.href = '/user/dashboard'; }, 750); 
            }
            else {
                $(modal_ID).modal('hide');
                $(`#${rowID}`).delay(500).fadeOut(1000, function(){$(this).remove();}); //removing the whole table row element

                // below code only applies when we're moderating comments
                var general_cmts = parseInt($('#general_cmt_counter').html());
                general_cmts -= 1;
                $(`#general_cmt_counter`).text(general_cmts).delay(500).fadeIn(700);

                post_details[postcmtID] = post_details[postcmtID]-1;
                $(`#cmt_counter_${postcmtID}`).text(post_details[postcmtID]).delay(500).fadeIn(700);

                if (post_details[postcmtID] < 1){ 
                    $(`#accordion_${postcmtID}`).delay(500).fadeOut(1000, function(){$(this).remove();}); //removing the whole accordion element
                }

                if (general_cmts < 1){ setTimeout(function() { alert('No hay más comentarios para moderar'); window.location.reload(true);} , 3750); }
                    
                console.log('update: '+JSON.stringify(post_details));
                console.log('update: '+general_cmts);
            }
            break;
      
        default:  break;
      }
}


function error(title, text){
    $("#toastForm").addClass('border-danger'); 
    $("#msg_header").addClass('bg-danger'); 
    $("#msg_icon").attr('class', 'fas fa-exclamation-circle mr-1');
    $("#msg_title").text(title); 
    $("#msg_txt").text(text); 
    $("#toastForm").toast('show');
}
// END TOAST MESSAGES SECTION //





// This function works with Profile settings form
var sthInput = false;
function img_profile_filename(elemID){
    if (elemID === 'profile_image'){
        var path = document.getElementById('profile_image').value;//take path
        var tokens = path.split('\\');//split path
        var filename = tokens[tokens.length-1]
        var output = filename.substr(0, filename.lastIndexOf('.')) || filename;
        return(output);
    }
    else{ if(sthInput == true) { var output = elemID.substr(0, elemID.lastIndexOf('.')) || elemID; 
        } else{ return false;}
    }   
}

//Profile settings form
$(window).on('load',function(){

    //Default values (marked with the prefix 'd'.) They're displayed directly from db
    var d_fname = $('#profile_firstName').val(), 
        d_lname = $('#profile_lastName').val(), 
        d_title = $('#profile_title').val(), 
        d_bio = $('#profile_bio').val(), 
        d_img = img_profile_filename($('#profile_author_img').text()), 
        d_pemail = $('#profile_email').val(), 
        d_fb = $('#profile_facebook').val(), 
        d_tw = $('#profile_twitter').val(),
        d_li = $('#proprofile_linkedin').val();     

     //If user leaves the section, get default values again and fill inputs
     $("#settings_profile").click(function(){
        $("#profile_firstName").val(d_fname); 
        $("#profile_lastName").val(d_lname); 
        $("#profile_title").val(d_title); 
        $("#profile_bio").val(d_bio); 
        $("#profile_email").val(d_pemail); 
        $("#profile_facebook").val(d_fb); 
        $("#profile_twitter").val(d_tw); 
        $("#proprofile_linkedin").val(d_li); 
    });


    $("#profile_image").change(function () {
        var validExtensions = ["jpg","jpeg","png"]
        var file = $(this).val().split('.').pop().toLowerCase();

        if (validExtensions.indexOf(file) == -1) { 
            error('Formato incorrecto', 'Solo se aceptan formatos de imagen.\nRecomendamos usar '+ validExtensions.join(', ')+'.');
            $(this).filestyle('clear'); sthInput = false; 
        } else{  if (this.files[0].size > 2097152) {
            size = (this.files[0].size/Math.pow(1024,2)).toFixed(2).slice('0, -1');
            error('Imagen demasiado grande', `La imagen seleccionada tiene un tamaño aproximado de ${size} MB, y excede el límite de tamaño permitido (2 MB).`);
            $(this).filestyle('clear'); sthInput = false; } else{ sthInput = true; }        
        }
    });

    
    $(document).on('submit', '#profile_frm',function(e){
        var data = new FormData($('#profile_frm').get(0));
        data.append('action', 'profile_Form');
        e.preventDefault();
        //New values introduced by user. If they're different than the default, then they've been changed, so we update them to db
        var n_fname = $('#profile_firstName').val();
        var n_lname = $('#profile_lastName').val();
        var n_title = $('#profile_title').val();
        var n_bio = $('#profile_bio').val();
        var n_img = img_profile_filename('profile_image');
        var n_pemail = $('#profile_email').val();
        var n_fb = $('#profile_facebook').val();
        var n_tw = $('#profile_twitter').val();
        var n_li = $('#proprofile_linkedin').val();

        if ((n_fname != d_fname)||(n_lname != d_lname)||(sthInput != false)||((n_img!="")&&(n_img!=d_img))||(n_title != d_title)||(n_bio != d_bio)||(n_pemail != d_pemail)||(n_fb != d_fb)||(n_tw != d_tw)||(n_li != d_li)){
            $.ajax({
                type: 'POST',
                dataType: 'json',
                url: window.location.pathname,
                data: data,
                contentType: false,
                processData: false,
                success:function(json){
                    if(json.success){success(success_title, success_text+=success_reloading, 0);}
                    else { 
                        if (json.errors == ''){error('Error en email', 'Ocurrió un error al intentar asignar el email')}
                        else{ for(var key in json.errors){error('Error en '+key, json.errors[key][0])}}
                    }
                },
            });
        }
        else {  error('Error en los datos', 'No se detectaron cambios'); }
    });
});





//Account settings form 
$(window).on('load',function(){

    //Default values (marked with the prefix 'd'.) They're displayed directly from db
    var d_usr = $('#acc_username').val(); 
    var d_email = $('#acc_email').val();
    var hasChanged = false;
    //If user leaves the section, get default values again and fill inputs
    $("#settings_account").click(function(){
        $("#acc_username").val(d_usr); 
        $("#acc_email").val(d_email); 
    });
    
    $(document).on('submit', '#account_frm',function(e){
        e.preventDefault();
        //New values introduced by user. If they're different than the default, then they've been changed, so we update them to db
        var n_user = $('#acc_username').val();
        var n_email = $('#acc_email').val();
        if ((n_user != d_usr)||(n_email != d_email)){ 
            hasChanged = true;
            $.ajax({
                type: 'POST',
                dataType: 'json',
                url: window.location.pathname,
                data:{
                    username: $('#acc_username').val(),
                    email: $('#acc_email').val(),
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                    action: 'account_Form',
                },
                success:function(json){
                    if(json.success){success(success_title, success_text+=success_reloading, 0);}
                    else { 
                        if (json.errors == 'email_already_taken'){error('Error en email', 'Ocurrió un error al intentar asignar el email')}
                        else{ for(var key in json.errors){error('Error en '+key, json.errors[key][0])}}
                    }
                },
            });
        }
        else { error('Error en los datos', 'No se detectaron cambios');}
    });
});





// New category form
$(document).on('submit', '#newCatego_frm',function(e){
    var data = new FormData($('#newCatego_frm').get(0));
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: window.location.pathname,
        dataType: 'json',
        data: data,
        contentType: false,
        processData: false,
        success: function(json){
            if(json.success){     
                document.getElementById("newCatego_frm").reset();
                $('#newCatego_form_success').fadeIn(700).css({'display': 'block'}).delay(2000).fadeOut(700);
            }
            else if (json.err_code == 'already_exists'){
                $('#newCatego_form_error').append('<span id="txt">: ya existe esa categoría</span>');
                $('#newCatego_form_error').fadeIn(700).css({'display': 'block'}).delay(2000).fadeOut(700);
            }
            else { alert(json.err_code); }
        },
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
    return false;
});





// START MODERATE COMMENTS SECTION //
var cmtID, postcmtID, cmt_author, cmt_body, comment_action;

$('[id^="approveCommentBtn_in_moderate"]').click(function() {
    postcmtID = $(this).data('postcmtid');
    cmtID = $(this).data('cmtid');
    cmt_author = $(this).data('cmtauthor');
    cmt_body = $(this).data('cmtbody');
    iconName = 'check';
    cmts_action_config(1)
 });

$('[id^="rejectCommentBtn_in_moderate"]').click(function() {
    postcmtID = $(this).data('postcmtid');
    cmtID = $(this).data('cmtid');
    cmt_author = $(this).data('cmtauthor');
    cmt_body = $(this).data('cmtbody');
    iconName = 'delete';
    cmts_action_config(2)
 });

function cmts_action_config(val){
    frm = $('#comment_action_frm');
    icon = `<i class="material-icons align-top">${iconName}</i>`;
    button = $('#modal_comment_action_confirm')
    label = $('#cmt_action_label');   
     
    switch (val) { // 1: approve, 2: delete,
        case 1: 
            comment_action = 'approve'; 
            frm.attr('method', 'POST');
            label.html(`¿Aprobar el comentario de <b>${cmt_author}</b>?<br><br><b>"</b>${cmt_body}</div><b>"</b>`)
            button.attr('class', 'btn btn-success px-3'); button.html(`${icon} Si, aprobar`);
        break;

        case 2: 
            comment_action = 'delete'; 
            frm.attr('method', 'DELETE');
            label.html(`¿Eliminar el comentario de <b>${cmt_author}</b>? <br><br><b>"</b>${cmt_body}<b>"</b>`)
            button.attr('class', 'btn btn-danger px-3'); button.html(`${icon} Si, eliminar`);
        break;

        default: break;
      }
}

$(document).on('submit ', '#commentActionsModal',function(e){
    var param; // Param is sent to success function. 0 reloads the page, 1 deletes the row 
    switch (comment_action) {
        case 'approve':  param = 1; success_text = 'El comentario fue aprobado.'; break;
        case 'delete': param = 1;  success_text = 'El comentario fue eliminado.'; break;
        default: break;        
    }
    e.preventDefault();
    $.ajax({
        url: `/usuario/comment/perform-action/${comment_action}/${cmtID}`,
        type: $(this).attr('method'),
        dataType: 'json',
        beforeSend: function (xhr) { xhr.setRequestHeader("X-CSRFToken", csrftoken);},
        success:function(json){
          if(json.success){success(success_title, success_text, param, cmtID, $('#commentActionsModal'));
        }
        },
        error : function(xhr,errmsg,err) {
          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
        });

});
// END COMMENTS SECTION //





// START MANAGE/MODERATE POSTS SECTION //
$('#deleteBtn_in_post_edit, #deleteBtn_in_post_list, #deleteBtn_in_dshbrd').on('click', function(){ 
    postID = $(this).data('postid'); posttitle = $(this).data('posttitle'); iconName = 'delete'; 
    if ($(this).attr('id') === 'deleteBtn_in_post_edit'){ post_action_config(1,1); }
    else{ post_action_config(1,2); }
});


$('#archiveBtn_in_post_edit, #archiveBtn_in_post_list').on('click', function(){ 
    postID = $(this).data('postid'); posttitle = $(this).data('posttitle'); iconName = 'archive'; 
    if ($(this).attr('id') === 'archiveBtn_in_post_edit'){ post_action_config(2,1); }
    else{ post_action_config(2,2); }
});

$('#unarchiveBtn_in_post_edit, #unarchiveBtn_in_post_list').on('click', function(){ 
    postID = $(this).data('postid'); posttitle = $(this).data('posttitle'); iconName = 'unarchive';
    if ($(this).attr('id') === 'unarchiveBtn_in_post_edit'){ post_action_config(3,1); }
    else{ post_action_config(3,2); }
});


$('[id^="rejectBtn_in_moderate"]').click(function() {
    postID = $(this).data('postid'); posttitle = $(this).data('posttitle');
    iconName = 'close'; post_action_config(4,2)
 });


$('[id^="approveBtn_in_moderate_"]').click(function() {
    postID = $(this).data('postid'); posttitle = $(this).data('posttitle');
    iconName = 'check'; post_action_config(5,2)
 });

var post_action, iconName, url, where_from, postID, posttitle, sender;

var frm = $('#post_action_frm');
var button = $('#modal_post_action_confirm'); 
var label = $('#post_action_label');   

function post_action_config(val, where_f){
    icon = `<i class="material-icons align-top">${iconName}</i>`;
    // where_f means where from, the sender (can be details page or dashboard page)
    switch (where_f) { case 1: sender = 'detail'; break; case 2: sender = 'dashboard'; break; default: sender = null; break; }

    switch (val) { // 1: delete, 2: archive, 3: unarchive, 4: reject
        case 1: 
            post_action = 'delete'; 
            frm.attr('method', 'DELETE');
            label.html(`¿Realmente deseas eliminar el post <b>${posttitle}</b>? <br><br>Esta acción no se puede deshacer.`)
            button.attr('class', 'btn btn-danger px-3'); button.html(`${icon} Si, eliminar`);
        break;

        case 2: 
            post_action = 'archive'; 
            frm.attr('method', 'POST');
            label.html(`¿Realmente deseas archivar el post <b>${posttitle}</b>? `)
            button.attr('class', 'btn btn-warning-light px-3'); button.html(`${icon} Si, archivar`);
        break;

        case 3: 
            post_action = 'unarchive'; 
            frm.attr('method', 'POST');
            label.html(`¿Sacar del archivo el post <b>${posttitle}</b>? `)
            button.attr('class', 'btn btn-warning-light px-3'); button.html(`${icon} Si, desarchivar`);
        break;

        case 4: 
            post_action = 'reject'; 
            frm.attr('method', 'POST');
            label.html(`¿Rechazar el post <b>${posttitle}</b>? `)
            button.attr('class', 'btn btn-danger px-3'); button.html(`${icon} Si, rechazar`);
        break;

        case 5: 
            post_action = 'approve'; 
            frm.attr('method', 'POST');
            label.html(`¿Aprobar el post <b>${posttitle}</b>? `)
            button.attr('class', 'btn btn-success px-3'); button.html(`${icon} Si, aprobar`);
        break;

        case 6: 
            post_action = 'approve_n_send'; 
            frm.attr('method', 'POST');
            label.html(`¿Aprobar y enviar por Newsletter el post <b>${posttitle}</b>? `)
            button.attr('class', 'btn btn-success px-3'); button.html(`${icon} Si, aprobar y enviar`);
        break;
      
        default: break;
      }
}

$(document).on('submit', '#postActionsModal',function(e){
    var param; // Param is sent to success function. 0 reloads the page, 1 deletes the row 
    switch (post_action) {
        case 'delete': 
            param = 1; success_text = 'El post fue eliminado.';
            if (sender === 'detail') { success_text += ' Redireccionando...'; }
        break;

        case 'archive': 
            param = 0;  success_text = 'El post fue archivado.';
            if (sender === 'detail') { success_text += success_reloading }
        break;

        case 'unarchive': 
            param = 0; success_text = 'El post fue desarchivado.';
            if (sender === 'detail') { success_text += success_reloading }
        break;

        case 'reject': param = 1; success_text = 'El post fue rechazado.'; break;

        case 'approve': param = 1; success_text = 'El post fue aprobado.'; break;
        
        case 'approve_n_send': param = 1; 
            success_text = 'El post fue aprobado y enviado a todos los destinatarios inscritos al Newsletter.'; 
            $('#modal_post_action_confirm').css({'display': 'none'}).fadeOut(800);
            $('#send_newsletter_sending').css({'display': 'block'}).fadeIn(800);
            $('#sending_newsletter_loadingProgressBar').css({'display': 'block'}).fadeIn(800);
        break;

        default: break;        
    }

    e.preventDefault();
    $.ajax({
        url: `/usuario/post/perform-action/${post_action}/${postID}`,
        type: $(this).attr('method'),
        dataType: 'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success:function(json){
          if(json.success){
              if(post_action == 'approve_n_send'){
                  $('#send_newsletter_sending').css({'display': 'none'});
                  $('#modal_post_action_confirm').css({'display': 'block'});
                  $('#sending_newsletter_loadingProgressBar').css({'display': 'none'});
                }
                success(success_title, success_text, param, postID, $('#postActionsModal'));
            //   postID = ""; posttitle = ""; iconName = ""; post_action = ""; frm.attr('method', '');
            //   label.html(""); button.attr('class', ''); button.html("");
            }
        },
        error : function(xhr,errmsg,err) {
          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
        });

});
// END MANAGE/MODERATE POSTS SECTION //




// START MANAGE/MODERATE POSTS & SEND NEWSLETTER SECTION //


$('[id^="approveSendNewsletter_Btn_in_moderate_"]').click(function() {
    postID = $(this).data('postid'); posttitle = $(this).data('posttitle');
    iconName = 'check'; post_action_config(6,2);

 });


// END MANAGE/MODERATE POSTS & SEND NEWSLETTER SECTION //









function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});