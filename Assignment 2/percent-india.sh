mkdir -p out
python3 meta.py
echo "Generated Metadata"

python3 q1.py
echo "Generated out/percent-india.csv"