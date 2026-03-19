import json
import multiprocessing
from datasets import load_dataset, Dataset
from transformers import AutoTokenizer
from typing import Dict, Any, Optional, List

def processing_sample(row: Dict[str, Any], tokenizer) -> Dict[str, str]:
    """
    Format for Llama 3.2 function calling:
    <|begin_of_text|><|start_header_id|>user<|end_header_id|>

    [Query]

    Tools: [tools_json]

    Calling: [calls_json]<|eot_id|>
    """
    # Format user query
    formatted_query = f"<user>{row['query']}</user>\n\n"

    # Parse and format available tools
    try:
        parsed_tools = json.loads(row["tools"])
        tools_text = '\n'.join(str(tool) for tool in parsed_tools)
    except json.JSONDecodeError:
        tools_text = str(row["tools"])  # Fallback to raw string
    
    formatted_tools = f"<tools>{tools_text}</tools>\n\n"

    # Parse and format expected function calls
    try:
        parsed_answers = json.loads(row["answers"])
        answers_text = '\n'.join(str(answer) for answer in parsed_answers)
    except json.JSONDecodeError:
        answers_text = str(row["answers"])  # Fallback to raw string

    formatted_answers = f"<calls>{answers_text}</calls>"

    # Combine all parts with EOS token
    complete_text = formatted_query + formatted_tools + formatted_answers + tokenizer.eos_token

    # Update row with processed data
    row["query"] = formatted_query
    row["tools"] = formatted_tools
    row["answers"] = formatted_answers
    row["text"] = complete_text

    return row


def load_and_process_dataset(
    tokenizer: AutoTokenizer, 
    dataset_name: str = "Salesforce/xlam-function-calling-60k", 
    sample_size: Optional[int] = None,
    filter_empty_tools: bool = True,
    max_length: int = 2048
) -> Dataset:
    """
    Load and process dataset optimized for Llama models.
    
    Args:
        tokenizer: The tokenizer for the target Llama model
        dataset_name: HuggingFace dataset name
        sample_size: Number of samples to use (None for all)
        filter_empty_tools: Remove samples with empty tools/answers
        max_length: Maximum sequence length
    """
    print(f"📥 Loading dataset: {dataset_name}")
    dataset = load_dataset(dataset_name, split='train')
    
    # Filter out empty/invalid samples before processing
    if filter_empty_tools:
        original_size = len(dataset)
        dataset = dataset.filter(
            lambda x: bool(x.get('tools', '[]')) and bool(x.get('answers', '[]')),
            desc="Filtering empty samples"
        )
        print(f"🗑️  Filtered out {original_size - len(dataset):,} empty samples")
    
    # Select subset if specified
    if sample_size is not None and sample_size < len(dataset):
        dataset = dataset.select(range(sample_size))
        print(f"🔬 Using sample size: {sample_size:,} samples")
    
    # Process in optimized batches
    def process_batch(batch):
        processed = []
        for i in range(len(batch['query'])):
            row = {
                'query': batch['query'][i],
                'tools': batch['tools'][i],
                'answers': batch['answers'][i]
            }
            processed_row = processing_sample(row, tokenizer)
            processed.append(processed_row)
        
        return {
            'text': [item['text'] for item in processed],
            'query': [item['query'] for item in processed],
            'tools': [item['tools'] for item in processed],
            'answers': [item['answers'] for item in processed]
        }
    
    
    processed_dataset = dataset.map(
        process_batch,
        batched=True,
        batch_size=2000,  # Larger batches for efficiency
        num_proc=min(8, multiprocessing.cpu_count()),  # More parallel processes
        desc="Processing for Llama",
        remove_columns=[col for col in dataset.column_names if col not in ['text', 'tools_json', 'calls_json']]
    )
    
    # Filter by max length
    def filter_by_length(example):
        return len(example['text']) <= max_length
    
    processed_dataset = processed_dataset.filter(
        filter_by_length,
        desc=f"Filtering samples > {max_length} chars"
    )
    
    print("\n✅ Dataset processing complete!")
    print(f"📊 Final dataset size: {len(processed_dataset):,} samples")
    
    if len(processed_dataset) > 0:
        avg_length = sum(len(t) for t in processed_dataset['text']) / len(processed_dataset)
        print(f"🔤 Average text length: {avg_length:,.0f} characters")
        print(f"📏 Estimated tokens/sample: ~{avg_length // 4:.0f}")
    
    return processed_dataset


def preview_dataset_sample(dataset: Dataset, tokenizer=None, index: int = 0) -> None:
    """
    Display a formatted preview of a dataset sample for inspection.
    
    Args:
        dataset: The processed dataset
        tokenizer: Optional tokenizer for token count
        index: Index of the sample to preview (default: 0)
    """
    if index >= len(dataset):
        print(f"❌ Index {index} is out of range. Dataset has {len(dataset)} samples.")
        return
    
    sample = dataset[index]
    
    print(f"\n{'='*80}")
    print(f"📋 Dataset Sample Preview (Index: {index})")
    print(f"{'='*80}\n")
    
    print(f"📝 Complete Training Text:")
    print("-" * 60)
    print(sample['text'])
    print("-" * 60)
    
    print(f"\n📊 Statistics:")
    print(f"   • Text length: {len(sample['text']):,} characters")
    
    if tokenizer:
        tokens = tokenizer.encode(sample['text'])
        print(f"   • Token count: {len(tokens):,} tokens")
    else:
        print(f"   • Estimated tokens: ~{len(sample['text']) // 4:,} tokens")
    
    print(f"\n🛠️  Tools: {sample.get('tools_json', 'N/A')[:100]}...")
    print(f"📞 Calls: {sample.get('calls_json', 'N/A')[:100]}...")
    print(f"\n✅ Preview complete!\n")