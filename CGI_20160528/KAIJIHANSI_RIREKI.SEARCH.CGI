#!/bin/bash -xv
#
#KAIJIHANSI_RIREKI.SEARCH.CGI  >>開示範囲履歴表示
#Usage:KAIJIHANSI_RIREKI.SEARCH.CGI 
#
#Written by wangjun date:2015/11/26

#変数定義
#homeディレクトリの定義
home=/home/trial
#マスタデータ
htmlpath=${home}/public_html/MDLINK/KAIJIHANI/HTML
#一時ファイル名の定義
tmp=/tmp/$$
#ログディレクトリの定義
logd=$home/public_html/MDLINK/KAIJIHANI/LOG
#SEMAPHORE(起動終了記録）ディレクトリの定義
semd=$home/SEMAPHORE
tbld=/MDLINK/TBL
#処理日付の取得
today=$(date +%Y%m%d)  
sdate=$(date +%Y%m%d).$(date +%H%M%S).$$  
# 走行ログの記録
echo   "${logd}/LOG.$(basename $0).$(date +%Y%m%d)_$(date +%H%M%S)_$$" &> /dev/null
exec 2> ${logd}/LOG.$(basename $0).$(date +%Y%m%d)_$(date +%H%M%S)_$$
# パスの定義
export PATH=/home/SMART:/home/SMART_TRIAL:/home/UTL:/home/TOOL:/usr/local/bin:${PATH}
export LANG=ja_JP.UTF-8
echo "Content-type:text/html;charset=UTF-8"
echo ""
# 起動時刻の記録
echo "$(basename $0) START $(date +%Y%m%d%H%M%S)" >> ${logd}/UPCNT
touch ${semd}/$(basename $0).START.${today}

#POSTによるWEBサーバーからのデータを受け渡し
dd bs=$CONTENT_LENGTH |\
qsstr >$tmp-name

makercd=$(grep makercd $tmp-name|selcol -c2)
rireki=$(grep rireki $tmp-name|selcol -c2)
#帳票名取るallはすべて
cat ${tbld}/BACKUP/${makercd}/${rireki}/MAKER_CATEGORY/$makercd|
hijoin -k1 $tbld/MDL_MAKER             |
fmtdecimal -c1                         |
render -lBUNSEIKILISTS $htmlpath/bunseiki.html -   |
cat - <(echo "###")                                   >${tmp}-category
tenrowc=$(cat ${tbld}/BACKUP/${makercd}/${rireki}/MDL_MAKER_TENPO_CATEGORY_UNYO |
selrow -e '$1=="'${makercd}'"'|rowc)
if [ $tenrowc -eq 0 ];then
    cat ${tbld}/BACKUP/${makercd}/${rireki}/MAKER_FINELINE/$makercd |
    kuniq -k1,5                |
    hijoin -k1 $tbld/MDL_MAKER |
    awk '{print $0,"0","全店"}'               |
    render -lCATEGORYLISTS $htmlpath/category.html - |
    cat ${tmp}-category -
else
    cat ${tbld}/BACKUP/${makercd}/${rireki}/MAKER_FINELINE/$makercd |
    kuniq -k1,5|hijoin -k1 $tbld/MDL_MAKER |
    crossjoin - <(cat ${tbld}/BACKUP/${makercd}/${rireki}/MAKER_TENPO_CATEGORY/${makercd}|
    kuniq -k2|hijoin -k1 ${tbld}/TEN_NAME)     |
    render -lCATEGORYLISTS $htmlpath/category.html -  |
    cat ${tmp}-category -
fi
# 終了時刻の記録
echo "$(basename $0) END $(date +%Y%m%d%H%M%S)" >> ${logd}/UPCNT
touch ${semd}/$(basename $0).END.${today}

#終了
rm -f $tmp-*
exit 0
