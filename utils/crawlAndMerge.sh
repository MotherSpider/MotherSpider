depth=1
threads=5
topN=22 #Comment this statement if you don't want to set topN value
crawldir="afterCrawl/crawldb"
segmentdir="afterCrawl/segments"
urlDir="urls/"
NUTCH_HOME=.
samplePyPath="$NUTCH_HOME/sample.py"

if [ -n "$topN" ]
then
  topN="-topN $topN"
else
  topN=""
fi

steps=8
echo "----- Inject (Step 1 of $steps) -----"
$NUTCH_HOME/nutch inject $crawldir $urlDir

echo "----- Generate, Fetch, Parse, Update (Step 2 of $steps) -----"
for((i=0; i < $depth; i++))
do
  echo "--- Beginning crawl at depth `expr $i + 1` of $depth ---"
  $NUTCH_HOME/nutch generate $crawldir $segmentdir $topN 
      
  if [ $? -ne 0 ]
  then
    echo "runbot: Stopping at depth $depth. No more URLs to fetch."
    break
  fi


  segment=`ls -d $segmentdir/* | tail -1`

  $NUTCH_HOME/nutch fetch $segment -threads $threads
  if [ $? -ne 0 ]
  then
    echo "runbot: fetch $segment at depth `expr $i + 1` failed."
    echo "runbot: Deleting segment $segment."
    rm $RMARGS $segment
    continue
  fi

  echo "--- Beginning parse at depth `expr $i + 1` of $depth ---"
  $NUTCH_HOME/nutch parse $crawdirl $segment $topN 
      
  if [ $? -ne 0 ]
  then
    echo "runbot: Stopping at depth $depth. No more URLs to fetch."
    break
  fi

  $NUTCH_HOME/nutch updatedb $crawldir $segment
done

echo "----- Merge Segments (Step 3 of $steps) -----"
$NUTCH_HOME/nutch mergesegs $crawldir/MERGEDsegments $segmentdir/*

echo "runbot: FINISHED: Crawl completed!"


echo "----- Running Nutchpy on merged segments and getting metadata(Step 4 of $steps) -----"
python $samplePyPath $crawldir/MERGEDsegments/*/content/part-00000/data $crawldir/current/part-00000/data 

echo "runbot: FINISHED: Nutchpy completed!"

echo ""
