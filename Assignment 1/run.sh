python3 meta.py > dump/meta_obs.txt
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
echo "Generated out/vaccination-population-ratio-district.csv, out/vaccination-population-ratio-state.csv and out/vaccination-population-ratio-overall.csv"
python3 q7.py
echo "Generated out/vaccine-type-ratio-district.csv, out/vaccine-type-ratio-state.csv and out/vaccine-type-ratio-overall.csv"
python3 q8.py
echo "Generated out/vaccinated-dose-ratio-district.csv, out/vaccinated-dose-ratio-state.csv and out/vaccinated-dose-ratio-overall.csv"