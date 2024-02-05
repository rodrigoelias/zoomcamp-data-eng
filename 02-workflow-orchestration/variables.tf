variable "location" {
  description = "Project Location"
  default     = "EU"
}

variable "project" {
  description = "Mage Project Variable"
  default     = "tidy-agency-412105"
}

variable "bq_dataset_name" {
  description = "Mage BigQuery Dataset Name"
  default     = "mage_dataset"
}

variable "gcs_bucket_name" {
  description = "Mage Storage Bucket Name"
  default     = "tidy-agency-412105-terra-mage-bucket"
}

variable "gcs_storage_class" {
  description = "GCS Storage Class"
  default     = "STANDARD"
}

variable "credentials" {
  description = "Project Credentials"
  default     = "~/.keys/tidy-agency-412105-5e42582866a9.json"
}