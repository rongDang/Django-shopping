// user
var user_Boolean = false;
var password_Boolean = false;
var varconfirm_Boolean = false;
var emaile_Boolean = false;
var Mobile_Boolean = false;
//blur() 函数触发 blur 事件，
// 或者如果设置了 function 参数，该函数也可规定当发生 blur 事件时执行的代码。
$('.reg_user').blur(function(){
  if ((/^.{3,8}$/).test($(".reg_user").val())){
    $('.user_hint').html("✔").css("color","green");
    user_Boolean = true;
  }else {
    $('.user_hint').html("×").css("color","red");
    user_Boolean = false;
  }
});
// password
$('.reg_password').blur(function(){
  if ((/^[a-z0-9_-]{6,16}$/).test($(".reg_password").val())){
    $('.password_hint').html("✔").css("color","green");
    password_Boolean = true;
  }else {
    $('.password_hint').html("×").css("color","red");
    password_Boolean = false;
  }
});


// password_confirm
$('.reg_confirm').blur(function(){
  //val() 方法返回或设置被选元素的值。元素的值是通过 value 属性设置的。该方法大多用于 input 元素。
  if (($(".reg_password").val())==($(".reg_confirm").val())){
    $('.confirm_hint').html("✔").css("color","green");
    varconfirm_Boolean = true;
  }else {
    $('.confirm_hint').html("×").css("color","red");
    varconfirm_Boolean = false;
  }
});


// Email
$('.reg_email').blur(function(){
  if ((/^[a-z\d]+(\.[a-z\d]+)*@([\da-z](-[\da-z])?)+(\.{1,2}[a-z]+)+$/).test($(".reg_email").val())){
    $('.email_hint').html("✔").css("color","green");
    emaile_Boolean = true;
  }else {
    $('.email_hint').html("×").css("color","red");
    emaile_Boolean = false;
  }
});


// Mobile
$('.reg_mobile').blur(function(){
  if ((/^1[34578]\d{9}$/).test($(".reg_mobile").val())){
    $('.mobile_hint').html("✔").css("color","green");
    Mobile_Boolean = true;
  }else {
    $('.mobile_hint').html("×").css("color","red");
    Mobile_Boolean = false;
  }
});


// click,当点击元素时，会发生 click 事件。在jQuery中如果前面得代码出错则后面得代码不会执行
$('.red_button').click(function(){
  //获取对应输入框的值
  var username = document.getElementById("name").value;
  var password = document.getElementById("pwd").value;
  var mail = document.getElementById("e_mail").value;
  var phone = document.getElementById("phone").value;
  //如果所有条件都满足则注册成功，页面跳转到首页去，（confirm？还有一个判断，判断电话号码和邮箱是否已经被注册）
  if(user_Boolean && password_Boolean && varconfirm_Boolean && emaile_Boolean && Mobile_Boolean){
    //判断注册的电话和邮箱是否存在   (后面再详细判断是电话存在还是邮箱存在,ajax实现)
      alert($('#form1').serialize());
      $.ajax({
          //跳转的链接
          url:"is_sign",
          type:"POST",
          dataType:"json",
          data:$('#form1').serialize(),
          success:function (data) {
              alert(data+'=====');
              alert(data.sex);
              //判断连接返回的值是否存在,有值表示账号存在
              if (data[0]!=null && data[0]!="") {
                  alert("账号或邮箱或用户名存在,重新注册");
                  location.href="sign";
              }else{
                  alert("注册成功！");
                  location.href="index";
              }
          },
          error:function (data) {
              alert(textStatus);
              alert(data.textStatus);
              alert(textStatus);
              alert("未知错误");
          }
      });
  }else {
      alert("请完善信息！");
  }
});

