"""Paid interface check on a non-benchmark task; never counted as research data."""
import json
from study import ROOT, MODEL, FINAL_SCHEMA, TOOLS
from run_experiment import Client, personal_key

def main():
    client = Client(personal_key(), ROOT/'outputs'/'api_cost_ledger.jsonl')
    payload = {'model': MODEL, 'store': False, 'temperature': 0.3,
        'instructions': 'This is a software interface test. Return the requested JSON object only.',
        'input': 'Return status answered, an empty claims array, chart_evidence_id null, and explanation interface test successful. Do not call any tools.',
        'tools': TOOLS, 'tool_choice': 'none', 'parallel_tool_calls': False, 'max_output_tokens': 200,
        'text': {'format': {'type': 'json_schema', 'name': 'analysis_answer', 'strict': True, 'schema': FINAL_SCHEMA}}}
    result, cost = client.create(payload, 'smoke_interface')
    texts = [c['text'] for i in result.get('output', []) if i.get('type') == 'message'
             for c in i.get('content', []) if c.get('type') == 'output_text']
    answer = json.loads('\n'.join(texts))
    import jsonschema
    jsonschema.validate(answer, FINAL_SCHEMA)
    record = {'purpose': 'Interface smoke test; not a benchmark result', 'model': result.get('model'),
              'status': result.get('status'), 'answer': answer, 'usage': result['usage'], 'cost_usd': cost}
    (ROOT/'outputs'/'smoke_test.json').write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps(record, indent=2))

if __name__ == '__main__':
    main()
