#!/bin/bash -xv
#
# EXCEL_DOWNLOAD.CGI  Excelダウンロード

# Written by wang_jun 2015/11/28

#環境変数設定
export PATH=/home/SMART_TRIAL:/home/SMART:/usr/local/bin:${PATH}
export LANG=ja_JP.UTF-8

#ログディレクトリ定義
logd=/home/trial/AP/MDLINK/KAIJIHANI/LOG

# 走行ログの記録
echo   "${logd}/LOG.$(basename $0).$(date +%Y%m%d)_$(date +%H%M%S)_$$" &> /dev/null
exec 2> ${logd}/LOG.$(basename $0).$(date +%Y%m%d)_$(date +%H%M%S)_$$

#変数定義
tbld=/MDLINK/TBL
tmp=/tmp/$$-$(basename $0).$(date +%Y%m%d%H%M%S)
download=/home/trial/AP/MDLINK/KAIJIHANI/DownLoad
exceld=/home/trial/AP/MDLINK/KAIJIHANI/EXCEL
# 共通処理、SOAPメッセージ解析
echo ${QUERY_STRING}    |
qsstr -l_ -i_           > $tmp-param


#エラー処理
ERROR_EXIT() {
    exit 0
}

echo ${QUERY_STRING} | qsstr -i_ -l_ > ${tmp}-paralist

makercd=$(readvalue -u makercd ${tmp}-paralist)
ckflg=$(readvalue -u ckflg ${tmp}-paralist)
if [ $ckflg != "all" ];then
  cat ${tbld}/MAKER_CATEGORY/$makercd    |
  hijoin -k1 $tbld/MDL_MAKER             |
  wExcel -t ${exceld}/kaijihani.xls -s1 -n分析系 -x2 -yA -o ${tmp}-sheet1.xls
  
  tenrowc=$(cat ${tbld}/MDL_MAKER_TENPO_CATEGORY_UNYO |
  selrow -e '$1=="'${makercd}'"'|rowc)
  if [ $tenrowc -eq 0 ];then
     cat $tbld/MAKER_FINELINE/$makercd      |
     selcol -c1,5                           |
     kuniq -k1,5                            |
     hijoin -k1 $tbld/MDL_MAKER             |
     awk '{print $0,"0","全店"}'            |
     wExcel -t ${tmp}-sheet1.xls -s2 -nカテマネ系 -x2 -yA -o ${download}/result_$$.xls
  else
    cat $tbld/MAKER_FINELINE/$makercd |
    selcol -c1,5|kuniq -k1,5|hijoin -k1 $tbld/MDL_MAKER |
    crossjoin - <(cat ${tbld}/MAKER_TENPO_CATEGORY/${makercd}|
    kuniq -k2|hijoin -k1 ${tbld}/TEN_NAME)     |
    wExcel -t ${tmp}-sheet1.xls -s2 -nカテマネ系 -x2 -yA -o ${download}/result_$$.xls
  fi
else
  ls ${tbld}/MAKER_CATEGORY/*            |
  grep -v 99999999                       |
  xargs cat                              |
  hijoin -k1 $tbld/MDL_MAKER             |
  wExcel -t ${exceld}/kaijihani.xls -s1 -n分析系 -x2 -yA -o ${tmp}-sheet1.xls
  
  ls $tbld/MAKER_FINELINE/*              |
  grep -v 99999999                       |
  xargs cat                              |
  selcol -c1,5                           |
  kuniq -k1,5                            |
  hijoin -k1 $tbld/MDL_MAKER            >${tmp}-all-category
  cat ${tmp}-all-category                |
  hejoin -a -k1 <(cat /MDLINK/TBL/MDL_MAKER_TENPO_CATEGORY_UNYO |kuniq -k1) >${tmp}-ok 2>${tmp}-ng
  cat ${tmp}-ng                          |
  awk '{print $0,"0","全店"}'            |
  cat - <(crossjoin -k1 ${tmp}-ok <(cat ${tbld}/MAKER_TENPO_CATEGORY/*|kuniq -k1,2|hijoin -k2 ${tbld}/TEN_NAME)) |
  ssort -k1 |
  wExcel -t ${tmp}-sheet1.xls -s2 -nカテマネ系 -x2 -yA -o ${download}/result_$$.xls
fi
#ヘッダ出力
echo "Accept-Ranges: bytes"
echo "Content-type:application/octet-stream;"
echo "Content-Disposition: attachment; filename=result_$$.xls";
echo "Content-Length: $(wc -c ${download}/result_$$.xls | awk '{print $1}')" 
echo ""

cat ${download}/result_$$.xls
#一時ファイル
#rm -rf $tmp-*
exit 0
