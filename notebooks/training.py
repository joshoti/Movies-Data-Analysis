from typing import Union

from datasets import DatasetDict, load_dataset
from pandas import DataFrame
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments


class CustomTrainer:
    output_dir = "../models"

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name

    def load_data(self, csv_path):
        dataset = load_dataset("csv", data_files=csv_path)
        return dataset

    def load_model(sekf, model_name="gpt2"):
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer.pad_token = tokenizer.eos_token
        model = AutoModelForCausalLM.from_pretrained(model_name)
        return model, tokenizer

    def tokenize_dataset(self, tokenizer, dataset: Union[DatasetDict, DataFrame]):
        def tokenize_datasetdict(batch):
            return tokenizer(
                batch["text"], padding="max_length", truncation=True, max_length=128
            )

        def tokenize_dataframe(batch):
            text = [f"{k}: {v}" for k, v in batch.items()]
            text = " ## ".join(text)
            return tokenizer(
                text, padding="max_length", truncation=True, max_length=256
            )

        tokenized_dataset = []
        if isinstance(dataset, DatasetDict):
            tokenized_dataset = dataset.map(tokenize_datasetdict, batched=True)["train"]

        elif isinstance(dataset, DataFrame):
            tokenized_dataset = []
            for index in range(len(dataset)):
                row = dataset.iloc[index]
                tokenized_dataset.append(tokenize_dataframe(row))

        return tokenized_dataset

    # Fine-tune the Model using Parameter-Efficient Fine-Tuning (PEFT)
    def fine_tune_model(self, model, tokenizer, dataset):
        peft_config = LoraConfig(
            task_type="CAUSAL_LM",
            r=4,  # 8
            lora_alpha=16,
            lora_dropout=0.1,
            target_modules=["c_attn"],
        )
        model = get_peft_model(model, peft_config)

        tokenized_dataset = self.tokenize_dataset(dataset)

        training_args = TrainingArguments(
            output_dir=self.output_dir,
            per_device_train_batch_size=2,  # 4
            num_train_epochs=3,
            save_steps=20_000,  # 10_000
            save_total_limit=2,
        )

        trainer = Trainer(
            model=model, args=training_args, train_dataset=tokenized_dataset
        )

        trainer.train()
        model.save_pretrained(self.output_dir)
