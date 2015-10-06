echo "Stats script Started"

crawlFolder=$1

python parser.py $crawlFolder $NUTCH_HOME

$NUTCH_HOME/bin/nutch readdb $crawlFolder/crawldb -stats | tee $crawlFolder/statistics/stats

grep -i "fetch of" $NUTCH_HOME/logs/* > $crawlFolder/statistics/errors

python error.py $crawlFolder/statistics/errors

rm $crawlFolder/statistics/errors

echo "Stats script completed"

