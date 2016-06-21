#!/bin/bash -xv
#
# TEN.CGI >>SEARCH_EXCEL_MASTER.CGI

# Written by 10015130    2015/07/06

#環境変数設定
export PATH=/home/SMART_TRIAL:/home/SMART:/usr/local/bin:${PATH}
export LANG=ja_JP.UTF-8

#ログディレクトリ定義
logd=/home/trial/AP/CATEGORY_MONTH_EVAL/LOG

# 走行ログの記録
echo   "${logd}/LOG.$(basename $0).$(date +%Y%m%d)_$(date +%H%M%S)_$$" &> /dev/null
exec 2> ${logd}/LOG.$(basename $0).$(date +%Y%m%d)_$(date +%H%M%S)_$$

#変数定義
mdltbld=/MDLINK/TBL
dir=/home/trial/AP/CATEGORY_MONTH_EVAL
cgid=${dir}/APP/CGI
shell=$dir/APP/SHELL
tpld=$dir/TEMPLATE
tmp=/tmp/$$-$(basename $0).$(date +%Y%m%d%H%M%S)
pompd=/home/trial/APDATA/CATEGORY_MONTH_EVAL/POMPA
shld=$(dirname $0)
download=/home/trial/AP/CATEGORY_EVAL/APP/HTML/download

# 共通処理、SOAPメッセージ解析
echo ${QUERY_STRING}    |
qsstr -l_ -i_           > $tmp-param

#システムログ
#10051179   zhao   20150923
startTime=$(date +%Y/%m/%d_%H:%M)
doStar=$(date +%Y-%m-%d@%H:%M:%S)

# エラー時のセマフォ処理定義
ERROR_TOUCH(){
    exit 1
} 

#エラー処理
ERROR_EXIT() {
    exit 0
}

echo ${QUERY_STRING} | qsstr -i_ -l_ > ${tmp}-paralist

zipfile=$(readvalue -u param ${tmp}-paralist)

#ヘッダ出力
echo "Accept-Ranges: bytes"
echo "Content-type:application/octet-stream;"
echo "Content-Disposition: attachment; filename=${zipfile}";
echo "Content-Length: $(wc -c ${download}/${zipfile} | awk '{print $1}')" 
echo ""

cat ${download}/${zipfile}

#終了ログ
echo "${HOSTNAME} $(basename $0) END   $(date +%Y%m%d%H%M%S)" >> ${logd}/UPCNT

#一時ファイル
rm -rf $tmp-*
exit 0
