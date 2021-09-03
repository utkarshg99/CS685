python3 meta_q1.py > meta/edtDist.txt
echo "Generated Metadata"
python3 q1.py
echo "Generated out/neighbor-districts-modified.json"
python3 q2.py
echo "Generated out/edge-graph.csv"
python3 q3.py
echo "Generated out/cases-weekly.csv, out/cases-monthly.csv and out/cases-overall.csv"
python3 q4.py
echo "Generated out/district-peaks.csv, out/state-peaks.csv and out/overall-peaks.csv"