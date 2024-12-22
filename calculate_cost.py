def estimate_cost(num_instructions: int):
    # Average tokens per interaction
    avg_input_tokens = 300
    avg_output_tokens = 1000
    
    # Total tokens
    total_input_tokens = num_instructions * avg_input_tokens
    total_output_tokens = num_instructions * avg_output_tokens
    
    # Cost in USD
    input_cost = (total_input_tokens / 1_000_000) * 3  # $3 per 1M tokens
    output_cost = (total_output_tokens / 1_000_000) * 15  # $15 per 1M tokens
    
    return {
        'input_tokens': total_input_tokens,
        'output_tokens': total_output_tokens,
        'input_cost': input_cost,
        'output_cost': output_cost,
        'total_cost': input_cost + output_cost,
        'estimated_time_single_key': f"{(num_instructions/5)/5:.1f} minutes",
        'estimated_time_five_keys': f"{(num_instructions/5)/25:.1f} minutes"
    }

# Example usage
print(estimate_cost(100))