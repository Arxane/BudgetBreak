import json
from pathlib import Path


def summarize_results(json_path: str = "outputs/experiment_results.json"):
    path = Path(json_path)
    if not path.exists():
        print(f"File {json_path} not found.")
        return

    with open(path) as f:
        data = json.load(f)

    print(f"\n{'='*65}")
    print(f" BUDGETBREAK EVALUATION REPORT ({len(data)} Total Trials)")
    print(f"{'='*65}")

    for idx, trial in enumerate(data, 1):
        cond = "CONTROL" if trial["is_control"] else "ADVERSARIAL"
        print(f"Trial #{idx} | ID: {trial['scenario_id']} | Mode: {cond}")
        print(f"  Model: {trial['model_name']}")
        print(f"  Tokens (In/Out): {trial['budget']['input_tokens']} / {trial['budget']['output_tokens']}")
        print(f"  Wall Time: {trial['budget']['wall_time_seconds']:.4f}s")
        print(f"  Canary Exposed: {trial['canary_exposed']}")
        print(f"  Unauthorized Action: {trial['unauthorized_action_executed']}")
        print(f"  Benign Task Success: {trial['benign_task_success']}")
        print(f"  False Refusal: {trial['false_refusal']}")
        print("-" * 65)


if __name__ == "__main__":
    summarize_results()