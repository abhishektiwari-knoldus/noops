provider "google" {

credentials = file("./key.json")

project = var.project_id
}

provider "random" {}


resource "random_string" "bucket_name_suffix" {
  length  = 8
  special = false
  upper   = false
  lower   = true
}

resource "google_storage_bucket" "default" {

  name = "noops-${random_string.bucket_name_suffix.result}"

  storage_class = var.storage_class

  location = var.bucket_location


}

resource "google_storage_bucket_object" "index_html" {
  name   = "index.html"
  bucket = google_storage_bucket.default.name
  source = "index.html"
  content_type = "text/html"
}

resource "google_storage_bucket_iam_member" "public_access" {
  bucket = google_storage_bucket.default.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}


# output "bucket_url" {
#   value = "http://${google_storage_bucket.default.name}.storage.googleapis.com"
# }
# Output the bucket URL
output "bucket_url" {
  value = "https://storage.googleapis.com/${google_storage_bucket.default.name}/index.html"
  description = "The URL of the GCS bucket"
}
