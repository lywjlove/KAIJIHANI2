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
maker_stores $makercd |
hijoin -k1 ${tbld}/TEN_NAME >${tmp}-kaijiten
[ -s ${tmp}-kaijiten ] || echo "0 全店" >${tmp}-kaijiten
cat ${tbld}/BACKUP/${makercd}/${rireki}/MAKER_CATEGORY/$makercd|
hijoin -k1 $tbld/MDL_MAKER             |
kuniq -k1,10                           |
crossjoin - ${tmp}-kaijiten            |
render -lBUNSEIKILISTS $htmlpath/bunseiki.html -   |
cat - <(echo "###")                                   >${tmp}-category
cat ${tbld}/BACKUP/${makercd}/${rireki}/MDL_MAKER_TENPO_CATEGORY_UNYO |
  selcol -c1 -c4,5                          |
  kuniq -k1,3                               |
  hejoin -a -k1,3 - <(cat ${tbld}/BACKUP/${makercd}/${rireki}/MAKER_FINELINE/${makercd} |
  selcol -c1,2 -c4 -c3 -c5|kuniq -k1,5)>${tmp}-ten 2>${tmp}-all
  cat ${tmp}-all                            |
  hijoin -k1 ${tbld}/MDL_MAKER              |
  selcol -c1 -c2 -c3 -c5 -c4 -c6            |
  awk '{print $0,"0","全店"}'               |
  cat - <(cat ${tmp}-ten |
  hijoin -k1,3 - <(selcol -c1 -c3,4 -c2 ${tbld}/BACKUP/${makercd}/${rireki}/MAKER_TENPO_CATEGORY/${makercd})|
  selcol -c1,3 -c6 -c4,5   |
  hijoin -k1 ${tbld}/MDL_MAKER              |
  selcol -c1,2 -c3 -c6 -c4 -c7 -c5|
  hijoin -k7 ${tbld}/TEN_NAME)     |
  ssort -k1,6                     |
  render -lCATEGORYLISTS $htmlpath/category.html - |
  cat ${tmp}-category -
# 終了時刻の記録
echo "$(basename $0) END $(date +%Y%m%d%H%M%S)" >> ${logd}/UPCNT
touch ${semd}/$(basename $0).END.${today}

#終了
#rm -f $tmp-*
exit 0
