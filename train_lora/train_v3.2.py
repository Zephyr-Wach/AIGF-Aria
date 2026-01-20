import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM, 
    AutoTokenizer, 
    TrainingArguments, 
    Trainer, 
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, TaskType

MODEL_ID = "models/Qwen2.5-3B-Instruct"
DATA_PATH = "data/train_v3.2.jsonl"
OUTPUT_DIR = "lora_aigf_v3.2"

def train():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, use_fast=False)
    tokenizer.pad_token = tokenizer.eos_token

    def preprocess_function(example):
        text = "".join([f"<|im_start|>{m['role']}\n{m['content']}<|im_end|>\n" for m in example["messages"]])
        return tokenizer(text, truncation=True, max_length=512, padding=False)

    dataset = load_dataset("json", data_files=DATA_PATH, split="train").map(preprocess_function, remove_columns=["messages"])

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype=torch.float16, 
        device_map={"": "mps"}
    )

    model.gradient_checkpointing_enable() 
    model.enable_input_require_grads()

    peft_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        task_type=TaskType.CAUSAL_LM,
    )
    model = get_peft_model(model, peft_config)

    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=8, 
        learning_rate=1e-5,
        num_train_epochs=2,
        save_strategy="epoch",
        logging_steps=1,
        gradient_checkpointing=True, 
        bf16=False,
        fp16=False,
        report_to="none",
        optim="adamw_torch",
        dataloader_pin_memory=False
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
    )

    trainer.train()
    model.save_pretrained(OUTPUT_DIR)
    print(f"✅ 完成！")

if __name__ == "__main__":
    train()