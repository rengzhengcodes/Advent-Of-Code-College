# goes through all the folders and times to make sure total runtime for a year is less than 25 seconds
for i in {1..19}
do
    cd $i
    echo $i
    python3 main.py
    cd ../
done