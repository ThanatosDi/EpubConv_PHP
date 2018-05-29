#!/bin/sh

if [ ! $1 ];then
  echo "command: ./epub.sh [filename]"
  exit
else
  if [ ! -f "${1}.epub" ];then
  echo "No file exists"
  #echo "No ${1}.epub file exists"
  exit
  fi
fi

Path=`pwd`
FileName=$1
FolderName=`echo "${1}"|opencc`

echo "-----------------------------------"
echo -e "\n解壓縮 epub 文件中...\n"
echo "-----------------------------------"
7za x $FileName.epub -o$FileName -y

FileArray=($(find ${FileName} -name '*.html' -o -name '*.ncx' -o -name '*.opf' -o -name '*.xhtml' -o -name '*.txt'))
ArrayCounts=`find ${FileName} -name '*.html' -o -name '*.ncx' -o -name '*.opf' -o -name '*.xhtml' -o -name '*.txt'|wc -l`

echo "-----------------------------------"
echo -e "搜尋檔案中\n"
echo -e "符合檔案數量 : ${ArrayCounts}\n"
echo -e "正在翻譯內容中...\n"
echo "-----------------------------------"

for ((i=0;i<${ArrayCounts};i++))
  do
    echo -e "正在處理...${FileArray[$i]}\n"
	#echo -e "重新命名舊有檔案\n"
    mv ${FileArray[$i]} ${FileArray[$i]}.bak
	#echo -e "正在翻譯檔案中...\n"
    opencc -i ${FileArray[$i]}.bak -o ${FileArray[$i]} -c zhs2zhtw_vp.ini
	#echo -e "移除舊有檔案\n"
	rm ${FileArray[$i]}.bak
  done
echo -e "\n正在重新壓縮 epub \n"
7za a -tzip ${FileName}_tc.epub ./${FileName}/*
rm -rf ${FileName} $FileName.epub

