provider "google" {
    project = "duckcloud-docsearch"
    region = "northamerica-northeast2-b"
}

# Creates a google cloud storage bucket
resource "google_storage_bucket" "doc_storage" {
    name = "duckcloud-docsearch-bucket"
    location = "Canada"
    force_destroy = false

    # Enables version control
    versioning {
        enabled = true
    }

    # Enforces IAM (Identity & Access Management) perms at bucket level only
    uniform_bucket_level_access = true

    # Auto delete old files after 365 days
    lifecycle_rule {
        action {
            type = "Delete"
        }
        condition {
            age = 365
        }
    }

    # Organization purposes
    labels = {
        environment = "dev" # usually depolyment tier, eg. prod, test
        owner = "submergedduck" # who is responsible, eg. data-team, duck
        # project = eg. docsearch, ml-api, backend
        # team = eg. infra, frontend, security
    }
}
