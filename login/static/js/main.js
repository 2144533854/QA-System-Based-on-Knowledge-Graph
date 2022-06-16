// 将问题发送到后台，并接收相应
function sendtoserver(text)
{
  var xmlhttp;
  if (window.XMLHttpRequest)
  {
    // IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
    xmlhttp=new XMLHttpRequest();
  }
  else
  {
    // IE6, IE5 浏览器执行代码
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
  xmlhttp.onreadystatechange=function()
  {
    if (xmlhttp.readyState==4 && xmlhttp.status==200)
    {

      var answer=xmlhttp.responseText;
      show($.trim(answer));
    }
  }
      //XMLHTTP.readyState的五种状态/4：响应已完成，可以获取并使用服务器的响应。
      //  相应完成，则显示出来
      // document.getElementById("myDiv").innerHTML=xmlhttp.responseText;
  xmlhttp.open("POST","/add/",true);//true为异步处理
  xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
  xmlhttp.send("question="+$.trim(text));
}

$('#info').keyup(function(e) {
    var key = e.which;
    if ($('#info').val() == '') {
        $('#send').css({
            'background-image': 'url(/static/img/btn32.png)'
        });
    } else {
        $('#send').css({
            'background-image': 'url(/static/img/btn3.gif)'
        });
    }
    if (key == 13) {
        $('#send').trigger("click");
        $('#send').css({
            'background-image': 'url(/static/img/btn3.png)'
        });
    }
});
var pre_time;
$('#send').click(function() {
    // 获取当前日期，并添加到对话框中
    var d = new Date();
    if (!pre_time || (pre_time && diff_time(d))) {
        var p = "<div><span>" + d.getHours() + ':' + (d.getMinutes().toString().length == 1?'0'+d.getMinutes():d.getMinutes()) + '</span></div>';
        pre_time = d;
        $('#chat').append(p);
    }
    // 获取当前问题信息
    var text = $('#info').val();
    // 判断问题是否为空
    if ($.trim(text)=="")
    {
        $('#send').css(setDisabled);
    }
    else {
        // 清空发送框
        $('#info').val('');
        $('#send').css({
            'background-image': 'url(/static/img/btn3.png)'
        });
        // 把发送内容添加到聊天框
        var p = "<div class='me'><div class='qipao'></div><div class='item'>" + text + '</div></div>';
        $('#chat').append(p);
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
        // 将问题信息发送到服务
        sendtoserver(text);
    }

})

function show(data) {
    var p = "<div class='robot'><div class='qipao'></div><div class='item'>" + data + '</div></div>';
    $('#chat').append(p);
    $('#chat').scrollTop($('#chat')[0].scrollHeight);
}

// 处理时间的函数
function diff_time(time) {
    if (time.getHours() - pre_time.getHours() == 0) {
        if (time.getMinutes() - pre_time.getMinutes() <= 5)
            return false;
    } else
        return true;
}

