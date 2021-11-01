mkdir -p out
python3 meta.py
echo "Generated Metadata"

python3 q1.py
echo "Generated out/percent-india.csv"

python3 q2.py
echo "Generated out/gender-india.csv"

python3 q3.py
echo "Generated out/geography-india.csv"

python3 q4.py
echo "Generated out/3-to-2-ratio.csv and out/2-to-1-ratio.csv"

python3 q5.py
echo "Generated out/age-india.csv"

python3 q6.py
echo "Generated out/literacy-india.csv"

python3 q7.py
echo "Generated out/region-india-a.csv and out/region-india-b.csv"

python3 q8.py
echo "Generated out/age-gender-1.csv, out/age-gender-2.csv and out/age-gender-3.csv"

python3 q9.py
echo "Generated out/literacy-gender-2.csv and out/literacy-gender-3.csv"