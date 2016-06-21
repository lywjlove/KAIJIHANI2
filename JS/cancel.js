/**
* キャンセル共通モジュール
* 前提条件：Jqueryが必須
* 
* author Red.Scarf  2015/10/19
*/
var cancel = (function ($) {
    var id=Math.floor(Math.random() * 1000);
    var $dialog = $(
	  '<div id="cancel-dialog-module" class="modal fade"  tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true" data-backdrop="static">' +
            '<div class="modal-dialog" style="width: 335px;">' +
                '<div class="modal-content" style="text-align: center;height: 200px;">' +
                    '<div class="panel-body" style="height: 200px; overflow: auto;">' +
                        '<br/>'+
                        '<span style="color: red;font-size: 13px;">データを準備しています、少々お待ちください。</span>'+
                        '<br/>'+
                        '<span style="color: red;font-size: 13px;">抽出時間が10分以上かかる場合は処理を中断します</span>'+
                        '<br/>'+
                        '<label id="timer" style="margin-top:10px;">00:00:00</label>'+
                        '<br/>'+
                        '<button type="button" id="btnCancel'+id+'" class="btn btn-default" style="margin-top: 15px;">キャンセル</button>' +
                    '</div>' +
                 '</div>' +
             '</div>' +
        '</div>'
    );
     var $sm = 0;//记录时钟开始分钟
     var $sc = 0;//记录时钟开始秒
     var $guid = "";
     var $timer = null;//时间显示对象 
     var $hour = 0;
     var $minute = 0; 
     var $second = 0; //时，分 ,钞 
     var $download = 1;
    var $fun = {
	  dialog: function(){
	    return $dialog;
	  },
	  init: function(obj){
         $guid=obj.guid;
	    $dialog.appendTo('body');
	    $("#btnCancel"+id).bind("click",$fun.cancelLoad);
	  },
      myinit: function(){
        $("#timer",window.parent.document).html("00:00:00");
        $hour = $minute = $second = 0; //初始化显示 
        $download=1;
      },
      mystartit: function(){
        $second++; 
        if($second>=60){ //判断秒是否到60, 是则进位 
            $second = 0; 
            $minute++; 
        } 
        if($minute>=60){ //判断分是否到60, 是则进位 
            $minute = 0; 
            $hour++; 
        }
        if($hour>=12){ //判断时是否到12，是则归零
            $hour=0;
        }
        $("#timer",window.parent.document).html($fun.j($hour) + ":" + $fun.j($minute) + ":" + $fun.j($second));
      }, 
      j: function(arg){
        return arg>=10 ? arg : "0" + arg; 
      },
      downFlg : function(){
        return $download;
      },
	  show: function(){
        window.clearInterval($timer);
        $fun.myinit();
        $timer = window.setInterval($fun.mystartit,1000);
        $dialog.modal("show");
	  },
	hide: function(){
        window.clearInterval($timer);
        $dialog.modal("hide");
          },
      cancelLoad : function(){
        $download=0;
        $dialog.modal('hide');
      }
    };
    return $fun;
});
//(jQuery);
