import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM, 
    AutoTokenizer, 
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

model_path = "./models/qwen/Qwen2.5-7B"
data_path = "./train_v3.2.jsonl"
output_dir = "./aria_qwen3_7b_lora"

tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

def tokenize_function(examples):
    texts = [
        tokenizer.apply_chat_template(msg, tokenize=False, add_generation_prompt=False) 
        for msg in examples["messages"]
    ]
    return tokenizer(texts, truncation=True, max_length=1024, padding=False)

dataset = load_dataset("json", data_files=data_path, split="train")
tokenized_dataset = dataset.map(
    tokenize_function, 
    batched=True, 
    remove_columns=dataset.column_names,
    desc="正在应用对话模板进行分词"
)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    quantization_config=bnb_config,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    trust_remote_code=True
)

model = prepare_model_for_kbit_training(model)
lora_config = LoraConfig(
    r=16, 
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

training_args = TrainingArguments(
    output_dir=output_dir,
    per_device_train_batch_size=2, 
    gradient_accumulation_steps=4, 
    learning_rate=1e-4,
    num_train_epochs=3, 
    bf16=True,
    logging_steps=5,
    save_strategy="epoch", 
    gradient_checkpointing=True, 
    optim="paged_adamw_8bit",
    lr_scheduler_type="cosine",
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False),
)

trainer.train()

final_path = output_dir + "_final"
trainer.model.save_pretrained(final_path)
tokenizer.save_pretrained(final_path)
print(f"✅ 完成！Adapter 产物位于: {final_path}")
