#!/bin/bash -xv
#
#LOG_KANSI_REPORT_SHOW.CGI  >>ログレポート抽出
#Usage:LOG_KANSI_REPORT_SHOW.CGI <sday> 
#
#Written by wangjun date:2015/10/22
#echo "Content-type:text/html;charset=UTF-8"
#echo ""

#変数定義
#homeディレクトリの定義
home=/home/trial
#マスタデータ
htmlpath=${home}/public_html/MDLINK/YAKAN_KANSI/HTML
#一時ファイル名の定義
tmp=/tmp/$$
#ログディレクトリの定義
logd=$home/public_html/MDLINK/YAKAN_KANSI/LOG
#SEMAPHORE(起動終了記録）ディレクトリの定義
semd=$home/SEMAPHORE
#レポートパス
rptd=${home}/public_html/MDLINK/YAKAN_KANSI/REPORT
#処理日付の取得
today=$(date +%Y%m%d)  
sdate=$(date +%Y%m%d).$(date +%H%M%S).$$  
shld=/home/trial/AP/MDLINK/SHELL
# 走行ログの記録
echo   "${logd}/LOG.$(basename $0).$(date +%Y%m%d)_$(date +%H%M%S)_$$" &> /dev/null
exec 2> ${logd}/LOG.$(basename $0).$(date +%Y%m%d)_$(date +%H%M%S)_$$
# パスの定義
export PATH=/home/SMART:/home/SMART_TRIAL:/home/UTL:/home/TOOL:/usr/local/bin:${PATH}
export LANG=ja_JP.UTF-8
echo "Content-type:text/html;charset=UTF-8"
# 起動時刻の記録
echo "$(basename $0) START $(date +%Y%m%d%H%M%S)" >> ${logd}/UPCNT
touch ${semd}/$(basename $0).START.${today}

#POSTによるWEBサーバーからのデータを受け渡し
dd bs=$CONTENT_LENGTH |\
qsstr >$tmp-name

#Cookieから取る
echo ${HTTP_COOKIE}                             |
sed 's/ //g' | sed 's/;/\&/g' | qsstr           > ${tmp}-cookie
#帳票名取るallはすべて
sday=$(grep sday $tmp-name|selcol -c2)
#sday=2015-10-26
#sessionid=$(readvalue -usessionid ${tmp}-cookie)
#usercd=$(readvalue -uusercd ${tmp}-cookie)
#cnt=$(cat /home/trial/WKSHL/SESSIONTABLE        |
#awk '$1=="'${usercd}'"'                         |
#awk '$2=="'${sessionid}'"'                      |
#tail -n1                                        |
#rowc                                            #)
#if [ $cnt -ne 1 ]; then
#    echo "Location:http://10.2.7.235/~trial/LOGIN/APP/CGI/LOGIN.CGI"
#    echo ""
#else
#    echo ""
#fi
echo ""
if [ -z $sday ];then
 sday=$(date +%Y-%m-%d)
 time=$(ls -l $rptd/$sday|awk '{print $6$7"日_"$8}')
 cat ${rptd}/$sday                       |
 render -lTRLISTS $htmlpath/MAIN.html -   |
 render -lDATE - <(echo "${sday}")        |
 render -lTIME - <(echo "${time}")
else
 $shld/MDLINK.YAKAN_KANSI_MAIN
 time=$(ls -l $rptd/$sday|awk '{print $6$7"日_"$8}')
 cat ${rptd}/$sday                        |
 render -lTRLISTS $htmlpath/REPORT.HTML - |
 cat - <(echo "###<lable>実行時刻:"$(echo ${time}|sed 's/_/ /g')"</lable>")
fi
exit 0


# 終了時刻の記録
echo "$(basename $0) END $(date +%Y%m%d%H%M%S)" >> ${logd}/UPCNT
touch ${semd}/$(basename $0).END.${today}

#終了
rm -f $tmp-*
exit 0
