mkdir -p meta
mkdir -p out
# mkdir -p dump
python3 meta.py
echo "Generated Metadata"
python3 q1.py
echo "Generated out/neighbor-districts-modified.json"
python3 q2.py
echo "Generated out/edge-graph.csv"
python3 q3.py
echo "Generated out/cases-weekly.csv, out/cases-monthly.csv and out/cases-overall.csv"
python3 q4.py
echo "Generated out/district-peaks.csv, out/state-peaks.csv and out/overall-peaks.csv"
python3 q5.py
echo "Generated out/vaccinated-count-week.csv, out/vaccinated-count-month.csv and out/vaccinated-count-overall.csv"
python3 q6.py
echo "Generated out/district-vaccination-population-ratio.csv, out/state-vaccination-population-ratio.csv and out/overall-vaccination-population-ratio.csv"
python3 q7.py
echo "Generated out/district-vaccine-type-ratio.csv, out/state-vaccine-type-ratio.csv and out/overall-vaccine-type-ratio.csv"
python3 q8.py
echo "Generated out/district-vaccinated-dose-ratio.csv, out/state-vaccinated-dose-ratio.csv and out/overall-vaccinated-dose-ratio.csv"
python3 q9.py
echo "Generated out/complete-vaccination.csv"