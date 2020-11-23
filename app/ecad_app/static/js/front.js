// $(function() {
//   $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
//     history.pushState({}, '', e.target.hash);
//   });
  
//   var hash = document.location.hash;
//   var prefix = "tab_";
//   if (hash) {
//     $('.list-group a[href="'+hash.replace(prefix,"")+'"]').tab('show');
//   }
// });

var ctct_widget, cmnt_widget;
var CaptchaCallback = function() {
  var sk = "6Le6M-UZAAAAAG77ynVY-OfrPRWMogcORDPQySLy";
  ctct_widget = grecaptcha.render('recaptcha_ctct', {'sitekey' : sk});
  cmnt_widget = grecaptcha.render('recaptcha_cmnt', {'sitekey' : sk});
};


function restart_ctct_btns(isSent){
  $('#contact_frm_sending').css({'display': 'none'}).fadeOut(800);
  $('#ctct_form_send').blur();
  $('#ctct_form_send').css({'display': 'block'}).fadeIn(800);
  if(isSent == true){ $('#ctct_form_success').fadeIn(1000).css({'display': 'block'}).delay(2500).fadeOut(1000); }
  else { $('#ctct_form_error').fadeIn(1000).css({'display': 'block'}).delay(2500).fadeOut(1000); }  
}


$(document).on('submit', '#contact_frm',function(e){
  $('#ctct_form_send').css({'display': 'none'}).fadeOut(800);
  $('#contact_frm_sending').css({'display': 'block'}).fadeIn(800);
  e.preventDefault();
  $.ajax({
    type:'POST',
    url:'/contact',
    dataType: 'json',
    data:{
      name:$('#contact_fullName').val(),
      email:$('#contact_email').val(),
      subject:$('#contact_subject').val(),
      msg:$('#contact_message').val(),
      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
      action: 'sendCtct_Form',
      grecaptcha_response:grecaptcha.getResponse(ctct_widget)
    },
    success:function(json){
      if(json.success){
        document.getElementById("contact_frm").reset();
        restart_ctct_btns(true);
        console.log('# --- JS: Captcha OK --- #')
        grecaptcha.reset(ctct_widget);
      }
      else if(json.err_code === 'invalid_captcha'){
        $('#ctct_form_errorCaptcha').fadeIn(1000).css({'display': 'block'}).delay(2500).fadeOut(1000);
        restart_ctct_btns(false);
        console.log('# --- JS: failed captcha --- #')
      }
    },
    error : function(xhr,errmsg,err) {
      restart_ctct_btns(false);
      console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
    
    });
});





$('#vote_fav').on('click', function(){reaction(1)});
$('#vote_util').on('click', function(){reaction(2)});
$('#vote_tmbup').on('click', function(){reaction(3)});
$('#vote_tmbdn').on('click', function(){reaction(4)});
var vote;
function reaction(val){
  icon = $('#new_reaction_success_icon');
  switch (val) {
    case 1: vote = 'fav'; icon.text('grade'); break;
    case 2: vote = 'util'; icon.text('done'); break;
    case 3: vote = 'thumbs_up'; icon.text('thumb_up'); break;
    case 4: vote = 'thumbs_down'; icon.text('thumb_down'); break;
    default: vote = 'vote_null'; break;
  }
}

$('#addReaction').submit(function(e){
  e.preventDefault();
  form = $('#addReaction');
  $.ajax({
    type: form.attr('method'),
    dataType: 'json',
    data: {
      reaction: vote,
      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
      action: 'reaction_Form',
    },
    success: function(json){
      if(json.success){
        $('#reactions').css({'display': 'none'}).fadeOut(4000);
        $('#new_reaction_success').fadeIn(1000).css({'display': 'block'}).delay(2500).fadeOut(1000);        
        setTimeout(function(){ $('#reactions_holder').remove();}, 4500);cl
      }
    else{ alert('error al agregar voto') }
  }

});});




$('#new_comment').submit(function(e){
  e.preventDefault();
  console.log('JS: llego aki')
  $.ajax({
    type: 'POST',
    dataType: 'json',
    data:{
      author: $('#comment_fullName').val(),
      author_email: $('#comment_email').val(),
      comment_body: $('#comment_body').val(),
      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
      action: 'newCmt_Form',
      grecaptcha_response:grecaptcha.getResponse(cmnt_widget)
    },
    success:function(json){
      if(json.success){
        document.getElementById("new_comment").reset();
        $('html, body').animate({scrollTop: $("#new_cmt_btn").offset().top - (160)}, 1500);
        $('#newCmt').collapse('toggle');
        $('#new_cmt_success').fadeIn(1000).css({'display': 'block'}).delay(2500).fadeOut(1000);
        console.log('# --- JS: Comment Captcha OK --- #')
        grecaptcha.reset(cmnt_widget);
      }
      else if(json.err_code === 'invalid_captcha'){
        $('#new_cmt_errorCaptcha').fadeIn(1000).css({'display': 'block'}).delay(2500).fadeOut(1000);
        console.log('# --- JS: Comment failed captcha --- #');
      }
    },
    error : function(xhr,errmsg,err) {
      console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
    
    });
});





function restart_subcribe_btns(isSent){
  $('#subscribe_sending').css({'display': 'none'}).fadeOut(800);
  $('#subscribe_send').css({'display': 'inline'}).fadeIn(800);
  $('#subscribe_send').blur();
  if(isSent == true){ $('#subscribe_success').fadeIn(1000).css({'display': 'block'}).delay(2500).fadeOut(1000); }
  else { $('#subscribe_error').fadeIn(1000).css({'display': 'block'}).delay(2500).fadeOut(1000); }  
}


$(document).on('submit', '#subscribe_frm',function(e){
  $('#subscribe_send').css({'display': 'none'}).fadeOut(800);
  $('#subscribe_sending').css({'display': 'inline-block'}).fadeIn(800);
  urll = window.location.origin + '/subscribe';
  e.preventDefault();
  $.ajax({
    type: 'POST',
    url: '/subscribe',
    dataType: 'json',
    data:{
      s_email: $('#sub_email').val(),
      csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
      action: 'subscribe_Form',
    },
    success:function(json){
      if(json.success){
        document.getElementById("subscribe_frm").reset();
        restart_subcribe_btns(true);
        console.log('# --- JS: OK --- #')
      }
      else{
        if(json.already_exists == true){
          $('#subscribe_already_error').fadeIn(1000).css({'display': 'block'}).delay(2500).fadeOut(1000);
          $('#subscribe_sending').css({'display': 'none'}).fadeOut(800);
          $('#subscribe_send').css({'display': 'inline'}).fadeIn(800);
        } else{ restart_subcribe_btns(); }
        console.log('# --- JS: Failed try of subscription --- #')
      }
    },
    error : function(xhr,errmsg,err) {
      console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }  
    });
});