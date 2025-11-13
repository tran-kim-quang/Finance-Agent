from agent.agent_handle import ask
from pathlib import Path
import sys
import pandas as pd

root_dir = Path(__file__).parent
# sys.path.insert(0, str(root_dir))

excel_file = root_dir / "AI Intern test questions.xlsx"
df = pd.read_excel(excel_file)
queries = df.iloc[1:14, 0].tolist()
queries = [q for q in queries if pd.notna(q) and str(q).strip()]
print(f"Đã đọc {len(queries)} queries từ file Excel\n")

for query in queries:
    print(f"\n{'='*70}")
    print(f"{query}")
    print('='*70)
    result = ask(query)
    print(result)