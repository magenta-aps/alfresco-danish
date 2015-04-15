#!/bin/bash
#Script is inspired by https://github.com/Redpill-Linpro/alfresco-swedish/blob/master/update-sources.sh


rm -rf ./compare/
mkdir  ./compare/

cd ./compare/

curl 'http://www.tinymce.com/i18n3x/index.php?ctrl=export&act=zip' -H 'Content-Type: application/x-www-form-urlencoded' --data 'la%5B%5D=da&la_export=js&pr_id=7&submitted=Download' > tinymce_da.zip

curl 'https://crowdin.com/download/project/alfresco/da.zip' > crowdin_da.zip



unzip crowdin_da.zip

#***********************#

mkdir -p ./repo/src/main/amp/config/

for f in `find alfresco -type f`; do
  mv $f ${f%.properties}_da.properties;
done;

mv  ./alfresco ./repo/src/main/amp/config/

#***********************#

mv ./share ./share_crowdin

mkdir -p ./share/src/main/amp/config/

for f in `find share_crowdin -type f`; do
  mv $f ${f%.properties}_da.properties;
done;

mv  ./share_crowdin/* ./share/src/main/amp/config/
rm -rf ./share_crowdin


mkdir -p ./share/src/main/amp/web/js/aikau/LATEST
mv ./share/src/main/amp/config/META-INF/js/alfresco ./share/src/main/amp/web/js/aikau/LATEST


#***********************#

mkdir -p ./share/src/main/amp/web/modules/editors/tiny_mce

unzip tinymce_da.zip

mv ./tinymce_language_pack/* ./share/src/main/amp/web/modules/editors/tiny_mce

rm -rf tinymce_language_pack/

#for f in `find rm -type f`; do
#  mv $f ${f%.properties}_da.properties;
#done;






