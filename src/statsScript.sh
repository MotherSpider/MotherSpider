crawlFolder=$1

time1=time

python parser.py $crawlFolder $NUTCH_HOME

$NUTCH_HOME/bin/nutch readdb $crawlFolder/crawldb -stats >> $crawlFolder/statistics/stats

while read line           
do  
	echo $line >> $crawlFolder/statistics/unfetchedReasons.txt         
    $NUTCH_HOME/bin/nutch parsechecker $line >> $crawlFolder/statistics/unfetchedReasons.txt
    echo "\n" >> $crawlFolder/statistics/unfetchedReasons.txt            
done <$crawlFolder/statistics/unfetched

time2=time

echo time1
echo "\n"
echo time2
