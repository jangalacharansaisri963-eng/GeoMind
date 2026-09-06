export interface ModelInfo {
  model_name: string;
  architecture: string;
  hidden_dimension: number;
  layers: number;
  attention_heads: number;
  intermediate_dimension: number;
  vocabulary_size: number;
  total_parameters: number;
  domains: string[];
  training_epochs_completed: number;
  active_datasets_count: number;
  datasets: string[];
}

export interface DatasetItem {
  filename: string;
  category: string;
  description: string;
  item_count: number;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  domain?: string;
  intent?: string;
  sources?: string[];
  interpreted_query?: string;
  timestamp: string;
  isTraining?: boolean;
}

export interface EpochRecord {
  epoch: number;
  loss: number;
  domain_acc: number;
  intent_acc: number;
}

export interface TrainingResult {
  status: string;
  epochs_trained: number;
  history: EpochRecord[];
  checkpoint_path: string;
  total_parameters: number;
}
