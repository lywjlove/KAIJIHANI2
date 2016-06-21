#!/bin/bash -xv
#
#RIREKI.SEARCH.CGI  >>修正履歴一覧作成
#Usage:RIREKI.SEARCH.CGI <makercd>
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
#makercd=000006237
if [ -d ${tbld}/BACKUP/${makercd} ];then
  rirekikensu=$(ls ${tbld}/BACKUP/${makercd}|tov|rowc)
  cd ${tbld}/BACKUP/${makercd}/
  ls              |
  tov                                         |
  tac             |
  render -lOPTIONLIST $htmlpath/history.html - |
  cat - <(echo "###"${rirekikensu})
else
 echo "<option value=\"\"></option>###0"
fi
# 終了時刻の記録
echo "$(basename $0) END $(date +%Y%m%d%H%M%S)" >> ${logd}/UPCNT
touch ${semd}/$(basename $0).END.${today}

#終了
rm -f $tmp-*
exit 0
