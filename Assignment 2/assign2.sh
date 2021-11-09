mkdir -p out
python3 meta.py
echo "Generated Metadata"

python3 q1.py
echo "Generated out/percent-india.csv"

python3 q2.py
echo "Generated out/gender-india-a.csv, out/gender-india-b.csv and out/gender-india-c.csv"

python3 q3.py
echo "Generated out/geography-india-a.csv, out/geography-india-b.csv and out/geography-india-c.csv"

python3 q4.py
echo "Generated out/3-to-2-ratio.csv and out/2-to-1-ratio.csv"

python3 q5.py
echo "Generated out/age-india.csv"

python3 q6.py
echo "Generated out/literacy-india.csv"

python3 q7.py
echo "Generated out/region-india-a.csv and out/region-india-b.csv"

python3 q8.py
echo "Generated out/age-gender-a.csv, out/age-gender-b.csv and out/age-gender-c.csv"

python3 q9.py
echo "Generated out/literacy-gender-a.csv, out/literacy-gender-b.csv and out/literacy-gender-c.csv"