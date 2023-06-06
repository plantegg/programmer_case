for i in {1..100}
    do
    starttime=`date +'%Y-%m-%d %H:%M:%S,%3N'`
    start_seconds=$(date --date="$starttime" +%s%3N);
    curl --max-time 1 -s 172.31.81.55:8000/server.pcap --output ~/aaa.pcap
    endtime=`date +'%Y-%m-%d %H:%M:%S,%3N'`
    end_seconds=$(date --date="$endtime" +%s%3N);
    echo [$starttime] runtime=$((end_seconds-start_seconds))
done