#!/bin/bash
NEWS_URL='http://finance.yahoo.com/rss/headline?s='

# read sources
while IFS='' read -r line || [[ -n "$line" ]]; do
  stock_url="${NEWS_URL}${line}"
  stock_filename="${2}/${line}.xml"
  wget ${stock_url} -O - | xmllint --format - > ${stock_filename}
  echo "Downloaded: $line"
  sleep 2s
done < "$1"

