#!/bin/bash -xv
#
#LOG_HISTORY.CGI  >>>アクセスログ
#Usage:LOG_HISTORY.CGI 
#
#Written by wangjun date:2010/12/29
#echo "Content-type:text/html;charset=UTF-8"
#echo ""

#変数定義
#homeディレクトリの定義
home=/home/trial
#マスタデータ
mstdata=${home}/APDATA/YAKAN_KANSI/POMPA
htmlpath=${home}/public_html/YAKAN_KANSI/HTML
#一時ファイル名の定義
tmp=/tmp/$$
#ログディレクトリの定義
logd=$home/public_html/YAKAN_KANSI/LOG
#SEMAPHORE(起動終了記録）ディレクトリの定義
semd=$home/SEMAPHORE
#処理日付の取得
today=$(date +%Y%m%d)  
sdate=$(date +%Y%m%d).$(date +%H%M%S).$$  
# 走行ログの記録
echo   "${logd}/LOG.$(basename $0).$(date +%Y%m%d)_$(date +%H%M%S)_$$" &> /dev/null
exec 2> ${logd}/LOG.$(basename $0).$(date +%Y%m%d)_$(date +%H%M%S)_$$
# パスの定義
export PATH=/home/SMART:/home/SMART_TRIAL:/home/UTL:/home/TOOL:/usr/local/bin:${PATH}
export LANG=ja_JP.UTF-8

#POSTによるWEBサーバーからのデータを受け渡し
#dd bs=$CONTENT_LENGTH |\
echo ${QUERY_STRING} |
qsstr >$tmp-parameter
#帳票名取るallはすべて
# 終了時刻の記録
sessionid=$(readvalue -usessionid ${tmp}-parameter)
usercd=$(readvalue -uusercd ${tmp}-parameter)

echo "$usercd $sessionid" >>/home/trial/WKSHL/SESSIONTABLE

echo "Set-Cookie: sessionid=$sessionid"
echo "Set-Cookie: usercd=$usercd"
echo "Content-type:text/html;charset=UTF-8"
echo "Location:LOG_HISTORY.CGI"
echo ""

#終了
rm -f $tmp-*
exit 0
