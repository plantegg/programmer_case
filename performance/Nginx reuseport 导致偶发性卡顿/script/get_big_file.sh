starttime=`date +'%Y-%m-%d %H:%M:%S,%3N'`
start_seconds=$(date --date="$starttime" +%s%3N);
curl 172.31.81.55:8000/0000000000000000.data --output ~/0000000000000000.data
endtime=`date +'%Y-%m-%d %H:%M:%S,%3N'`
end_seconds=$(date --date="$endtime" +%s%3N);
echo $((end_seconds-start_seconds))