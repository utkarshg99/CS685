mkdir -p meta
mkdir -p out
# mkdir -p dump
python3 meta.py
echo "Generated Metadata"
python3 q1.py
echo "Generated out/neighbor-districts-modified.json"
python3 q2.py
echo "Generated out/edge-graph.csv"