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

# List để lưu kết quả
results = []

for query in queries:
    print(f"\n{'='*70}")
    print(f"{query}")
    print('='*70)
    result = ask(query)
    print(result)
    
    # Lưu kết quả vào list
    results.append({
        "Query": query,
        "Answer": result if result else ""
    })

# Tạo DataFrame từ kết quả
results_df = pd.DataFrame(results)

# Ghi ra file Excel
output_file = root_dir / "agent_test.xlsx"
results_df.to_excel(output_file, index=False, engine='openpyxl')
print(f"\n{'='*70}")
print(f"Đã ghi {len(results)} kết quả vào file: {output_file}")
print('='*70)