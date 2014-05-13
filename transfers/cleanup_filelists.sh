INFILE=$1
infile_label="_raw.txt"

OUTFILE=${INFILE%${infile_label}}".txt" #drop the label in the end of infile
echo Write filelist to $OUTFILE
cmspath="/cms" # spurious string to remove in front of the path

while read line
do
  fullpath=`echo $line | awk '{print $2}'`
  echo ${fullpath#${cmspath}} >> $OUTFILE # subdract /cms and write to outfile 
done<$INFILE
